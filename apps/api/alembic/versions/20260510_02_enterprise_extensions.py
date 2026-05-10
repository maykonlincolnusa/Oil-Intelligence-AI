"""enterprise architecture upgrades: timescale, postgis-ready fields, reports, alerts

Revision ID: 20260510_02
Revises: 20260510_01
Create Date: 2026-05-10 00:30:00
"""

from alembic import op

# revision identifiers, used by Alembic.
revision = "20260510_02"
down_revision = "20260510_01"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute(
        """
        DO $$
        BEGIN
            IF EXISTS (SELECT 1 FROM pg_available_extensions WHERE name = 'timescaledb') THEN
                CREATE EXTENSION IF NOT EXISTS timescaledb;
            END IF;
        EXCEPTION WHEN OTHERS THEN
            RAISE NOTICE 'TimescaleDB extension not installed or not permitted.';
        END $$;
        """
    )
    op.execute(
        """
        DO $$
        BEGIN
            IF EXISTS (SELECT 1 FROM pg_available_extensions WHERE name = 'postgis') THEN
                CREATE EXTENSION IF NOT EXISTS postgis;
            END IF;
        EXCEPTION WHEN OTHERS THEN
            RAISE NOTICE 'PostGIS extension not installed or not permitted.';
        END $$;
        """
    )

    op.execute("ALTER TABLE ports ADD COLUMN IF NOT EXISTS location_wkt VARCHAR(180)")
    op.execute("ALTER TABLE ports ADD COLUMN IF NOT EXISTS location_geojson JSONB DEFAULT '{}'::jsonb")
    op.execute("ALTER TABLE ports ADD COLUMN IF NOT EXISTS location_srid INTEGER DEFAULT 4326")

    op.execute("ALTER TABLE chokepoints ADD COLUMN IF NOT EXISTS location_wkt VARCHAR(180)")
    op.execute(
        "ALTER TABLE chokepoints ADD COLUMN IF NOT EXISTS location_geojson JSONB DEFAULT '{}'::jsonb"
    )
    op.execute("ALTER TABLE chokepoints ADD COLUMN IF NOT EXISTS location_srid INTEGER DEFAULT 4326")

    op.execute("ALTER TABLE vessels ADD COLUMN IF NOT EXISTS last_known_latitude DOUBLE PRECISION")
    op.execute("ALTER TABLE vessels ADD COLUMN IF NOT EXISTS last_known_longitude DOUBLE PRECISION")
    op.execute("ALTER TABLE vessels ADD COLUMN IF NOT EXISTS location_wkt VARCHAR(180)")
    op.execute("ALTER TABLE vessels ADD COLUMN IF NOT EXISTS location_geojson JSONB DEFAULT '{}'::jsonb")
    op.execute("ALTER TABLE vessels ADD COLUMN IF NOT EXISTS location_srid INTEGER DEFAULT 4326")

    op.execute("ALTER TABLE vessel_positions ADD COLUMN IF NOT EXISTS position_wkt VARCHAR(180)")

    op.execute("ALTER TABLE tanker_routes ADD COLUMN IF NOT EXISTS route_wkt TEXT")
    op.execute("ALTER TABLE tanker_routes ADD COLUMN IF NOT EXISTS route_geojson JSONB DEFAULT '{}'::jsonb")
    op.execute("ALTER TABLE tanker_routes ADD COLUMN IF NOT EXISTS route_srid INTEGER DEFAULT 4326")

    op.execute("ALTER TABLE storage_sites ADD COLUMN IF NOT EXISTS location_wkt VARCHAR(180)")
    op.execute(
        "ALTER TABLE storage_sites ADD COLUMN IF NOT EXISTS location_geojson JSONB DEFAULT '{}'::jsonb"
    )
    op.execute("ALTER TABLE storage_sites ADD COLUMN IF NOT EXISTS location_srid INTEGER DEFAULT 4326")

    op.execute("ALTER TABLE refinery_sites ADD COLUMN IF NOT EXISTS location_wkt VARCHAR(180)")
    op.execute(
        "ALTER TABLE refinery_sites ADD COLUMN IF NOT EXISTS location_geojson JSONB DEFAULT '{}'::jsonb"
    )
    op.execute("ALTER TABLE refinery_sites ADD COLUMN IF NOT EXISTS location_srid INTEGER DEFAULT 4326")

    op.execute("ALTER TABLE satellite_observations ADD COLUMN IF NOT EXISTS location_wkt VARCHAR(180)")
    op.execute(
        "ALTER TABLE satellite_observations ADD COLUMN IF NOT EXISTS location_geojson JSONB DEFAULT '{}'::jsonb"
    )
    op.execute(
        "ALTER TABLE satellite_observations ADD COLUMN IF NOT EXISTS location_srid INTEGER DEFAULT 4326"
    )

    op.execute(
        """
        CREATE TABLE IF NOT EXISTS alert_rules (
            id SERIAL PRIMARY KEY,
            rule_key VARCHAR(80) UNIQUE NOT NULL,
            name VARCHAR(180) NOT NULL,
            description TEXT NOT NULL,
            threshold DOUBLE PRECISION NOT NULL,
            comparator VARCHAR(10) NOT NULL DEFAULT '>',
            enabled BOOLEAN NOT NULL DEFAULT TRUE,
            metadata_json JSONB NOT NULL DEFAULT '{}'::jsonb,
            created_at TIMESTAMPTZ DEFAULT now(),
            updated_at TIMESTAMPTZ DEFAULT now()
        )
        """
    )
    op.execute("CREATE INDEX IF NOT EXISTS ix_alert_rules_rule_key ON alert_rules (rule_key)")

    op.execute(
        """
        CREATE TABLE IF NOT EXISTS alert_events (
            id SERIAL PRIMARY KEY,
            rule_key VARCHAR(80) NOT NULL,
            triggered_at TIMESTAMPTZ NOT NULL,
            severity VARCHAR(20) NOT NULL DEFAULT 'medium',
            message TEXT NOT NULL,
            metric_value DOUBLE PRECISION,
            threshold_value DOUBLE PRECISION,
            is_active BOOLEAN NOT NULL DEFAULT TRUE,
            metadata_json JSONB NOT NULL DEFAULT '{}'::jsonb,
            created_at TIMESTAMPTZ DEFAULT now(),
            updated_at TIMESTAMPTZ DEFAULT now()
        )
        """
    )
    op.execute("CREATE INDEX IF NOT EXISTS ix_alert_events_rule_key ON alert_events (rule_key)")
    op.execute("CREATE INDEX IF NOT EXISTS ix_alert_events_triggered_at ON alert_events (triggered_at)")

    op.execute(
        """
        CREATE TABLE IF NOT EXISTS daily_intelligence_reports (
            id SERIAL PRIMARY KEY,
            report_date DATE UNIQUE NOT NULL,
            market_summary TEXT NOT NULL,
            top_price_movers JSONB NOT NULL DEFAULT '[]'::jsonb,
            top_geopolitical_events JSONB NOT NULL DEFAULT '[]'::jsonb,
            risk_score INTEGER NOT NULL,
            maritime_risk_score INTEGER NOT NULL,
            refinery_storage_alerts JSONB NOT NULL DEFAULT '[]'::jsonb,
            scenario_watchlist JSONB NOT NULL DEFAULT '[]'::jsonb,
            executive_summary TEXT NOT NULL,
            confidence DOUBLE PRECISION NOT NULL DEFAULT 0.65,
            metadata_json JSONB NOT NULL DEFAULT '{}'::jsonb,
            created_at TIMESTAMPTZ DEFAULT now(),
            updated_at TIMESTAMPTZ DEFAULT now()
        )
        """
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_daily_intelligence_reports_report_date ON daily_intelligence_reports (report_date)"
    )

    op.execute(
        """
        DO $$
        BEGIN
            IF EXISTS (SELECT 1 FROM pg_extension WHERE extname = 'postgis') THEN
                EXECUTE 'ALTER TABLE ports ADD COLUMN IF NOT EXISTS location_geom geometry(Point,4326)';
                EXECUTE 'ALTER TABLE chokepoints ADD COLUMN IF NOT EXISTS location_geom geometry(Point,4326)';
                EXECUTE 'ALTER TABLE vessels ADD COLUMN IF NOT EXISTS location_geom geometry(Point,4326)';
                EXECUTE 'ALTER TABLE vessel_positions ADD COLUMN IF NOT EXISTS position_geom geometry(Point,4326)';
                EXECUTE 'ALTER TABLE tanker_routes ADD COLUMN IF NOT EXISTS route_geom geometry(LineString,4326)';
                EXECUTE 'ALTER TABLE storage_sites ADD COLUMN IF NOT EXISTS location_geom geometry(Point,4326)';
                EXECUTE 'ALTER TABLE refinery_sites ADD COLUMN IF NOT EXISTS location_geom geometry(Point,4326)';
                EXECUTE 'ALTER TABLE satellite_observations ADD COLUMN IF NOT EXISTS location_geom geometry(Point,4326)';
            END IF;
        EXCEPTION WHEN OTHERS THEN
            RAISE NOTICE 'PostGIS geometry column setup skipped.';
        END $$;
        """
    )

    op.execute(
        """
        DO $$
        BEGIN
            IF EXISTS (SELECT 1 FROM pg_extension WHERE extname = 'timescaledb') THEN
                BEGIN
                    PERFORM create_hypertable(
                        'price_series',
                        by_range('timestamp', INTERVAL '7 days'),
                        if_not_exists => TRUE,
                        migrate_data => TRUE
                    );
                    PERFORM create_hypertable(
                        'fundamental_records',
                        by_range('period', INTERVAL '30 days'),
                        if_not_exists => TRUE,
                        migrate_data => TRUE
                    );
                EXCEPTION WHEN OTHERS THEN
                    PERFORM create_hypertable(
                        'price_series',
                        'timestamp',
                        if_not_exists => TRUE,
                        migrate_data => TRUE,
                        chunk_time_interval => INTERVAL '7 days'
                    );
                    PERFORM create_hypertable(
                        'fundamental_records',
                        'period',
                        if_not_exists => TRUE,
                        migrate_data => TRUE,
                        chunk_time_interval => INTERVAL '30 days'
                    );
                END;
            END IF;
        EXCEPTION WHEN OTHERS THEN
            RAISE NOTICE 'Hypertable conversion skipped.';
        END $$;
        """
    )


