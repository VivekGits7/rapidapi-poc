-- ============================================================
-- Auto Parts Catalog POC — Demo Walkthrough
-- ============================================================
-- DB: autoparts  (user: autoparts)
-- Run sections in order, top to bottom.
--
-- Sections:
--   1. POC Health Check     — verify every table has data (run first)
--   2. Full Hierarchy Tree  — one query showing all data at once
--   3. Drill-Down Walkthrough — step-by-step (replace <PLACEHOLDERS>)
--   4. Finale: 7-table JOIN — the "wow" query
-- ============================================================


-- ============================================================
-- SECTION 1 — POC HEALTH CHECK
-- ============================================================
-- One query, shows every table + row count + OK/EMPTY status.
-- If every row says OK, the POC is successful — all 17 RapidAPI
-- endpoints captured their data into PostgreSQL.

SELECT 'languages'              AS table_name, COUNT(*) AS rows, CASE WHEN COUNT(*)>0 THEN 'OK' ELSE 'EMPTY' END AS status FROM languages
UNION ALL SELECT 'countries',               COUNT(*), CASE WHEN COUNT(*)>0 THEN 'OK' ELSE 'EMPTY' END FROM countries
UNION ALL SELECT 'vehicle_types',           COUNT(*), CASE WHEN COUNT(*)>0 THEN 'OK' ELSE 'EMPTY' END FROM vehicle_types
UNION ALL SELECT 'category_tree',           COUNT(*), CASE WHEN COUNT(*)>0 THEN 'OK' ELSE 'EMPTY' END FROM category_tree
UNION ALL SELECT 'manufacturers',           COUNT(*), CASE WHEN COUNT(*)>0 THEN 'OK' ELSE 'EMPTY' END FROM manufacturers
UNION ALL SELECT 'models',                  COUNT(*), CASE WHEN COUNT(*)>0 THEN 'OK' ELSE 'EMPTY' END FROM models
UNION ALL SELECT 'vehicles',                COUNT(*), CASE WHEN COUNT(*)>0 THEN 'OK' ELSE 'EMPTY' END FROM vehicles
UNION ALL SELECT 'engine_variants',         COUNT(*), CASE WHEN COUNT(*)>0 THEN 'OK' ELSE 'EMPTY' END FROM engine_variants
UNION ALL SELECT 'vehicle_categories',      COUNT(*), CASE WHEN COUNT(*)>0 THEN 'OK' ELSE 'EMPTY' END FROM vehicle_categories
UNION ALL SELECT 'articles',                COUNT(*), CASE WHEN COUNT(*)>0 THEN 'OK' ELSE 'EMPTY' END FROM articles
UNION ALL SELECT 'article_details',         COUNT(*), CASE WHEN COUNT(*)>0 THEN 'OK' ELSE 'EMPTY' END FROM article_details
UNION ALL SELECT 'article_specs',           COUNT(*), CASE WHEN COUNT(*)>0 THEN 'OK' ELSE 'EMPTY' END FROM article_specs
UNION ALL SELECT 'article_oem_refs',        COUNT(*), CASE WHEN COUNT(*)>0 THEN 'OK' ELSE 'EMPTY' END FROM article_oem_refs
UNION ALL SELECT 'article_compatible_cars', COUNT(*), CASE WHEN COUNT(*)>0 THEN 'OK' ELSE 'EMPTY' END FROM article_compatible_cars
UNION ALL SELECT 'article_media',           COUNT(*), CASE WHEN COUNT(*)>0 THEN 'OK' ELSE 'EMPTY' END FROM article_media
UNION ALL SELECT 'article_fitment',         COUNT(*), CASE WHEN COUNT(*)>0 THEN 'OK' ELSE 'EMPTY' END FROM article_fitment
UNION ALL SELECT 'article_cross_refs',      COUNT(*), CASE WHEN COUNT(*)>0 THEN 'OK' ELSE 'EMPTY' END FROM article_cross_refs
UNION ALL SELECT 'article_search_results',  COUNT(*), CASE WHEN COUNT(*)>0 THEN 'OK' ELSE 'EMPTY' END FROM article_search_results
UNION ALL SELECT 'dump_jobs',               COUNT(*), CASE WHEN COUNT(*)>0 THEN 'OK' ELSE 'EMPTY' END FROM dump_jobs
ORDER BY table_name;


