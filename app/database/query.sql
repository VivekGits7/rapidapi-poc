-- Active: 1778497325951@@localhost@5432@autoparts
-- Auto Parts Catalog — full database schema
-- Run this once to reset all tables and recreate the schema.
-- Re-running this is safe: DROP TABLE IF EXISTS handles existing data.

-- ==================== DROP EVERYTHING (in dependency order) ====================
DROP TABLE IF EXISTS article_search_results CASCADE;
DROP TABLE IF EXISTS article_cross_refs CASCADE;
DROP TABLE IF EXISTS article_fitment CASCADE;
DROP TABLE IF EXISTS article_media CASCADE;
DROP TABLE IF EXISTS article_compatible_cars CASCADE;
DROP TABLE IF EXISTS article_oem_refs CASCADE;
DROP TABLE IF EXISTS article_specs CASCADE;
DROP TABLE IF EXISTS article_details CASCADE;
DROP TABLE IF EXISTS articles CASCADE;
DROP TABLE IF EXISTS vehicle_categories CASCADE;
DROP TABLE IF EXISTS engine_variants CASCADE;
DROP TABLE IF EXISTS vehicles CASCADE;
DROP TABLE IF EXISTS models CASCADE;
DROP TABLE IF EXISTS manufacturers CASCADE;
DROP TABLE IF EXISTS category_tree CASCADE;
DROP TABLE IF EXISTS vehicle_types CASCADE;
DROP TABLE IF EXISTS countries CASCADE;
DROP TABLE IF EXISTS languages CASCADE;
DROP TABLE IF EXISTS dump_jobs CASCADE;

-- ==================== DUMP JOBS ====================
CREATE TABLE dump_jobs (
    id                          SERIAL PRIMARY KEY,
    status                      VARCHAR(20)  NOT NULL DEFAULT 'idle',
    current_phase               VARCHAR(40)  NOT NULL DEFAULT 'idle',
    started_at                  TIMESTAMP,
    completed_at                TIMESTAMP,
    error_message               TEXT,
    total_api_calls             INT NOT NULL DEFAULT 0,
    budget_limit                INT NOT NULL DEFAULT 400,
    reference_done              BOOLEAN NOT NULL DEFAULT FALSE,
    manufacturers_done          BOOLEAN NOT NULL DEFAULT FALSE,
    models_done                 BOOLEAN NOT NULL DEFAULT FALSE,
    vehicles_done               BOOLEAN NOT NULL DEFAULT FALSE,
    engine_variants_done        BOOLEAN NOT NULL DEFAULT FALSE,
    categories_done             BOOLEAN NOT NULL DEFAULT FALSE,
    articles_done               BOOLEAN NOT NULL DEFAULT FALSE,
    article_details_done        BOOLEAN NOT NULL DEFAULT FALSE,
    article_media_done          BOOLEAN NOT NULL DEFAULT FALSE,
    oem_batch_done              BOOLEAN NOT NULL DEFAULT FALSE,
    fitment_done                BOOLEAN NOT NULL DEFAULT FALSE,
    cross_refs_done             BOOLEAN NOT NULL DEFAULT FALSE,
    search_done                 BOOLEAN NOT NULL DEFAULT FALSE,
    languages_count             INT NOT NULL DEFAULT 0,
    countries_count             INT NOT NULL DEFAULT 0,
    vehicle_types_count         INT NOT NULL DEFAULT 0,
    manufacturers_count         INT NOT NULL DEFAULT 0,
    models_count                INT NOT NULL DEFAULT 0,
    vehicles_count              INT NOT NULL DEFAULT 0,
    engine_variants_count       INT NOT NULL DEFAULT 0,
    vehicle_categories_count    INT NOT NULL DEFAULT 0,
    articles_count              INT NOT NULL DEFAULT 0,
    article_details_count       INT NOT NULL DEFAULT 0,
    article_media_count         INT NOT NULL DEFAULT 0,
    oem_refs_count              INT NOT NULL DEFAULT 0,
    fitment_count               INT NOT NULL DEFAULT 0,
    cross_refs_count            INT NOT NULL DEFAULT 0,
    search_count                INT NOT NULL DEFAULT 0,
    created_at                  TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at                  TIMESTAMP NOT NULL DEFAULT NOW()
);

