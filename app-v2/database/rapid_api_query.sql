-- Active: 1778497325951@@localhost@5432@autoparts
-- ==========================================================================
-- rapid_api_query.sql — FULL up-to-date schema for the RapidAPI dump
--
-- SOURCE OF TRUTH for the database schema.
-- It always reflects the current state of every table, index, constraint, sequence.
--
-- WORKFLOW:
--   1. To bootstrap a fresh DB: run this file once.
--   2. When the schema needs to change (new column, new index, etc.):
--      a. Add a migration file at `database/migrations/NNN_<description>.sql`
--         with ONLY the diff queries (ALTER TABLE, CREATE INDEX, etc.).
--      b. Update THIS file to reflect the new state after the migration applies.
--      c. Both must stay in sync.
--
-- NAMING CONVENTION: every table sourced from RapidAPI data carries the
-- `rapid_api_` prefix. This makes it obvious which tables hold third-party
-- dumped data vs. our own application data.
--
-- DFS CRAWL RESUMABILITY: `*_fetched_at` columns on parent tables act as
-- per-row cursors. A row with NULL means "still to fetch children for it."
-- Partial indexes on `WHERE *_fetched_at IS NULL` make next-work-item
-- lookups O(1) regardless of how many done rows exist.
-- ==========================================================================

-- ==================== SEQUENCES (type-agnostic) ====================
CREATE SEQUENCE IF NOT EXISTS seq_languages       START 1;
CREATE SEQUENCE IF NOT EXISTS seq_countries       START 1;
CREATE SEQUENCE IF NOT EXISTS seq_vehicle_types   START 1;
CREATE SEQUENCE IF NOT EXISTS seq_manufacturers   START 1;
CREATE SEQUENCE IF NOT EXISTS seq_dump_jobs       START 1;

-- ==================== SEQUENCES (type-scoped) ====================
-- 11 vehicle type codes: pc, cv, moto, lcv, dcab, axle, eng, bus, aft, trac, voem
-- Each type-scoped table needs 11 sequences (one per type).

-- manufacturer_vehicle_types
CREATE SEQUENCE IF NOT EXISTS seq_mvt_pc    START 1;
CREATE SEQUENCE IF NOT EXISTS seq_mvt_cv    START 1;
CREATE SEQUENCE IF NOT EXISTS seq_mvt_moto  START 1;
CREATE SEQUENCE IF NOT EXISTS seq_mvt_lcv   START 1;
CREATE SEQUENCE IF NOT EXISTS seq_mvt_dcab  START 1;
CREATE SEQUENCE IF NOT EXISTS seq_mvt_axle  START 1;
CREATE SEQUENCE IF NOT EXISTS seq_mvt_eng   START 1;
CREATE SEQUENCE IF NOT EXISTS seq_mvt_bus   START 1;
CREATE SEQUENCE IF NOT EXISTS seq_mvt_aft   START 1;
CREATE SEQUENCE IF NOT EXISTS seq_mvt_trac  START 1;
CREATE SEQUENCE IF NOT EXISTS seq_mvt_voem  START 1;

-- models
CREATE SEQUENCE IF NOT EXISTS seq_models_pc    START 1;
CREATE SEQUENCE IF NOT EXISTS seq_models_cv    START 1;
CREATE SEQUENCE IF NOT EXISTS seq_models_moto  START 1;
CREATE SEQUENCE IF NOT EXISTS seq_models_lcv   START 1;
CREATE SEQUENCE IF NOT EXISTS seq_models_dcab  START 1;
CREATE SEQUENCE IF NOT EXISTS seq_models_axle  START 1;
CREATE SEQUENCE IF NOT EXISTS seq_models_eng   START 1;
CREATE SEQUENCE IF NOT EXISTS seq_models_bus   START 1;
CREATE SEQUENCE IF NOT EXISTS seq_models_aft   START 1;
CREATE SEQUENCE IF NOT EXISTS seq_models_trac  START 1;
CREATE SEQUENCE IF NOT EXISTS seq_models_voem  START 1;

