# Auto Parts Catalog API — Manual Test Guide

Base URL: `http://localhost:8000`  
Swagger UI: `http://localhost:8000/docs`

---

## API Hierarchy — What Calls What

```
Auto Parts Catalog API
│
├── 🔵 REFERENCE DATA  (no prerequisites — call any time)
│   ├── GET /api/lookup/languages        → [lngId, lngIso2, lngDescription]
│   ├── GET /api/lookup/countries        → {countries: [{id, couCode, countryName}]}
│   └── GET /api/vehicles/types          → [{id, vehicleType}]
│                                              └── typeId ──────────────────────┐
│                                                                                ▼
├── 🟢 VEHICLE CATALOG  (sequential — each step feeds the next)                 │
│   ├── Step 1: GET /api/vehicles/makes?type_id={typeId}                        │
│   │          → {manufacturers: [{manufacturerId, manufacturerName}]}          │
│   │                              └── manufacturerId ──────────┐               │
│   │                                                           ▼               │
│   ├── Step 2: GET /api/vehicles/models?manufacturer_id={mfgId}&type_id={typeId}
│   │          → {models: [{modelId, modelName, modelYearFrom, modelYearTo}]}   │
│   │                       └── modelId ──────────┐                             │
│   │                                             ▼                             │
│   ├── Step 3a: GET /api/vehicles/engines?model_id={modelId}&type_id={typeId}  │
│   │           → {modelTypes: [{vehicleId, typeEngineName, powerKw, fuelType}]}│
│   │                            └── vehicleId ──────────────────────┐          │
│   │                                                                │          │
│   └── Step 3b: GET /api/vehicles/variants?model_id={modelId}      │          │
│               → {modelTypes: [{vehicleId}]}  (lightweight)         │          │
│                               └── vehicleId ───────────────────────┤          │
│                                                                    ▼          │
├── 🟠 CATEGORIES                                                    │          │
│   ├── GET /api/categories/?type_id={typeId}                        │          │
│   │       → full category tree  (no vehicleId needed)              │          │
│   │                                                                │          │
│   └── GET /api/categories/by-vehicle?vehicle_id={vehicleId}        │◄─────────┘
│           → vehicle-specific categories [{categoryId, categoryName}]
│                                           └── categoryId ──────────┐
│                                                                    ▼
├── 🟣 PARTS / ARTICLES  (needs vehicleId + categoryId)             │
│   ├── GET  /api/products/?vehicle_id={v}&category_id={c}          │◄──────────┘
│   │        → {articles: [{articleId, articleNo, supplierName}]}
│   │                       └── articleId ──────┐
│   │                                           ▼
│   ├── POST /api/products/details  {articleId, langId, typeId, countryFilterId}
│   │        → full specs, OEM numbers, compatible cars
│   │
│   ├── GET  /api/products/media?article_id={articleId}
│   │        → [{imageUrl, mediaType}]
│   │
│   ├── POST /api/products/oem-numbers  {articleIds: [...]}
│   │        → OEM cross-reference numbers
│   │
│   ├── GET  /api/products/fitment?article_no={no}&supplier_id={id}
│   │        → list of all vehicles this part fits
│   │
│   └── GET  /api/products/cross-references?article_id={articleId}
│            → equivalent parts from other suppliers
│
├── 🔍 SEARCH  (standalone — no prerequisites)
│   ├── GET /api/search/by-article-no?article_no={no}
│   │       → articles matching supplier part number
│   │
│   └── GET /api/search/by-oem-no?oem_no={no}
│           → aftermarket parts matching OEM number
│
└── 🔴 VIN  (standalone — no prerequisites)
    └── GET /api/vin/decode/{vin}
            → vin-data-1: {manufacturer, region, modelYear}
            → vin-data-2: {make, model, trim, engine, fuelType}
            → vin-data-3: [{manufacturer address}]
```

---

### Key IDs to Use for Testing

| Step | Example ID | What It Represents |
|------|------------|-------------------|
| `typeId` | `1` | Passenger Car |
| `manufacturerId` | `111` | Toyota |
| `modelId` | `5626` | Toyota Corolla E11 |
| `vehicleId` | `19942` | Toyota Corolla 1.4 (EE111) |
| `categoryId` | `100260` | Oil Filter |
| `articleId` | `125` | MANN-FILTER OC 607 |
| `supplierId` | `4` | MANN-FILTER |
| `langId` | `4` | English (GB) |
| `countryFilterId` | `63` | Germany |

---

## 1. Reference Data

### GET /api/lookup/languages
No parameters required.

**Expected response:**
```json
{
  "success": true,
  "message": "Fetched 52 languages",
  "data": [
    { "lngId": "4", "lngIso2": "en", "lngDescription": "English (GB)" },
    { "lngId": "37", "lngIso2": "qa", "lngDescription": "English (USA)" }
  ]
}
```
**What to verify:** List is not empty. `lngId: "4"` (English GB) and `lngId: "37"` (English USA) are present.