def downgrade() -> None:
    op.execute("DROP TABLE IF EXISTS daily_intelligence_reports")
    op.execute("DROP TABLE IF EXISTS alert_events")
    op.execute("DROP TABLE IF EXISTS alert_rules")

    op.execute("ALTER TABLE satellite_observations DROP COLUMN IF EXISTS location_geom")
    op.execute("ALTER TABLE satellite_observations DROP COLUMN IF EXISTS location_wkt")
    op.execute("ALTER TABLE satellite_observations DROP COLUMN IF EXISTS location_geojson")
    op.execute("ALTER TABLE satellite_observations DROP COLUMN IF EXISTS location_srid")

    op.execute("ALTER TABLE refinery_sites DROP COLUMN IF EXISTS location_geom")
    op.execute("ALTER TABLE refinery_sites DROP COLUMN IF EXISTS location_wkt")
    op.execute("ALTER TABLE refinery_sites DROP COLUMN IF EXISTS location_geojson")
    op.execute("ALTER TABLE refinery_sites DROP COLUMN IF EXISTS location_srid")

    op.execute("ALTER TABLE storage_sites DROP COLUMN IF EXISTS location_geom")
    op.execute("ALTER TABLE storage_sites DROP COLUMN IF EXISTS location_wkt")
    op.execute("ALTER TABLE storage_sites DROP COLUMN IF EXISTS location_geojson")
    op.execute("ALTER TABLE storage_sites DROP COLUMN IF EXISTS location_srid")

    op.execute("ALTER TABLE tanker_routes DROP COLUMN IF EXISTS route_geom")
    op.execute("ALTER TABLE tanker_routes DROP COLUMN IF EXISTS route_wkt")
    op.execute("ALTER TABLE tanker_routes DROP COLUMN IF EXISTS route_geojson")
    op.execute("ALTER TABLE tanker_routes DROP COLUMN IF EXISTS route_srid")

    op.execute("ALTER TABLE vessel_positions DROP COLUMN IF EXISTS position_geom")
    op.execute("ALTER TABLE vessel_positions DROP COLUMN IF EXISTS position_wkt")

    op.execute("ALTER TABLE vessels DROP COLUMN IF EXISTS location_geom")
    op.execute("ALTER TABLE vessels DROP COLUMN IF EXISTS last_known_latitude")
    op.execute("ALTER TABLE vessels DROP COLUMN IF EXISTS last_known_longitude")
    op.execute("ALTER TABLE vessels DROP COLUMN IF EXISTS location_wkt")
    op.execute("ALTER TABLE vessels DROP COLUMN IF EXISTS location_geojson")
    op.execute("ALTER TABLE vessels DROP COLUMN IF EXISTS location_srid")

    op.execute("ALTER TABLE chokepoints DROP COLUMN IF EXISTS location_geom")
    op.execute("ALTER TABLE chokepoints DROP COLUMN IF EXISTS location_wkt")
    op.execute("ALTER TABLE chokepoints DROP COLUMN IF EXISTS location_geojson")
    op.execute("ALTER TABLE chokepoints DROP COLUMN IF EXISTS location_srid")

    op.execute("ALTER TABLE ports DROP COLUMN IF EXISTS location_geom")
    op.execute("ALTER TABLE ports DROP COLUMN IF EXISTS location_wkt")
    op.execute("ALTER TABLE ports DROP COLUMN IF EXISTS location_geojson")
    op.execute("ALTER TABLE ports DROP COLUMN IF EXISTS location_srid")