-- ============================================================
-- SECTION 2 — FULL HIERARCHY TREE (no IDs needed)
-- ============================================================
-- Single query, runs in one shot. Shows the entire catalog as
-- a flat table — but ORDER BY makes the hierarchy visible.
-- Use this as your "everything at a glance" slide.
-- Columns:  brand -> model -> years -> engine -> part_category -> part_no -> supplier

SELECT
    m.manufacturer_name                                                 AS brand,
    mo.model_name                                                       AS model,
    COALESCE(mo.year_from, '?') || ' - ' || COALESCE(mo.year_to, 'now') AS years,
    v.engine_name                                                       AS engine,
    vc.category_name                                                    AS part_category,
    a.article_no                                                        AS part_no,
    a.supplier_name                                                     AS supplier
FROM manufacturers m
LEFT JOIN models             mo ON mo.manufacturer_id = m.manufacturer_id
LEFT JOIN vehicles           v  ON v.model_id         = mo.model_id
LEFT JOIN vehicle_categories vc ON vc.vehicle_id      = v.vehicle_id
LEFT JOIN articles           a  ON a.vehicle_id       = v.vehicle_id
                              AND a.category_id      = vc.category_id
ORDER BY 1, 2, 4, 5, 6;


-- ============================================================
-- SECTION 3 — STEP-BY-STEP DRILL-DOWN
-- ============================================================
-- Walk through each level live. Each step reveals IDs you paste
-- into the NEXT step (look for >>> markers).


-- ----------- Step 1: Vehicle Types -----------
SELECT id, vehicle_type FROM vehicle_types ORDER BY id;
-- TALKING POINT: id=1 is Passenger Car — that's what our POC dumped.


-- ----------- Step 2: Manufacturers (brands) -----------
SELECT manufacturer_id, manufacturer_name FROM manufacturers ORDER BY manufacturer_id;
-- TALKING POINT: 3 brands in our sample (cap = DUMP_MAX_MANUFACTURERS in config.py).
-- >>> COPY a manufacturer_id from results. Paste into <MFG_ID> below.


-- ----------- Step 3: Models under that brand -----------
-- >>> Replace <MFG_ID> with the manufacturer_id from Step 2.
SELECT model_id, model_name, year_from, year_to
FROM models
WHERE manufacturer_id = <MFG_ID>;
-- TALKING POINT: each row is one production-era model.
-- >>> COPY a model_id. Paste into <MODEL_ID> below.


-- ----------- Step 4: Engine variants for that model -----------
-- >>> Replace <MODEL_ID> with the model_id from Step 3.
SELECT
    v.vehicle_id,
    v.engine_name,
    ev.power_kw,
    ev.power_ps,
    ev.fuel_type,
    ev.capacity_lt,
    ev.number_of_cylinders,
    ev.construction_start,
    ev.construction_end
FROM vehicles v
LEFT JOIN engine_variants ev ON ev.vehicle_id = v.vehicle_id
WHERE v.model_id = <MODEL_ID>;
-- TALKING POINT: vehicle_id is THE key for everything below.
-- >>> COPY a vehicle_id. Paste into <VEHICLE_ID> below.


-- ----------- Step 5: Categories that have parts for that engine -----------
-- >>> Replace <VEHICLE_ID> with the vehicle_id from Step 4.
SELECT category_id, category_name
FROM vehicle_categories
WHERE vehicle_id = <VEHICLE_ID>;
-- TALKING POINT: full catalog has 1000+ categories — this table stores
--                only categories that actually have parts for this engine.
-- >>> COPY a category_id. Paste into <CATEGORY_ID> below.