-- vehicles
CREATE SEQUENCE IF NOT EXISTS seq_vehicles_pc    START 1;
CREATE SEQUENCE IF NOT EXISTS seq_vehicles_cv    START 1;
CREATE SEQUENCE IF NOT EXISTS seq_vehicles_moto  START 1;
CREATE SEQUENCE IF NOT EXISTS seq_vehicles_lcv   START 1;
CREATE SEQUENCE IF NOT EXISTS seq_vehicles_dcab  START 1;
CREATE SEQUENCE IF NOT EXISTS seq_vehicles_axle  START 1;
CREATE SEQUENCE IF NOT EXISTS seq_vehicles_eng   START 1;
CREATE SEQUENCE IF NOT EXISTS seq_vehicles_bus   START 1;
CREATE SEQUENCE IF NOT EXISTS seq_vehicles_aft   START 1;
CREATE SEQUENCE IF NOT EXISTS seq_vehicles_trac  START 1;
CREATE SEQUENCE IF NOT EXISTS seq_vehicles_voem  START 1;

-- categories
CREATE SEQUENCE IF NOT EXISTS seq_categories_pc    START 1;
CREATE SEQUENCE IF NOT EXISTS seq_categories_cv    START 1;
CREATE SEQUENCE IF NOT EXISTS seq_categories_moto  START 1;
CREATE SEQUENCE IF NOT EXISTS seq_categories_lcv   START 1;
CREATE SEQUENCE IF NOT EXISTS seq_categories_dcab  START 1;
CREATE SEQUENCE IF NOT EXISTS seq_categories_axle  START 1;
CREATE SEQUENCE IF NOT EXISTS seq_categories_eng   START 1;
CREATE SEQUENCE IF NOT EXISTS seq_categories_bus   START 1;
CREATE SEQUENCE IF NOT EXISTS seq_categories_aft   START 1;
CREATE SEQUENCE IF NOT EXISTS seq_categories_trac  START 1;
CREATE SEQUENCE IF NOT EXISTS seq_categories_voem  START 1;

-- vehicle_categories
CREATE SEQUENCE IF NOT EXISTS seq_vca_pc    START 1;
CREATE SEQUENCE IF NOT EXISTS seq_vca_cv    START 1;
CREATE SEQUENCE IF NOT EXISTS seq_vca_moto  START 1;
CREATE SEQUENCE IF NOT EXISTS seq_vca_lcv   START 1;
CREATE SEQUENCE IF NOT EXISTS seq_vca_dcab  START 1;
CREATE SEQUENCE IF NOT EXISTS seq_vca_axle  START 1;
CREATE SEQUENCE IF NOT EXISTS seq_vca_eng   START 1;
CREATE SEQUENCE IF NOT EXISTS seq_vca_bus   START 1;
CREATE SEQUENCE IF NOT EXISTS seq_vca_aft   START 1;
CREATE SEQUENCE IF NOT EXISTS seq_vca_trac  START 1;
CREATE SEQUENCE IF NOT EXISTS seq_vca_voem  START 1;

-- ==================== REFERENCE TABLES ====================

