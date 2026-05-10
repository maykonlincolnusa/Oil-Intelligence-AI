from datetime import date, datetime, timedelta, timezone
from random import uniform

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import (
    Chokepoint,
    DeclineCurveAnalysis,
    FireEvent,
    FundamentalRecord,
    GeopoliticalEvent,
    OilField,
    OilSpillObservation,
    Port,
    PortCall,
    PriceSeries,
    ProductionForecast,
    RefinerySite,
    Reservoir,
    SatelliteObservation,
    Scenario,
    StorageSite,
    TankerRoute,
    Vessel,
    VesselPosition,
    Well,
    WellProduction,
)
from app.models.enums import (
    BenchmarkSymbol,
    FundamentalIndicator,
    OilImpact,
    RiskLevel,
    Severity,
    VesselType,
    WellStatus,
    WellType,
)


async def seed_if_empty(session: AsyncSession) -> None:
    price_count = await session.scalar(select(PriceSeries.id).limit(1))
    if price_count:
        return

    now = datetime.now(timezone.utc)

    for symbol, base in [(BenchmarkSymbol.BRENT, 82.0), (BenchmarkSymbol.WTI, 78.0)]:
        for idx in range(90):
            ts = now - timedelta(days=90 - idx)
            value = base + uniform(-3.4, 3.4)
            session.add(
                PriceSeries(
                    symbol=symbol,
                    timestamp=ts,
                    open=value - uniform(0.4, 1.1),
                    high=value + uniform(0.2, 1.5),
                    low=value - uniform(0.2, 1.5),
                    close=value,
                    value=value,
                    source="SEED_MOCK",
                    metadata_json={"benchmark": symbol},
                )
            )

    indicators = [
        FundamentalIndicator.CRUDE_INVENTORY,
        FundamentalIndicator.GASOLINE_INVENTORY,
        FundamentalIndicator.DISTILLATE_INVENTORY,
        FundamentalIndicator.REFINERY_UTILIZATION,
        FundamentalIndicator.PRODUCTION,
        FundamentalIndicator.IMPORTS,
        FundamentalIndicator.EXPORTS,
        FundamentalIndicator.CONSUMPTION,
    ]

    for idx in range(45):
        period = date.today() - timedelta(days=45 - idx)
        for ind in indicators:
            val = {
                FundamentalIndicator.CRUDE_INVENTORY: 440 + uniform(-14, 14),
                FundamentalIndicator.GASOLINE_INVENTORY: 230 + uniform(-9, 9),
                FundamentalIndicator.DISTILLATE_INVENTORY: 120 + uniform(-7, 7),
                FundamentalIndicator.REFINERY_UTILIZATION: 89 + uniform(-2, 2),
                FundamentalIndicator.PRODUCTION: 13.1 + uniform(-0.6, 0.6),
                FundamentalIndicator.IMPORTS: 6.4 + uniform(-0.6, 0.6),
                FundamentalIndicator.EXPORTS: 4.3 + uniform(-0.5, 0.5),
                FundamentalIndicator.CONSUMPTION: 20.0 + uniform(-1.0, 1.0),
            }[ind]
            unit = "percent" if ind == FundamentalIndicator.REFINERY_UTILIZATION else "mbpd"
            if "inventory" in ind:
                unit = "mbbl"
            session.add(
                FundamentalRecord(
                    indicator=ind,
                    country="United States",
                    region="North America",
                    product_type="petroleum",
                    unit=unit,
                    period=period,
                    value=val,
                    source="SEED_MOCK",
                    metadata_json={"frequency": "daily"},
                )
            )

    event_rows = [
        {
            "headline": "Tensions rise near Strait of Hormuz",
            "description": "Naval confrontation triggered temporary tanker rerouting.",
            "categories": ["geopolitical_risk", "maritime_risk", "supply_risk"],
            "oil_impact": OilImpact.BULLISH,
            "risk_level": RiskLevel.HIGH,
            "sentiment": 0.45,
            "regions": ["Middle East"],
            "assets": ["shipping_lanes", "upstream_supply"],
        },
        {
            "headline": "Major Gulf Coast refinery outage",
            "description": "Refinery shutdown reduces distillate output and raises crack spreads.",
            "categories": ["refinery_risk", "supply_risk"],
            "oil_impact": OilImpact.BULLISH,
            "risk_level": RiskLevel.HIGH,
            "sentiment": 0.38,
            "regions": ["North America"],
            "assets": ["refining"],
        },
        {
            "headline": "US crude inventories post surprise draw",
            "description": "Weekly drawdown supports near-term price structure.",
            "categories": ["supply_risk"],
            "oil_impact": OilImpact.BULLISH,
            "risk_level": RiskLevel.MEDIUM,
            "sentiment": 0.22,
            "regions": ["North America"],
            "assets": ["inventory_system"],
        },
        {
            "headline": "Manufacturing slowdown pressures fuel demand",
            "description": "Macro data points to weaker consumption trajectory.",
            "categories": ["demand_risk", "macro_risk"],
            "oil_impact": OilImpact.BEARISH,
            "risk_level": RiskLevel.MEDIUM,
            "sentiment": -0.34,
            "regions": ["Global"],
            "assets": ["demand_centers"],
        },
        {
            "headline": "OPEC+ signals deeper summer output restraint",
            "description": "Delegates discussed extending coordinated cuts amid tight inventories.",
            "categories": ["supply_risk", "geopolitical_risk"],
            "oil_impact": OilImpact.BULLISH,
            "risk_level": RiskLevel.HIGH,
            "sentiment": 0.41,
            "regions": ["Middle East", "Global"],
            "assets": ["upstream_supply"],
        },
        {
            "headline": "Red Sea security corridor partially restored",
            "description": "Escort program lowered immediate disruption risk for product tankers.",
            "categories": ["maritime_risk", "geopolitical_risk"],
            "oil_impact": OilImpact.BEARISH,
            "risk_level": RiskLevel.MEDIUM,
            "sentiment": -0.2,
            "regions": ["Middle East", "North Africa"],
            "assets": ["shipping_lanes"],
        },
    ]
    for i, row in enumerate(event_rows):
        session.add(
            GeopoliticalEvent(
                event_time=now - timedelta(hours=4 + i * 7),
                headline=row["headline"],
                description=row["description"],
                oil_impact=row["oil_impact"],
                sentiment=row["sentiment"],
                risk_level=row["risk_level"],
                categories=row["categories"],
                affected_assets=row["assets"],
                affected_regions=row["regions"],
                confidence_score=0.72,
                source="SEED_MOCK",
                metadata_json={"module": "events"},
            )
        )

    chokepoints = [
        ("Strait of Hormuz", "Middle East", 26.566, 56.25),
        ("Suez Canal", "North Africa", 30.44, 32.35),
        ("Bab el-Mandeb", "Red Sea", 12.7, 43.3),
        ("Turkish Straits", "Black Sea", 41.1, 29.0),
        ("Panama Canal", "Central America", 9.08, -79.68),
        ("Gulf of Mexico", "North America", 24.0, -90.0),
        ("Singapore Strait", "Southeast Asia", 1.23, 103.8),
    ]
    for name, region, lat, lon in chokepoints:
        session.add(
            Chokepoint(
                name=name,
                region=region,
                description=f"Critical maritime energy transit point: {name}",
                latitude=lat,
                longitude=lon,
                location_wkt=f"POINT({lon} {lat})",
                location_geojson={"type": "Point", "coordinates": [lon, lat]},
                location_srid=4326,
                risk_level="high" if name in {"Strait of Hormuz", "Bab el-Mandeb"} else "medium",
                metadata_json={"watch": True},
            )
        )

    ports = [
        ("Ras Tanura", "Saudi Arabia", "Middle East", 26.64, 50.16),
        ("Rotterdam", "Netherlands", "Europe", 51.95, 4.13),
        ("Singapore", "Singapore", "Asia", 1.26, 103.84),
    ]
    for p in ports:
        session.add(
            Port(
                name=p[0],
                country=p[1],
                region=p[2],
                latitude=p[3],
                longitude=p[4],
                location_wkt=f"POINT({p[4]} {p[3]})",
                location_geojson={"type": "Point", "coordinates": [p[4], p[3]]},
                location_srid=4326,
                is_oil_terminal=True,
                metadata_json={"type": "terminal"},
            )
        )

    vessels = [
        ("9387420", "Aegean Star", VesselType.CRUDE_OIL_TANKER, "Liberia", 320000),
        ("9471231", "Atlantic Flow", VesselType.PRODUCT_TANKER, "Marshall Islands", 75000),
        ("9512309", "Arctic LNG", VesselType.LNG_CARRIER, "Norway", 95000),
    ]
    for imo, name, vtype, flag, dwt in vessels:
        session.add(
            Vessel(
                imo=imo,
                name=name,
                vessel_type=vtype,
                flag=flag,
                deadweight_tons=dwt,
                last_known_latitude=24.2 + len(name) * 0.01,
                last_known_longitude=53.4 + len(name) * 0.01,
                location_wkt=f"POINT({53.4 + len(name) * 0.01} {24.2 + len(name) * 0.01})",
                location_geojson={
                    "type": "Point",
                    "coordinates": [53.4 + len(name) * 0.01, 24.2 + len(name) * 0.01],
                },
                location_srid=4326,
                metadata_json={"tracking": "mock"},
            )
        )

    await session.flush()

    vessel_rows = (await session.execute(select(Vessel))).scalars().all()
    port_rows = (await session.execute(select(Port))).scalars().all()
    chokepoint_rows = (await session.execute(select(Chokepoint))).scalars().all()

    for idx, vessel in enumerate(vessel_rows):
        session.add(
            VesselPosition(
                vessel_id=vessel.id,
                timestamp=now - timedelta(minutes=idx * 25),
                latitude=24.0 + idx,
                longitude=53.0 + idx,
                position_wkt=f"POINT({53.0 + idx} {24.0 + idx})",
                speed_knots=12.5 + idx,
                course_degrees=90.0,
                nav_status="under_way",
            )
        )
        session.add(
            TankerRoute(
                vessel_id=vessel.id,
                origin_port_id=port_rows[0].id if port_rows else None,
                destination_port_id=port_rows[min(1, len(port_rows) - 1)].id if port_rows else None,
                eta=now + timedelta(days=7 + idx),
                status="in_transit",
                route_risk_score=68 + idx * 7,
                route_wkt=(
                    f"LINESTRING({50.16 + idx * 0.2} {26.64 - idx * 0.1}, "
                    f"{56.25 + idx * 0.3} {26.57 - idx * 0.2}, {4.13 + idx * 0.2} {51.95 - idx * 0.1})"
                ),
                route_geojson={
                    "type": "LineString",
                    "coordinates": [
                        [50.16 + idx * 0.2, 26.64 - idx * 0.1],
                        [56.25 + idx * 0.3, 26.57 - idx * 0.2],
                        [4.13 + idx * 0.2, 51.95 - idx * 0.1],
                    ],
                },
                route_srid=4326,
                metadata_json={"route": "seed", "name": f"Core Route {idx + 1}"},
            )
        )

    for idx, vessel in enumerate(vessel_rows[:2]):
        cp = chokepoint_rows[idx % len(chokepoint_rows)] if chokepoint_rows else None
        session.add(
            PortCall(
                vessel_id=vessel.id,
                port_id=port_rows[idx % len(port_rows)].id,
                arrival_time=now - timedelta(days=2 - idx),
                departure_time=now - timedelta(days=1 - idx),
                cargo_type="crude",
                status="completed",
            )
        )
        if cp:
            from app.models.maritime import MaritimeAnomaly

            session.add(
                MaritimeAnomaly(
                    vessel_id=vessel.id,
                    chokepoint_id=cp.id,
                    detected_at=now - timedelta(hours=3 + idx),
                    anomaly_type="speed_drop",
                    severity="high",
                    description="Unusual deceleration near chokepoint transit lane.",
                    risk_score=78 - idx * 6,
                    metadata_json={"source": "ais_mock"},
                )
            )

    storage_sites = [
        ("Cushing Hub", "United States", "North America", 35.98, -96.77, 76000000, "Multiple"),
        ("Fujairah Storage", "UAE", "Middle East", 25.12, 56.34, 42000000, "Fujairah Oil Industry"),
    ]
    for s in storage_sites:
        session.add(
            StorageSite(
                name=s[0],
                country=s[1],
                region=s[2],
                latitude=s[3],
                longitude=s[4],
                location_wkt=f"POINT({s[4]} {s[3]})",
                location_geojson={"type": "Point", "coordinates": [s[4], s[3]]},
                location_srid=4326,
                capacity_bbl=s[5],
                operator=s[6],
                metadata_json={"source": "seed"},
            )
        )

    refineries = [
        ("Jamnagar Refinery", "India", "Asia", 22.36, 70.04, 1240000, "Reliance", "operational"),
        ("Baytown Refinery", "United States", "North America", 29.73, -94.96, 560000, "ExxonMobil", "maintenance"),
    ]
    for r in refineries:
        session.add(
            RefinerySite(
                name=r[0],
                country=r[1],
                region=r[2],
                latitude=r[3],
                longitude=r[4],
                location_wkt=f"POINT({r[4]} {r[3]})",
                location_geojson={"type": "Point", "coordinates": [r[4], r[3]]},
                location_srid=4326,
                capacity_bpd=r[5],
                operator=r[6],
                status=r[7],
                metadata_json={"source": "seed"},
            )
        )

    session.add(
        SatelliteObservation(
            provider="Sentinel Hub",
            observed_at=now - timedelta(hours=6),
            latitude=25.2,
            longitude=56.3,
            location_wkt="POINT(56.3 25.2)",
            location_geojson={"type": "Point", "coordinates": [56.3, 25.2]},
            location_srid=4326,
            observation_type="storage_tank_fill_change",
            confidence_score=0.67,
            summary="Moderate draw observed across selected floating-roof tanks.",
            metadata_json={"module": "satellite"},
        )
    )
    session.add(
        FireEvent(
            site_name="Gulf Coast Refinery Cluster",
            detected_at=now - timedelta(hours=8),
            latitude=29.7,
            longitude=-95.1,
            intensity=0.81,
            confidence_score=0.74,
            source="NASA FIRMS",
            metadata_json={"module": "satellite"},
        )
    )
    session.add(
        OilSpillObservation(
            observed_at=now - timedelta(days=1),
            latitude=26.1,
            longitude=50.0,
            estimated_area_km2=4.8,
            severity="medium",
            source="Sentinel Hub",
            metadata_json={"module": "satellite"},
        )
    )

    fields = [
        ("Volve", "Norway", "North Sea", "Equinor", 1993, 58.42, 1.90),
        ("Permian Demo", "United States", "Permian", "Demo Energy", 2008, 31.84, -102.37),
    ]
    for f in fields:
        session.add(
            OilField(
                name=f[0],
                country=f[1],
                basin=f[2],
                operator=f[3],
                status="producing",
                start_year=f[4],
                latitude=f[5],
                longitude=f[6],
                metadata_json={"source": "seed"},
            )
        )

    await session.flush()
    field_rows = (await session.execute(select(OilField))).scalars().all()

    for field in field_rows:
        reservoir = Reservoir(
            field_id=field.id,
            name=f"{field.name} Main Reservoir",
            formation="Sandstone",
            drive_mechanism="water_drive",
            estimated_ooip_mmbbl=520.0,
            status="active",
            metadata_json={"source": "seed"},
        )
        session.add(reservoir)
        await session.flush()

        for idx in range(2):
            well = Well(
                field_id=field.id,
                reservoir_id=reservoir.id,
                name=f"{field.name[:4].upper()}-{idx+1}",
                well_type=WellType.PRODUCER,
                status=WellStatus.ACTIVE,
                spud_date=date.today() - timedelta(days=3200 + idx * 180),
                latitude=(field.latitude or 0) + idx * 0.01,
                longitude=(field.longitude or 0) + idx * 0.01,
                metadata_json={"source": "seed"},
            )
            session.add(well)
            await session.flush()

            for d in range(5):
                session.add(
                    WellProduction(
                        well_id=well.id,
                        period_date=date.today() - timedelta(days=5 - d),
                        oil_bpd=11200 - idx * 450 - d * 120,
                        gas_mmscfd=8.4 - d * 0.12,
                        water_bpd=2400 + d * 40,
                        source="Volve Mock Loader",
                        metadata_json={"source": "seed"},
                    )
                )

            session.add(
                DeclineCurveAnalysis(
                    well_id=well.id,
                    model_type="hyperbolic",
                    qi=12150.0,
                    di=0.11,
                    b_factor=0.78,
                    forecast_horizon_days=365,
                    r_squared=0.91,
                    generated_at=now,
                    metadata_json={"source": "seed"},
                )
            )

        session.add(
            ProductionForecast(
                field_id=field.id,
                horizon_days=180,
                generated_at=now,
                base_case_bpd=22000,
                bullish_case_bpd=24600,
                bearish_case_bpd=19500,
                confidence_score=0.68,
                metadata_json={"source": "seed"},
            )
        )

    scenario_rows = [
        {
            "title": "Strait of Hormuz disruption",
            "event_description": "Escalation temporarily disrupts VLCC transit and raises war-risk premiums.",
            "affected_region": "Middle East",
            "affected_asset": "Shipping Lanes",
            "horizon_days": 30,
            "severity": Severity.HIGH,
        },
        {
            "title": "OPEC+ emergency production cut",
            "event_description": "Coordinated cut deepens prompt crude tightness and widens backwardation.",
            "affected_region": "Global",
            "affected_asset": "Crude Supply",
            "horizon_days": 45,
            "severity": Severity.HIGH,
        },
        {
            "title": "Gulf Coast refinery outage",
            "event_description": "Unplanned outage tightens diesel cracks and dislocates product balances.",
            "affected_region": "North America",
            "affected_asset": "Refining Capacity",
            "horizon_days": 21,
            "severity": Severity.MEDIUM,
        },
    ]
    for row in scenario_rows:
        session.add(
            Scenario(
                title=row["title"],
                event_description=row["event_description"],
                affected_region=row["affected_region"],
                affected_asset=row["affected_asset"],
                horizon_days=row["horizon_days"],
                severity=row["severity"],
                executive_summary=f"{row['title']} baseline assessment indicates elevated monitoring needs.",
                base_case="Partial disruption with adaptive logistics and manageable spread widening.",
                bullish_case="Prolonged disruption tightens balances and supports front-month crude.",
                bearish_case="Rapid normalization reverses risk premium and flattens time spreads.",
                operational_impact="Requires tighter freight monitoring, feedstock optionality, and hedging agility.",
                affected_sectors=["Upstream", "Refining", "Shipping", "Trading"],
                confidence=0.66,
                recommended_monitoring_signals=[
                    "Prompt Brent spread",
                    "Chokepoint transit delays",
                    "Weekly inventories",
                    "Refinery utilization",
                ],
                metadata_json={"source": "seed_scenarios"},
            )
        )

    await session.commit()


async def run_seed(session: AsyncSession) -> None:
    await seed_if_empty(session)
