from datetime import datetime, timezone

from sqlalchemy import desc, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.enums import FundamentalIndicator
from app.models.risk import AlertEvent, AlertRule
from app.repositories import EventRepository, FundamentalsRepository, MarketRepository
from app.services.maritime_service import MaritimeService
from app.services.risk_scoring_service import RiskScoringService
from app.services.satellite_service import SatelliteService


DEFAULT_ALERT_RULES = [
    {
        "rule_key": "brent_move_gt_3",
        "name": "Brent daily move > 3%",
        "description": "Trigger when absolute Brent change exceeds 3%",
        "threshold": 3.0,
        "comparator": ">",
    },
    {
        "rule_key": "wti_move_gt_3",
        "name": "WTI daily move > 3%",
        "description": "Trigger when absolute WTI change exceeds 3%",
        "threshold": 3.0,
        "comparator": ">",
    },
    {
        "rule_key": "global_risk_gt_75",
        "name": "Global oil risk score > 75",
        "description": "Trigger on broad multi-factor oil market stress",
        "threshold": 75.0,
        "comparator": ">",
    },
    {
        "rule_key": "geopolitical_risk_gt_75",
        "name": "Geopolitical risk score > 75",
        "description": "Trigger on elevated geopolitical risk stress",
        "threshold": 75.0,
        "comparator": ">",
    },
    {
        "rule_key": "maritime_risk_gt_70",
        "name": "Maritime risk score > 70",
        "description": "Trigger on elevated maritime risk stress",
        "threshold": 70.0,
        "comparator": ">",
    },
    {
        "rule_key": "chokepoint_disruption_detected",
        "name": "Chokepoint disruption event detected",
        "description": "Trigger when recent events mention strategic chokepoint disruption",
        "threshold": 1.0,
        "comparator": ">=",
    },
    {
        "rule_key": "refinery_event_detected",
        "name": "Refinery event detected",
        "description": "Trigger on refinery event category or thermal fire signal",
        "threshold": 1.0,
        "comparator": ">=",
    },
    {
        "rule_key": "inventory_drawdown_threshold",
        "name": "Inventory drawdown above threshold",
        "description": "Trigger when crude inventory draw exceeds 6 mbbl",
        "threshold": 6.0,
        "comparator": ">",
    },
]