-- API 1 — Languages
CREATE TABLE IF NOT EXISTS rapid_api_languages (
    language_id     TEXT        PRIMARY KEY,          -- LNG_001
    external_id     INT         NOT NULL UNIQUE,      -- from API: lngId
    iso_code        VARCHAR(10),                      -- from API: lngIso2 (nullable, e.g. "Universal")
    description     VARCHAR(255) NOT NULL,            -- from API: lngDescription
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_rapid_api_languages_external_id ON rapid_api_languages(external_id);

-- API 2 — Countries
CREATE TABLE IF NOT EXISTS rapid_api_countries (
    country_id      TEXT        PRIMARY KEY,          -- COU_063
    external_id     INT         NOT NULL UNIQUE,      -- from API: id
    country_code    VARCHAR(10),                      -- from API: couCode
    country_name    VARCHAR(255) NOT NULL,            -- from API: countryName
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_rapid_api_countries_external_id ON rapid_api_countries(external_id);

-- API 3 — Vehicle Types
-- `supports_vehicles_api` lets the deep-crawl phase fast-skip API 8 for types
-- where we've already proven the API returns "not supported yet" (AXLE / AFT /
-- ENG / VOEM and similar). NULL means we haven't probed it yet — the dumper
-- attempts the call once, then sets this based on the response.
CREATE TABLE IF NOT EXISTS rapid_api_vehicle_types (
    vehicle_type_id        TEXT        PRIMARY KEY,          -- VTY_001 (PC), VTY_002 (CV), ...
    external_id            INT         NOT NULL UNIQUE,      -- from API: id (1..11)
    name                   VARCHAR(100) NOT NULL,            -- from API: vehicleType ("PC", "CV", "Motorcycle"...)
    type_code              VARCHAR(20) NOT NULL UNIQUE,      -- our short code: PC, CV, MOTO, LCV, DCAB, AXLE, ENG, BUS, AFT, TRAC, VOEM
    supports_vehicles_api  BOOLEAN,                          -- NULL=unknown, TRUE=confirmed, FALSE="not supported yet" → fast-skip
    created_at             TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at             TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_rapid_api_vehicle_types_external_id ON rapid_api_vehicle_types(external_id);
CREATE INDEX IF NOT EXISTS idx_rapid_api_vehicle_types_type_code   ON rapid_api_vehicle_types(type_code);

-- ==================== MANUFACTURERS ====================
CREATE TABLE IF NOT EXISTS rapid_api_manufacturers (
    manufacturer_id     TEXT        PRIMARY KEY,      -- MFG_00001
    external_id         INT         NOT NULL UNIQUE,  -- from API: manufacturerId
    manufacturer_name   VARCHAR(255) NOT NULL,        -- from API: manufacturerName
    created_at          TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at          TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_rapid_api_manufacturers_external_id ON rapid_api_manufacturers(external_id);
CREATE INDEX IF NOT EXISTS idx_rapid_api_manufacturers_name        ON rapid_api_manufacturers(manufacturer_name);

CREATE TABLE IF NOT EXISTS rapid_api_manufacturer_vehicle_types (
    mvt_id              TEXT        PRIMARY KEY,      -- MVT_PC_00001, MVT_CV_00001, MVT_MOTO_00001, ...
    manufacturer_id     TEXT        NOT NULL REFERENCES rapid_api_manufacturers(manufacturer_id) ON DELETE CASCADE,
    vehicle_type_id     TEXT        NOT NULL REFERENCES rapid_api_vehicle_types(vehicle_type_id) ON DELETE CASCADE,
    models_fetched_at   TIMESTAMPTZ,                  -- DFS cursor: NULL = models not yet fetched for this (mfg, type)
    created_at          TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE (manufacturer_id, vehicle_type_id)
);
CREATE INDEX IF NOT EXISTS idx_rapid_api_mvt_manufacturer    ON rapid_api_manufacturer_vehicle_types(manufacturer_id);
CREATE INDEX IF NOT EXISTS idx_rapid_api_mvt_vehicle_type    ON rapid_api_manufacturer_vehicle_types(vehicle_type_id);
-- Partial index: "find next un-fetched MVT row" is O(1) thanks to this
CREATE INDEX IF NOT EXISTS idx_rapid_api_mvt_models_pending  ON rapid_api_manufacturer_vehicle_types(mvt_id)
    WHERE models_fetched_at IS NULL;

-- ==================== MODELS ====================
CREATE TABLE IF NOT EXISTS rapid_api_models (
    model_id            TEXT        PRIMARY KEY,      -- MOD_PC_000001
    external_id         INT         NOT NULL,         -- from API: modelId
    model_name          VARCHAR(500) NOT NULL,        -- from API: modelName
    manufacturer_id     TEXT        NOT NULL REFERENCES rapid_api_manufacturers(manufacturer_id) ON DELETE CASCADE,
    vehicle_type_id     TEXT        NOT NULL REFERENCES rapid_api_vehicle_types(vehicle_type_id) ON DELETE CASCADE,
    lang_id             INT         NOT NULL,
    country_filter_id   INT         NOT NULL,
    year_from           DATE,                         -- from API: modelYearFrom (nullable)
    year_to             DATE,                         -- from API: modelYearTo (nullable)
    vehicles_fetched_at  TIMESTAMPTZ,                 -- DFS cursor: NULL = vehicles not yet fetched for this model
    vehicles_api_status  VARCHAR(20),                 -- has_data | empty | not_supported | malformed | failed | NULL
    vehicles_api_message TEXT,                        -- the API's prose response when status != has_data (e.g. "not supported yet")
    created_at          TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at          TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE (external_id, manufacturer_id, vehicle_type_id, lang_id, country_filter_id)
);
CREATE INDEX IF NOT EXISTS idx_rapid_api_models_external_id          ON rapid_api_models(external_id);
CREATE INDEX IF NOT EXISTS idx_rapid_api_models_manufacturer_id      ON rapid_api_models(manufacturer_id);
CREATE INDEX IF NOT EXISTS idx_rapid_api_models_vehicle_type_id      ON rapid_api_models(vehicle_type_id);
CREATE INDEX IF NOT EXISTS idx_rapid_api_models_vehicles_pending     ON rapid_api_models(model_id)
    WHERE vehicles_fetched_at IS NULL;
CREATE INDEX IF NOT EXISTS idx_rapid_api_models_vehicles_api_status  ON rapid_api_models(vehicles_api_status);

-- ==================== VEHICLES (engine variants from API 8) ====================
CREATE TABLE IF NOT EXISTS rapid_api_vehicles (
    vehicle_id              TEXT        PRIMARY KEY,  -- VEH_PC_0000001
    external_id             INT         NOT NULL UNIQUE,  -- from API: vehicleId
    model_id                TEXT        NOT NULL REFERENCES rapid_api_models(model_id)               ON DELETE CASCADE,
    vehicle_type_id         TEXT        NOT NULL REFERENCES rapid_api_vehicle_types(vehicle_type_id) ON DELETE CASCADE,
    lang_id                 INT         NOT NULL,
    country_filter_id       INT         NOT NULL,
    manufacturer_name       VARCHAR(255),
    model_name              VARCHAR(500),
    type_engine_name        VARCHAR(255),             -- from API: typeEngineName
    construction_start      DATE,                     -- from API: constructionIntervalStart
    construction_end        DATE,                     -- from API: constructionIntervalEnd
    power_kw                NUMERIC(10, 4),           -- from API: powerKw
    power_ps                NUMERIC(10, 4),           -- from API: powerPs
    capacity_tax            VARCHAR(50),              -- from API: capacityTax
    fuel_type               VARCHAR(100),             -- from API: fuelType
    body_type               VARCHAR(100),             -- from API: bodyType
    number_of_cylinders     INT,                      -- from API: numberOfCylinders
    capacity_lt             NUMERIC(10, 4),           -- from API: capacityLt
    capacity_tech           NUMERIC(10, 4),           -- from API: capacityTech
    engine_codes            VARCHAR(255),             -- from API: engineCodes
    eng_id                  INT,                      -- from API: engId
    categories_fetched_at   TIMESTAMPTZ,              -- DFS cursor: NULL = categories not yet fetched for this vehicle
    created_at              TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at              TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_rapid_api_vehicles_external_id        ON rapid_api_vehicles(external_id);
CREATE INDEX IF NOT EXISTS idx_rapid_api_vehicles_model_id           ON rapid_api_vehicles(model_id);
CREATE INDEX IF NOT EXISTS idx_rapid_api_vehicles_vehicle_type_id    ON rapid_api_vehicles(vehicle_type_id);
CREATE INDEX IF NOT EXISTS idx_rapid_api_vehicles_eng_id             ON rapid_api_vehicles(eng_id);
CREATE INDEX IF NOT EXISTS idx_rapid_api_vehicles_categories_pending ON rapid_api_vehicles(vehicle_id)
    WHERE categories_fetched_at IS NULL;

-- ==================== CATEGORIES ====================
CREATE TABLE IF NOT EXISTS rapid_api_categories (
    category_id             TEXT        PRIMARY KEY,  -- CAT_PC_0001
    external_id             INT         NOT NULL,     -- from API: categoryId
    category_name           VARCHAR(500) NOT NULL,    -- from API: categoryName

    -- Tree linkage
    parent_category_id      TEXT        REFERENCES rapid_api_categories(category_id) ON DELETE CASCADE,
    root_category_id        TEXT        REFERENCES rapid_api_categories(category_id),
    level                   INT         NOT NULL,     -- 1 = root, increments with depth
    path                    TEXT        NOT NULL,     -- materialized breadcrumb: 'Accessories > Floor Mats'

    -- Node classification
    node_type               VARCHAR(20) NOT NULL DEFAULT 'category',  -- 'category' | 'product'
    product_external_id     INT,                                      -- TecDoc productId; non-null only when node_type = 'product'
    is_leaf                 BOOLEAN     NOT NULL DEFAULT FALSE,

    -- Display
    sort_order              INT         NOT NULL DEFAULT 0,

    -- Scope
    vehicle_type_id         TEXT        NOT NULL REFERENCES rapid_api_vehicle_types(vehicle_type_id) ON DELETE CASCADE,
    lang_id                 INT         NOT NULL,

    created_at              TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at              TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    UNIQUE (external_id, vehicle_type_id, lang_id)
);
CREATE INDEX IF NOT EXISTS idx_rapid_api_categories_external_id  ON rapid_api_categories(external_id);
CREATE INDEX IF NOT EXISTS idx_rapid_api_categories_parent       ON rapid_api_categories(parent_category_id);
CREATE INDEX IF NOT EXISTS idx_rapid_api_categories_root         ON rapid_api_categories(root_category_id);
CREATE INDEX IF NOT EXISTS idx_rapid_api_categories_vehicle_type ON rapid_api_categories(vehicle_type_id);
CREATE INDEX IF NOT EXISTS idx_rapid_api_categories_level        ON rapid_api_categories(level);
CREATE INDEX IF NOT EXISTS idx_rapid_api_categories_path         ON rapid_api_categories(path text_pattern_ops);
CREATE INDEX IF NOT EXISTS idx_rapid_api_categories_leaf         ON rapid_api_categories(is_leaf);
CREATE INDEX IF NOT EXISTS idx_rapid_api_categories_node_type    ON rapid_api_categories(node_type);
CREATE INDEX IF NOT EXISTS idx_rapid_api_categories_product_ext  ON rapid_api_categories(product_external_id) WHERE product_external_id IS NOT NULL;

-- ==================== VEHICLE-CATEGORY JUNCTION ====================
CREATE TABLE IF NOT EXISTS rapid_api_vehicle_categories (
    vca_id              TEXT        PRIMARY KEY,      -- VCA_PC_00000001
    vehicle_id          TEXT        NOT NULL REFERENCES rapid_api_vehicles(vehicle_id)    ON DELETE CASCADE,
    category_id         TEXT        NOT NULL REFERENCES rapid_api_categories(category_id) ON DELETE CASCADE,
    created_at          TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE (vehicle_id, category_id)
);
CREATE INDEX IF NOT EXISTS idx_rapid_api_vehicle_categories_vehicle  ON rapid_api_vehicle_categories(vehicle_id);
CREATE INDEX IF NOT EXISTS idx_rapid_api_vehicle_categories_category ON rapid_api_vehicle_categories(category_id);

-- ==================== DUMP JOBS (3 phase flags — DFS architecture) ====================
CREATE TABLE IF NOT EXISTS rapid_api_dump_jobs (
    job_id                   TEXT        PRIMARY KEY,  -- JOB_001
    status                   VARCHAR(20) NOT NULL DEFAULT 'idle',   -- idle|running|paused|completed|failed
    current_phase            VARCHAR(40) NOT NULL DEFAULT 'idle',   -- idle|reference|manufacturers|deep_crawl|completed|failed|paused
    started_at               TIMESTAMPTZ,
    completed_at             TIMESTAMPTZ,
    error_message            TEXT,
    stop_requested           BOOLEAN     NOT NULL DEFAULT FALSE,    -- set by CLI/API stop signal

    -- 3 phase-done flags
    reference_done           BOOLEAN     NOT NULL DEFAULT FALSE,
    manufacturers_done       BOOLEAN     NOT NULL DEFAULT FALSE,
    deep_crawl_done          BOOLEAN     NOT NULL DEFAULT FALSE,

    -- live row counts
    languages_count          INT         NOT NULL DEFAULT 0,
    countries_count          INT         NOT NULL DEFAULT 0,
    vehicle_types_count      INT         NOT NULL DEFAULT 0,
    manufacturers_count      INT         NOT NULL DEFAULT 0,
    mvt_count                INT         NOT NULL DEFAULT 0,
    models_count             INT         NOT NULL DEFAULT 0,
    vehicles_count           INT         NOT NULL DEFAULT 0,
    categories_count         INT         NOT NULL DEFAULT 0,
    vehicle_categories_count INT         NOT NULL DEFAULT 0,

    total_api_calls          INT         NOT NULL DEFAULT 0,
    created_at               TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at               TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_rapid_api_dump_jobs_status     ON rapid_api_dump_jobs(status);
CREATE INDEX IF NOT EXISTS idx_rapid_api_dump_jobs_created_at ON rapid_api_dump_jobs(created_at DESC);

-- ==================== UNPARSED ITEMS (catch-all audit table) ====================
-- Every API item that couldn't be shoehorned into the typed schema lands here.
-- We never silently skip data — if it can't be parsed it gets a row here so
-- it can be inspected (and re-processed) later.
CREATE SEQUENCE IF NOT EXISTS seq_unparsed_items START 1;

CREATE TABLE IF NOT EXISTS rapid_api_unparsed_items (
    unparsed_id   TEXT         PRIMARY KEY,    -- UNP_00000001
    api_path      TEXT         NOT NULL,       -- RapidAPI path the item came from
    entity_type   VARCHAR(50)  NOT NULL,       -- 'language' | 'country' | 'vehicle_type' | 'manufacturer' | 'model' | 'vehicle' | 'category'
    parent_ref    JSONB,                       -- trace-back context, e.g. {"model_id":"MOD_PC_000123"}
    raw_item      JSONB        NOT NULL,       -- the original item exactly as the API returned it
    reason        VARCHAR(100) NOT NULL,       -- 'non_list_response' | 'non_dict_item' | 'missing_external_id' | 'unparseable_external_id'
    created_at    TIMESTAMPTZ  NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_rapid_api_unparsed_entity   ON rapid_api_unparsed_items(entity_type);
CREATE INDEX IF NOT EXISTS idx_rapid_api_unparsed_reason   ON rapid_api_unparsed_items(reason);
CREATE INDEX IF NOT EXISTS idx_rapid_api_unparsed_created  ON rapid_api_unparsed_items(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_rapid_api_unparsed_api_path ON rapid_api_unparsed_items(api_path);

-- ==================== API KEY STATE (cooldown persistence + per-key call counts) ====================
-- success_calls / failed_calls / total_calls invariant:
--   total_calls = success_calls + failed_calls
-- Every call that actually reaches RapidAPI lands in exactly one bucket
-- (success on 200, failed on 429 / 403 / 5xx / other 4xx). Network errors
-- never reached RapidAPI so they're not counted.
CREATE TABLE IF NOT EXISTS rapid_api_api_key_state (
    key_id          VARCHAR(20) PRIMARY KEY,        -- 'KEY_1' .. 'KEY_4'
    key_value       TEXT        NOT NULL,           -- actual RapidAPI key
    cooldown_until  TIMESTAMPTZ,                    -- NULL if available; otherwise wait until this time
    last_status     INT,                            -- last HTTP status (200, 429, 403, ...)
    calls_today     INT         NOT NULL DEFAULT 0, -- legacy success-only daily bucket (kept for backwards compat)
    calls_month     INT         NOT NULL DEFAULT 0, -- legacy success-only monthly bucket (kept for backwards compat)
    success_calls   INT         NOT NULL DEFAULT 0, -- HTTP 200 responses
    failed_calls    INT         NOT NULL DEFAULT 0, -- non-200 responses (429, 403, 5xx, other 4xx)
    total_calls     INT         NOT NULL DEFAULT 0, -- success + failed
    last_used_at    TIMESTAMPTZ,
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