-- ==================== REFERENCE TABLES ====================
CREATE TABLE languages (
    lng_id          VARCHAR(10) PRIMARY KEY,
    lng_iso2        VARCHAR(10),
    lng_description VARCHAR(255) NOT NULL,
    created_at      TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE countries (
    id              INT PRIMARY KEY,
    cou_code        VARCHAR(10),
    country_name    VARCHAR(255) NOT NULL,
    created_at      TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE vehicle_types (
    id              INT PRIMARY KEY,
    vehicle_type    VARCHAR(100) NOT NULL,
    created_at      TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE category_tree (
    id              INT PRIMARY KEY DEFAULT 1,
    type_id         INT NOT NULL,
    lang_id         INT NOT NULL,
    tree_data       JSONB NOT NULL,
    fetched_at      TIMESTAMP NOT NULL DEFAULT NOW()
);

-- ==================== MANUFACTURERS ====================
CREATE TABLE manufacturers (
    manufacturer_id     INT PRIMARY KEY,
    manufacturer_name   VARCHAR(255) NOT NULL,
    type_id             INT NOT NULL DEFAULT 1,
    created_at          TIMESTAMP NOT NULL DEFAULT NOW()
);

-- ==================== MODELS ====================
CREATE TABLE models (
    model_id            INT PRIMARY KEY,
    model_name          VARCHAR(255) NOT NULL,
    manufacturer_id     INT NOT NULL REFERENCES manufacturers(manufacturer_id) ON DELETE CASCADE,
    year_from           VARCHAR(20),
    year_to             VARCHAR(20),
    created_at          TIMESTAMP NOT NULL DEFAULT NOW()
);
CREATE INDEX idx_models_manufacturer_id ON models(manufacturer_id);

-- ==================== VEHICLES ====================
CREATE TABLE vehicles (
    vehicle_id          INT PRIMARY KEY,
    model_id            INT NOT NULL REFERENCES models(model_id) ON DELETE CASCADE,
    manufacturer_name   VARCHAR(255),
    model_name          VARCHAR(255),
    engine_name         VARCHAR(255),
    created_at          TIMESTAMP NOT NULL DEFAULT NOW()
);
CREATE INDEX idx_vehicles_model_id ON vehicles(model_id);

-- ==================== ENGINE VARIANTS (full details) ====================
CREATE TABLE engine_variants (
    vehicle_id              INT PRIMARY KEY REFERENCES vehicles(vehicle_id) ON DELETE CASCADE,
    manufacturer_name       VARCHAR(255),
    model_name              VARCHAR(255),
    type_engine_name        VARCHAR(255),
    construction_start      VARCHAR(50),
    construction_end        VARCHAR(50),
    power_kw                VARCHAR(20),
    power_ps                VARCHAR(20),
    fuel_type               VARCHAR(50),
    body_type               VARCHAR(100),
    number_of_cylinders     INT,
    capacity_lt             VARCHAR(20),
    capacity_tech           VARCHAR(20),
    engine_codes            VARCHAR(255),
    created_at              TIMESTAMP NOT NULL DEFAULT NOW()
);

-- ==================== VEHICLE CATEGORIES ====================
CREATE TABLE vehicle_categories (
    id              SERIAL PRIMARY KEY,
    vehicle_id      INT NOT NULL REFERENCES vehicles(vehicle_id) ON DELETE CASCADE,
    category_id     INT NOT NULL,
    category_name   VARCHAR(255),
    created_at      TIMESTAMP NOT NULL DEFAULT NOW(),
    UNIQUE (vehicle_id, category_id)
);
CREATE INDEX idx_vehicle_categories_vehicle_id ON vehicle_categories(vehicle_id);

-- ==================== ARTICLES (basic list data) ====================
CREATE TABLE articles (
    id              SERIAL PRIMARY KEY,
    article_id      INT NOT NULL,
    article_no      VARCHAR(100),
    supplier_id     INT,
    supplier_name   VARCHAR(255),
    product_name    VARCHAR(255),
    vehicle_id      INT REFERENCES vehicles(vehicle_id) ON DELETE SET NULL,
    category_id     INT,
    created_at      TIMESTAMP NOT NULL DEFAULT NOW(),
    UNIQUE (article_id, vehicle_id, category_id)
);
CREATE INDEX idx_articles_article_id  ON articles(article_id);
CREATE INDEX idx_articles_vehicle_id  ON articles(vehicle_id);
CREATE INDEX idx_articles_supplier_id ON articles(supplier_id);

-- ==================== ARTICLE DETAILS (full record) ====================
CREATE TABLE article_details (
    article_id          INT PRIMARY KEY,
    article_no          VARCHAR(100),
    article_product_name VARCHAR(255),
    supplier_id         INT,
    supplier_name       VARCHAR(255),
    ean_no              VARCHAR(255),
    s3image             TEXT,
    raw_response        JSONB,
    fetched_at          TIMESTAMP NOT NULL DEFAULT NOW()
);

-- ==================== ARTICLE SPECS ====================
CREATE TABLE article_specs (
    id              SERIAL PRIMARY KEY,
    article_id      INT NOT NULL REFERENCES article_details(article_id) ON DELETE CASCADE,
    criteria_name   VARCHAR(255),
    criteria_value  TEXT
);
CREATE INDEX idx_article_specs_article_id ON article_specs(article_id);

-- ==================== ARTICLE OEM REFERENCES ====================
CREATE TABLE article_oem_refs (
    id              SERIAL PRIMARY KEY,
    article_id      INT NOT NULL,
    oem_brand       VARCHAR(255),
    oem_display_no  VARCHAR(255),
    source          VARCHAR(30) NOT NULL DEFAULT 'details'
);
CREATE INDEX idx_article_oem_refs_article_id ON article_oem_refs(article_id);

-- ==================== ARTICLE COMPATIBLE CARS ====================
CREATE TABLE article_compatible_cars (
    id                      SERIAL PRIMARY KEY,
    article_id              INT NOT NULL,
    vehicle_id              INT,
    model_id                INT,
    manufacturer_name       VARCHAR(255),
    model_name              VARCHAR(255),
    type_engine_name        VARCHAR(255),
    construction_start      VARCHAR(50),
    construction_end        VARCHAR(50)
);
CREATE INDEX idx_article_compatible_cars_article_id ON article_compatible_cars(article_id);

-- ==================== ARTICLE MEDIA ====================
CREATE TABLE article_media (
    id                      SERIAL PRIMARY KEY,
    article_id              INT NOT NULL,
    article_media_type      VARCHAR(50),
    article_media_file_name VARCHAR(500),
    supplier_id             INT,
    media_information       VARCHAR(100),
    s3image                 TEXT
);
CREATE INDEX idx_article_media_article_id ON article_media(article_id);

-- ==================== ARTICLE FITMENT (by article_no + supplier) ====================
CREATE TABLE article_fitment (
    id                      SERIAL PRIMARY KEY,
    article_no              VARCHAR(100),
    supplier_id             INT,
    article_id              INT,
    compatible_count        INT NOT NULL DEFAULT 0,
    raw_response            JSONB,
    fetched_at              TIMESTAMP NOT NULL DEFAULT NOW()
);
CREATE INDEX idx_article_fitment_article_no ON article_fitment(article_no);

-- ==================== ARTICLE CROSS-REFERENCES ====================
CREATE TABLE article_cross_refs (
    id                      SERIAL PRIMARY KEY,
    article_id              INT NOT NULL,
    raw_response            JSONB,
    fetched_at              TIMESTAMP NOT NULL DEFAULT NOW()
);
CREATE INDEX idx_article_cross_refs_article_id ON article_cross_refs(article_id);

-- ==================== ARTICLE SEARCH RESULTS ====================
CREATE TABLE article_search_results (
    id              SERIAL PRIMARY KEY,
    search_type     VARCHAR(30) NOT NULL,
    search_no       VARCHAR(255) NOT NULL,
    results_count   INT NOT NULL DEFAULT 0,
    raw_response    JSONB,
    fetched_at      TIMESTAMP NOT NULL DEFAULT NOW()
);
CREATE INDEX idx_article_search_results_search_no ON article_search_results(search_no);
