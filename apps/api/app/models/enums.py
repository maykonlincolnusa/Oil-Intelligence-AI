from enum import StrEnum


class BenchmarkSymbol(StrEnum):
    BRENT = "BRENT"
    WTI = "WTI"


class FundamentalIndicator(StrEnum):
    CRUDE_INVENTORY = "crude_inventory"
    GASOLINE_INVENTORY = "gasoline_inventory"
    DISTILLATE_INVENTORY = "distillate_inventory"
    REFINERY_UTILIZATION = "refinery_utilization"
    PRODUCTION = "production"
    IMPORTS = "imports"
    EXPORTS = "exports"
    CONSUMPTION = "consumption"


class OilImpact(StrEnum):
    BULLISH = "bullish_oil_impact"
    BEARISH = "bearish_oil_impact"
    NEUTRAL = "neutral_oil_impact"


class RiskLevel(StrEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    EXTREME = "extreme"


class EventCategory(StrEnum):
    SUPPLY_RISK = "supply_risk"
    DEMAND_RISK = "demand_risk"
    REFINERY_RISK = "refinery_risk"
    MARITIME_RISK = "maritime_risk"
    GEOPOLITICAL_RISK = "geopolitical_risk"
    MACRO_RISK = "macro_risk"


class Severity(StrEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    EXTREME = "extreme"


class VesselType(StrEnum):
    CRUDE_OIL_TANKER = "crude_oil_tanker"
    PRODUCT_TANKER = "product_tanker"
    LNG_CARRIER = "lng_carrier"
    LPG_CARRIER = "lpg_carrier"
    CHEMICAL_TANKER = "chemical_tanker"


class SiteStatus(StrEnum):
    OPERATIONAL = "operational"
    MAINTENANCE = "maintenance"
    OUTAGE = "outage"


class WellType(StrEnum):
    PRODUCER = "producer"
    INJECTOR = "injector"
    EXPLORATION = "exploration"


class WellStatus(StrEnum):
    ACTIVE = "active"
    SHUT_IN = "shut_in"
    ABANDONED = "abandoned"