---

### GET /api/lookup/countries
No parameters required.

**Expected response:**
```json
{
  "success": true,
  "message": "Fetched N countries",
  "data": {
    "countries": [
      { "id": 63, "couCode": "D", "countryName": "Germany" },
      { "id": 261, "couCode": "USA", "countryName": "United States" }
    ]
  }
}
```
**What to verify:** `id: 63` (Germany) is present — this is the default country used in all catalog calls.

---

## 2. Vehicle Catalog

> These endpoints must be called in order: **types → makes → models → engines/variants**

### GET /api/vehicles/types
No parameters required.

**Expected response:**
```json
{
  "success": true,
  "message": "Fetched 11 vehicle types",
  "data": [
    { "id": 1, "vehicleType": "PC" },
    { "id": 2, "vehicleType": "CV" },
    { "id": 3, "vehicleType": "Motorcycle" }
  ]
}
```
**What to verify:** `id: 1` (PC = Passenger Car) is present. Total should be 11 types.

---

### GET /api/vehicles/makes?type_id=1
| Parameter | Value | Notes |
|-----------|-------|-------|
| `type_id` | `1` | 1 = Passenger Car |

**Expected response:**
```json
{
  "success": true,
  "message": "Fetched 698 manufacturers",
  "data": {
    "countManufactures": 698,
    "manufacturers": [
      { "manufacturerId": 16, "manufacturerName": "BMW" },
      { "manufacturerId": 111, "manufacturerName": "TOYOTA" },
      { "manufacturerId": 74, "manufacturerName": "MERCEDES-BENZ" }
    ]
  }
}
```
**What to verify:** Count > 0. BMW (`id: 16`), Toyota (`id: 111`), Mercedes (`id: 74`) are present.

---

### GET /api/vehicles/models?manufacturer_id=111&type_id=1
| Parameter | Value | Notes |
|-----------|-------|-------|
| `manufacturer_id` | `111` | Toyota |
| `type_id` | `1` | Passenger Car |

**Expected response:**
```json
{
  "success": true,
  "message": "Fetched N models",
  "data": {
    "countModels": 42,
    "models": [
      { "modelId": 5626, "modelName": "COROLLA (_E11_)", "modelYearFrom": "1997-01-01", "modelYearTo": "2002-01-01" }
    ]
  }
}
```
**What to verify:** Models list is not empty. Each item has `modelId`, `modelName`, `modelYearFrom`.

---

### GET /api/vehicles/engines?model_id=5626&type_id=1
| Parameter | Value | Notes |
|-----------|-------|-------|
| `model_id` | `5626` | Toyota Corolla E11 |
| `type_id` | `1` | Passenger Car |

**Expected response:**
```json
{
  "success": true,
  "message": "Fetched N engine variants",
  "data": {
    "countModelTypes": 12,
    "modelTypes": [
      {
        "vehicleId": 19942,
        "typeEngineName": "1.4 (EE111_)",
        "powerKw": 66,
        "powerPs": 90,
        "fuelType": "Petrol",
        "constructionIntervalStart": "1997-04-01",
        "constructionIntervalEnd": "2002-01-01"
      }
    ]
  }
}
```
**What to verify:** Each item has a `vehicleId` — this is the key ID used for all parts lookups.

---

### GET /api/vehicles/variants?model_id=5626&type_id=1
Same as `/engines` but lightweight — only returns `vehicleId` values without full specs.

**What to verify:** Response is faster. Each item has `vehicleId`.

---

## 3. Categories

### GET /api/categories/?type_id=1
| Parameter | Value | Notes |
|-----------|-------|-------|
| `type_id` | `1` | Passenger Car |

**Expected response:** Full category tree (nested hierarchy of part categories).

**What to verify:** Response is a list/tree. Top-level categories include items like "Engine", "Brakes", "Suspension".

---

### GET /api/categories/by-vehicle?vehicle_id=19942&type_id=1
| Parameter | Value | Notes |
|-----------|-------|-------|
| `vehicle_id` | `19942` | Toyota Corolla 1.4 |
| `type_id` | `1` | Passenger Car |

**Expected response:**
```json
{
  "success": true,
  "message": "Fetched N category rows for vehicle 19942",
  "data": {
    "categories": [
      { "categoryId1": 1, "categoryName1": "Engine", "categoryId2": 100260, "categoryName2": "Oil Filter" }
    ]
  }
}
```
**What to verify:** Only shows categories that have parts for this specific vehicle. Count should be less than the full tree.

---

## 4. Parts / Articles

> Use `vehicle_id: 19942` (Toyota Corolla 1.4) and `category_id: 100260` (Oil Filter) for all tests below.

