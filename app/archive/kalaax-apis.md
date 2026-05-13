# Kalaax — TecDoc API Usage Plan

> Cross-references `API_DOCS.md` (TecDoc endpoints) with `Kalaax_Backend_Development_Guide.md` (what the platform actually needs).

---

## How TecDoc APIs Are Used in Kalaax

TecDoc APIs are called in **two distinct ways**:

| Mode | When | Who calls it |
|------|------|-------------|
| **Nightly Sync** | 2 AM Cairo, Celery task | Populates `vehicles`, `products`, `categories`, `product_vehicle_fitment` tables in PostgreSQL + Elasticsearch index |
| **Live / Fallback** | Real-time per request | For data not yet synced (VIN decode, fresh OEM lookups) |

Most TecDoc data flows through the sync. Elasticsearch handles search. Live TecDoc calls are the exception, not the rule.

---

## Which APIs Are Needed

### GROUP 1 — Nightly Sync (Celery Task)

These power the sync task that builds the local DB. Called in batches of 100. Upsert on `tecdoc_id`.

| # | API | Populates Table | Notes |
|---|-----|-----------------|-------|
| #5 | GET Vehicle Types | `vehicles` (type filter) | Entry point for type-based pagination |
| #6 | GET Manufacturer IDs by Type | `vehicles.make` | All brands per type |
| #7 | GET Manufacturer Info by ID | `vehicles.make` | Brand name |
| #8 | GET Models by Type & Manufacturer | `vehicles.model` | All models per brand |
| #14 | GET Vehicle IDs by Model ID | `vehicles.tecdoc_id` | Exact variant IDs — core vehicle records |
| #12 | GET Engine Types by Model | `vehicles.engine` | Engine/fuel variants |
| #27 | GET List All Categories | `categories` | Full category tree |
| #28 | GET Categories by Vehicle ID | `categories` (vehicle-specific) | Which categories have parts for a vehicle |
| #41 | GET Article List by Vehicle + Category | `products`, `product_vehicle_fitment` | Core parts data per vehicle+category |
| #36 | POST Article Details by Article ID | `products` (full detail) | Specs, OEM numbers, descriptions |
| #48 | GET Article Media | `products.images` (→ S3 sync) | Images fetched → stored in S3 `media_files/images/` |
| #26 | POST Get OEM by Article ID | `products.oem_numbers` | OEM numbers JSONB field |
| #43 | GET Compatible Vehicles by Article No | `product_vehicle_fitment` | Which vehicles each part fits |

**Total sync APIs: 13**

---

### GROUP 2 — Live API Calls (Real-Time)

Called per request for features that can't rely on sync alone.

| # | API | Kalaax Endpoint | Notes |
|---|-----|-----------------|-------|
| #19 | GET Search Articles by Article No | `GET /search` (part number lookup) | When buyer types a part number directly |
| #20 | GET Search Articles by OEM No | `GET /products/oem-crossref` | OEM cross-reference search |
| #50 | GET Cross-References by Article ID | `GET /products/{id}` (product detail) | "Also available from these brands" |
| #56–60 | VIN Decoder | `POST /vehicles/vin-lookup` | POC requirement P0 Day 1. Try TecDoc first, fallback to NHTSA free API |

**Total live APIs: 4 (+ NHTSA as free VIN fallback)**

---

### GROUP 3 — Useful but Optional

Add after core flows work.

| # | API | Feature |
|---|-----|---------|
| #39 | GET Article Criteria | Specs table on product page (`products.specifications`) |
| #13 | GET Engine Details | Richer engine info during vehicle selection |
| #25 | GET List All Suppliers | Brand filter in search |
| #51 | GET Equivalent OEM Numbers | Deeper OEM chain lookup |

---

### Not Needed

| # | API | Reason |
|---|-----|--------|
| #1–4 | Languages / Countries | One-time setup only — hardcode `langId=4`, `countryId=1` |
| #15 | KBA Number | Germany only |
| #16 | License Plate | Netherlands only |
| #9, #10 | Model/Vehicle Details | Covered by #8 + #14 |
| #11 | Model Image | Low value for v1 |
| #61–68 | Enhanced `*`/`**` Search | Higher RapidAPI tier cost — Elasticsearch covers search |
| #29, #30 | Categories v2/v3 | #28 is sufficient |
| #42 | POST Article List | #41 GET is sufficient |
| #49 | POST Article Media | #48 GET is sufficient |
| #52–55 | Deep OEM Chain | #50 covers the main case |
| #21–23 | EAN / IAM / Trade No Search | Edge cases, not primary paths |

---

## POC Scope (Minimal Viable Loop)

From the backend guide POC checklist (P0 items). Goal: prove the loop works end-to-end.

> **pick vehicle → browse parts → view product detail**

| # | API | Purpose |
|---|-----|---------|
| #5 | GET Vehicle Types | Selector start |
| #6 | GET Manufacturer IDs by Type | Brand list |
| #8 | GET Models by Type & Manufacturer | Model list |
| #14 | GET Vehicle IDs by Model ID | Exact vehicle variant |
| #28 | GET Categories by Vehicle ID | Part categories for vehicle |
| #41 | GET Article List by Vehicle + Category | Product listing |
| #36 | POST Article Details by Article ID | Product detail page |
| #48 | GET Article Media | Product images |
| #19 | GET Search Articles by Article No | Part number search |
| #56–60 | VIN Decoder | POC requirement — P0 Day 1 per backend guide |

**POC total: 10 APIs**

For POC: hardcode `langId=4`, skip engine step, skip cross-refs and OEM. Just prove the loop.

---

## VIN Decode Strategy

Per Section 4.2 of backend guide:
1. Try TecDoc VIN endpoint (#56–60) first
2. If TecDoc returns no result → fallback to **NHTSA free API** (`vpic.nhtsa.dot.gov`)
3. Map result to a `vehicles.tecdoc_id` in our DB

---

## Summary

| Group | APIs | When |
|-------|------|------|
| Nightly Sync (Celery) | 13 | Every night 2 AM Cairo |
| Live / Fallback | 4 | Per request |
| Optional (later) | 4 | After core works |
| Not Needed | ~17 | Skip |
| **Total needed** | **17** | |