class AlertService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.market_repo = MarketRepository(session)
        self.fund_repo = FundamentalsRepository(session)
        self.event_repo = EventRepository(session)
        self.risk_service = RiskScoringService(session)
        self.maritime_service = MaritimeService(session)
        self.satellite_service = SatelliteService(session)

    async def ensure_default_rules(self) -> None:
        existing = await self.session.execute(select(AlertRule.rule_key))
        existing_keys = {row[0] for row in existing.all()}

        created = False
        for rule in DEFAULT_ALERT_RULES:
            if rule["rule_key"] in existing_keys:
                continue
            self.session.add(
                AlertRule(
                    rule_key=rule["rule_key"],
                    name=rule["name"],
                    description=rule["description"],
                    threshold=rule["threshold"],
                    comparator=rule["comparator"],
                    enabled=True,
                    metadata_json={"seeded": True},
                )
            )
            created = True
        if created:
            await self.session.commit()

    async def list_rules(self, limit: int = 200, offset: int = 0) -> list[AlertRule]:
        await self.ensure_default_rules()
        rows = await self.session.execute(
            select(AlertRule).order_by(AlertRule.rule_key).offset(offset).limit(limit)
        )
        return list(rows.scalars().all())

    async def count_rules(self) -> int:
        await self.ensure_default_rules()
        result = await self.session.execute(select(func.count()).select_from(AlertRule))
        return int(result.scalar_one())

    async def list_events(self, limit: int = 50, offset: int = 0) -> list[AlertEvent]:
        rows = await self.session.execute(
            select(AlertEvent)
            .order_by(desc(AlertEvent.triggered_at))
            .offset(offset)
            .limit(limit)
        )
        return list(rows.scalars().all())

    async def count_events(self) -> int:
        result = await self.session.execute(select(func.count()).select_from(AlertEvent))
        return int(result.scalar_one())

    async def evaluate(self) -> dict:
        await self.ensure_default_rules()
        rules = await self.list_rules(limit=500, offset=0)

        brent_move = await self._price_move_percent("BRENT")
        wti_move = await self._price_move_percent("WTI")
        risk = await self.risk_service.calculate()
        maritime = await self.maritime_service.risk_summary()
        refinery_flag = await self._refinery_event_flag()
        chokepoint_flag = await self._chokepoint_disruption_flag()
        drawdown = await self._inventory_drawdown_magnitude()

        metrics = {
            "brent_move_gt_3": abs(brent_move),
            "wti_move_gt_3": abs(wti_move),
            "global_risk_gt_75": float(risk["global_risk_score"]),
            "geopolitical_risk_gt_75": float(risk["geopolitical_risk_score"]),
            "maritime_risk_gt_70": float(maritime["maritime_risk_score"]),
            "refinery_event_detected": float(refinery_flag),
            "chokepoint_disruption_detected": float(chokepoint_flag),
            "inventory_drawdown_threshold": drawdown,
        }

        triggered_events: list[AlertEvent] = []
        now = datetime.now(timezone.utc)

        for rule in rules:
            if not rule.enabled:
                continue
            value = metrics.get(rule.rule_key, 0.0)
            triggered = self._evaluate_comparator(value, rule.comparator, rule.threshold)
            if not triggered:
                continue

            message = self._build_alert_message(rule.rule_key, value, rule.threshold)
            severity = "high" if value >= (rule.threshold * 1.35 if rule.threshold else 1) else "medium"
            event = AlertEvent(
                rule_key=rule.rule_key,
                triggered_at=now,
                severity=severity,
                message=message,
                metric_value=value,
                threshold_value=rule.threshold,
                is_active=True,
                metadata_json={"comparator": rule.comparator},
            )
            self.session.add(event)
            triggered_events.append(event)

        await self.session.commit()

        events_payload = [
            {
                "rule_key": e.rule_key,
                "triggered_at": e.triggered_at,
                "severity": e.severity,
                "message": e.message,
                "metric_value": e.metric_value,
                "threshold_value": e.threshold_value,
                "is_active": e.is_active,
            }
            for e in triggered_events
        ]

        return {
            "evaluated_at": now,
            "triggered_count": len(triggered_events),
            "events": events_payload,
        }

    async def _price_move_percent(self, symbol: str) -> float:
        rows = await self.market_repo.get_prices(symbol=symbol, limit=2)
        if len(rows) < 2:
            return 0.0
        latest = float(rows[0].value)
        previous = float(rows[1].value)
        if previous == 0:
            return 0.0
        return ((latest - previous) / previous) * 100

    async def _inventory_drawdown_magnitude(self) -> float:
        rows = await self.fund_repo.get_fundamentals(
            indicator=FundamentalIndicator.CRUDE_INVENTORY,
            limit=2,
        )
        if len(rows) < 2:
            return 0.0
        latest = float(rows[0].value)
        previous = float(rows[1].value)
        drawdown = previous - latest
        return max(0.0, drawdown)

    async def _refinery_event_flag(self) -> int:
        events = await self.event_repo.get_recent_events(days=7)
        if any("refinery_risk" in event.categories for event in events):
            return 1

        satellite_summary = await self.satellite_service.summary()
        if satellite_summary.get("active_fire_events", 0) > 0:
            return 1

        return 0

    async def _chokepoint_disruption_flag(self) -> int:
        events = await self.event_repo.get_recent_events(days=7)
        terms = [
            "hormuz",
            "suez",
            "bab el-mandeb",
            "red sea",
            "turkish straits",
            "panama canal",
            "singapore strait",
        ]
        for event in events:
            text = f"{event.headline} {event.description}".lower()
            if any(term in text for term in terms):
                return 1
        return 0

    @staticmethod
    def _evaluate_comparator(value: float, comparator: str, threshold: float) -> bool:
        if comparator == ">":
            return value > threshold
        if comparator == ">=":
            return value >= threshold
        if comparator == "<":
            return value < threshold
        if comparator == "<=":
            return value <= threshold
        return False

    @staticmethod
    def _build_alert_message(rule_key: str, value: float, threshold: float) -> str:
        templates = {
            "brent_move_gt_3": f"Brent moved {value:.2f}% (threshold {threshold:.2f}%)",
            "wti_move_gt_3": f"WTI moved {value:.2f}% (threshold {threshold:.2f}%)",
            "global_risk_gt_75": f"Global oil risk score reached {value:.0f} (threshold {threshold:.0f})",
            "geopolitical_risk_gt_75": (
                f"Geopolitical risk score reached {value:.0f} (threshold {threshold:.0f})"
            ),
            "maritime_risk_gt_70": f"Maritime risk score reached {value:.0f} (threshold {threshold:.0f})",
            "refinery_event_detected": "Refinery event signal detected from events/satellite feed",
            "chokepoint_disruption_detected": "Strategic chokepoint disruption signal detected",
            "inventory_drawdown_threshold": (
                f"Crude inventory drawdown of {value:.2f} mbbl exceeded {threshold:.2f} mbbl"
            ),
        }
        return templates.get(rule_key, f"Alert triggered: {rule_key}")