-- ----------- Step 6: Real parts for that vehicle + category -----------
-- >>> Replace <VEHICLE_ID> and <CATEGORY_ID> with values from Steps 4 & 5.
SELECT article_id, article_no, supplier_name, product_name
FROM articles
WHERE vehicle_id = <VEHICLE_ID> AND category_id = <CATEGORY_ID>;
-- TALKING POINT: actual part numbers from real suppliers (MANN, Bosch, etc).
-- >>> COPY an article_id. Paste into <ARTICLE_ID> below.
-- >>> ALSO note the article_no (the text part number). Paste into <ARTICLE_NO> in Step 7g.


-- ----------- Step 7a: Master record for one part -----------
-- >>> Replace <ARTICLE_ID> with the article_id from Step 6.
SELECT article_id, article_no, supplier_name, ean_no, s3image
FROM article_details
WHERE article_id = <ARTICLE_ID>;
-- TALKING POINT: EAN barcode + hosted product image URL.


-- ----------- Step 7b: Specifications -----------
SELECT criteria_name, criteria_value
FROM article_specs
WHERE article_id = <ARTICLE_ID>;
-- TALKING POINT: free-form key/value spec sheet (diameter, weight, thread, etc).


-- ----------- Step 7c: OEM cross-references -----------
SELECT oem_brand, oem_display_no, source
FROM article_oem_refs
WHERE article_id = <ARTICLE_ID>;
-- TALKING POINT: aftermarket part to OEM part-number mapping.


-- ----------- Step 7d: Every vehicle this part fits -----------
SELECT manufacturer_name, model_name, type_engine_name,
       construction_start, construction_end
FROM article_compatible_cars
WHERE article_id = <ARTICLE_ID>;
-- TALKING POINT: same physical part fits multiple cars across brands.


-- ----------- Step 7e: Product photos -----------
SELECT article_media_type, s3image
FROM article_media
WHERE article_id = <ARTICLE_ID>;
-- TALKING POINT: images / drawings — open one s3image URL in browser.


-- ----------- Step 7f: Global fitment count -----------
SELECT article_no, supplier_id, compatible_count
FROM article_fitment
WHERE article_id = <ARTICLE_ID>;
-- TALKING POINT: how many vehicles this part fits globally.


-- ----------- Step 7g: Cached search results -----------
-- >>> Replace <ARTICLE_NO> (keep the quotes!) with the article_no from Step 6.
SELECT search_type, search_no, results_count, fetched_at
FROM article_search_results
WHERE search_no = '<ARTICLE_NO>';
-- TALKING POINT: search index — customer types part number → we serve from DB,
--                no RapidAPI call.


-- ============================================================
-- SECTION 4 — FINALE: ONE QUERY, END-TO-END
-- ============================================================
-- 7-table JOIN: brand -> model -> year -> engine -> HP -> fuel
--             -> category -> part_no -> supplier -> image_url
-- This single query is the foundation of any parts e-commerce page.

SELECT
    m.manufacturer_name                                AS brand,
    mo.model_name                                      AS model,
    mo.year_from || ' - ' || COALESCE(mo.year_to, 'now') AS years,
    v.engine_name                                      AS engine,
    ev.power_ps                                        AS hp,
    ev.fuel_type                                       AS fuel,
    vc.category_name                                   AS part_category,
    a.article_no                                       AS part_no,
    a.supplier_name                                    AS supplier,
    ad.s3image                                         AS image_url
FROM articles a
JOIN article_details     ad ON ad.article_id      = a.article_id
JOIN vehicles            v  ON v.vehicle_id       = a.vehicle_id
JOIN engine_variants     ev ON ev.vehicle_id      = v.vehicle_id
JOIN models              mo ON mo.model_id        = v.model_id
JOIN manufacturers       m  ON m.manufacturer_id  = mo.manufacturer_id
JOIN vehicle_categories  vc ON vc.vehicle_id      = a.vehicle_id
                          AND vc.category_id     = a.category_id
ORDER BY m.manufacturer_name, mo.model_name;