### GET /api/products/?vehicle_id=19942&category_id=100260
| Parameter | Value |
|-----------|-------|
| `vehicle_id` | `19942` |
| `category_id` | `100260` |

**Expected response:**
```json
{
  "success": true,
  "message": "Fetched N articles",
  "data": {
    "countArticles": 15,
    "articles": [
      { "articleId": 125, "articleNo": "OC 607", "supplierName": "MANN-FILTER", "s3image": "https://..." }
    ]
  }
}
```
**What to verify:** List not empty. Each item has `articleId` and `articleNo`.

---

### POST /api/products/details
**Request body:**
```json
{
  "articleId": 125,
  "langId": 4,
  "typeId": 1,
  "countryFilterId": 63
}
```
**Expected response:** Full article record with `allSpecifications`, `eanNo`, OEM cross-references, compatible cars list.

**What to verify:** `allSpecifications` is a list. `compatibleCars` is not empty.

---

### GET /api/products/media?article_id=125
| Parameter | Value |
|-----------|-------|
| `article_id` | `125` |

**Expected response:**
```json
{
  "success": true,
  "message": "Fetched N media items",
  "data": [
    { "articleMediaType": "JPG", "imageUrl": "https://..." }
  ]
}
```
**What to verify:** At least one image URL is returned.

---

### POST /api/products/oem-numbers
**Request body:**
```json
{
  "articleIds": [125, 131540]
}
```
**Expected response:** OEM cross-reference numbers for each article.

**What to verify:** Response contains entries for each articleId submitted.

---

### GET /api/products/fitment?article_no=OC 607&supplier_id=4
| Parameter | Value | Notes |
|-----------|-------|-------|
| `article_no` | `OC 607` | MANN-FILTER oil filter |
| `supplier_id` | `4` | MANN-FILTER supplier ID |

**Expected response:** List of all vehicles this part fits.

**What to verify:** `compatibleCars` list is not empty. Contains Toyota models.

---

### GET /api/products/cross-references?article_id=131540
| Parameter | Value |
|-----------|-------|
| `article_id` | `131540` |

**Expected response:** Equivalent parts from other suppliers for the same function.

**What to verify:** Multiple suppliers listed for the same product type.

---

## 5. Search

### GET /api/search/by-article-no?article_no=OC 607
| Parameter | Value |
|-----------|-------|
| `article_no` | `OC 607` |

**Expected response:**
```json
{
  "success": true,
  "message": "Found N articles",
  "data": {
    "countArticles": 1,
    "articles": [{ "articleId": 125, "articleNo": "OC 607", "supplierName": "MANN-FILTER" }]
  }
}
```
**What to verify:** Returns the MANN-FILTER OC 607 oil filter. `articleId` matches what we got from `/products/`.

---

### GET /api/search/by-oem-no?oem_no=8F0 513 035 N
| Parameter | Value |
|-----------|-------|
| `oem_no` | `8F0 513 035 N` |

**Expected response:** Aftermarket parts that cross-reference this OEM number.

**What to verify:** Multiple suppliers returned for the same OEM number.

---

## 6. VIN

### GET /api/vin/decode/WDBFA68F42F202731
No query parameters.

**Expected response:**
```json
{
  "success": true,
  "message": "VIN decoded successfully",
  "data": {
    "tecdoc": {
      "vin-data-1": { "vin": "WDBFA68F42F202731", "manufacturer": "Mercedes-Benz", "modelYear": [2002] },
      "vin-data-2": { "make": "MERCEDES-BENZ", "model": "SL-Class", "trim": "SL500", "fuelType": "Gasoline" },
      "vin-data-3": [{ "title": "Manufacturer", "information": { "Manufacturer": "Daimler AG" } }]
    },
    "nhtsa": null
  }
}
```
**What to verify:**
- `vin-data-1` has `manufacturer` and `modelYear`
- `vin-data-2` has `make`, `model`, `trim`
- `nhtsa` is `null` (NHTSA fallback was removed — expected)

---

## Common IDs Reference

| Thing | ID | Name |
|-------|----|------|
| Language | `4` | English (GB) |
| Language | `37` | English (USA) |
| Language | `42` | Arabic |
| Country | `63` | Germany (default) |
| Country | `261` | USA |
| Vehicle Type | `1` | Passenger Car (PC) |
| Vehicle Type | `2` | Commercial Vehicle (CV) |
| Manufacturer | `16` | BMW |
| Manufacturer | `74` | Mercedes-Benz |
| Manufacturer | `111` | Toyota |
| Model | `5626` | Toyota Corolla E11 (1997–2002) |
| Vehicle | `19942` | Toyota Corolla 1.4 (EE111) |
| Category | `100260` | Oil Filter |
| Supplier | `4` | MANN-FILTER |
| Article | `125` | MANN-FILTER OC 607 (Oil Filter) |
