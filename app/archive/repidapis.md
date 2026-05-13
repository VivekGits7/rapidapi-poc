# API Documentation

> Add each API below using the template. One section per API endpoint.

---

## Table of Contents

- [Template](#template)
- [APIs](#apis)
  1. [GET  Languages](#1-get-languages)
  2. [GET  Countries](#2-get-countries)
  3. [GET  Language Info by ID](#3-get-language-info-by-id)
  4. [GET  Countries by Language ID](#4-get-countries-by-language-id)
- **Manufacturer**
  5. [GET  Vehicle Types](#5-get-vehicle-types)
  6. [GET  Manufacturer IDs by Type ID](#6-get-manufacturer-ids-by-type-id)
  7. [GET  Manufacturer Info by ID](#7-get-manufacturer-info-by-id)
  8. [GET  Models by Type & Manufacturer](#8-get-models-by-type--manufacturer)
  9. [GET  Model Details by Model ID](#9-get-model-details-by-model-id)
  10. [GET  Model Details by Vehicle ID](#10-get-model-details-by-vehicle-id)
  11. [GET  Model Image by Model ID](#11-get-model-image-by-model-id)
  12. [GET  Engine Types by Model](#12-get-engine-types-by-model)
  13. [GET  Engine Details](#13-get-engine-details)
  14. [GET  Vehicle IDs by Model ID](#14-get-vehicle-ids-by-model-id)
  15. [GET  Vehicles by KBA Number (Germany)](#15-get-vehicles-by-kba-number-germany)
  16. [GET  Vehicles by License Plate (Netherlands / Kenteken)](#16-get-vehicles-by-license-plate-netherlands--kenteken)
  17. [GET  Part Criteria for Vehicle](#17-get-part-criteria-for-vehicle)
  18. [GET  TypeId by VehicleId and ManufacturerId](#18-get-typeid-by-vehicleid-and-manufacturerid)
  19. [GET  Search Articles by Article No](#19-get-search-articles-by-article-no)
  20. [GET  Search Articles by OEM No](#20-get-search-articles-by-oem-no)
  21. [GET  Search Articles by EAN No](#21-get-search-articles-by-ean-no)
  22. [GET  Search Articles by IAM No](#22-get-search-articles-by-iam-no)
  23. [GET  Search Articles by Trade No](#23-get-search-articles-by-trade-no)
  24. [POST  Article Details by Article No](#24-post-article-details-by-article-no)
  25. [GET  List All Suppliers](#25-get-list-all-suppliers)
  26. [POST  Get OEM by Article ID](#26-post-get-oem-by-article-id)
- **Part Info (by Article ID)**
  27. [GET  List All Categories](#27-get-list-all-categories)
  28. [GET  List Categories by Vehicle ID (v1)](#28-get-list-categories-by-vehicle-id-v1)
  29. [GET  List Categories by Vehicle ID (v2)](#29-get-list-categories-by-vehicle-id-v2)
  30. [GET  List Categories by Vehicle ID (v3)](#30-get-list-categories-by-vehicle-id-v3)
  31. [GET  List Main Category by Article ID](#31-get-list-main-category-by-article-id)
  32. [GET  List Categories by Article ID](#32-get-list-categories-by-article-id)
  33. [GET  Search (sub)Categories by Text](#33-get-search-subcategories-by-text)
  34. [GET  List All Product Names](#34-get-list-all-product-names)
  35. [GET  Article Details by Article ID](#35-get-article-details-by-article-id)
  36. [POST  Article Details by Article ID (Complete)](#36-post-article-details-by-article-id-complete)
  37. [GET  Article Details & Compatibility by Article ID](#37-get-article-details--compatibility-by-article-id)
  38. [POST  Article Details by Article ID & Language ID](#38-post-article-details-by-article-id--language-id)
  39. [GET  Article Criteria](#39-get-article-criteria)
  40. [POST  Article Specifications by Article IDs](#40-post-article-specifications-by-article-ids)
  41. [GET  Article List by Vehicle ID & Category ID](#41-get-article-list-by-vehicle-id--category-id)
  42. [POST  Article List by Vehicle ID & Category ID](#42-post-article-list-by-vehicle-id--category-id)
  43. [GET  Compatible Vehicles by Article No & Supplier ID](#43-get-compatible-vehicles-by-article-no--supplier-id)
  44. [GET  List Accessory Parts by Article ID](#44-get-list-accessory-parts-by-article-id)
  45. [GET  Vehicle Spare Part Criteria](#45-get-vehicle-spare-part-criteria)
  46. [GET  Parts Diagram Coordinates](#46-get-parts-diagram-coordinates)
  47. [GET  List of Parts for Article ID](#47-get-list-of-parts-for-article-id)
  48. [GET  Article Media](#48-get-article-media)
  49. [POST  Article Media](#49-post-article-media)
- **Parts Cross Reference**
  50. [GET  Cross-References by Article ID](#50-get-cross-references-by-article-id)
  51. [GET  Equivalent OEM Numbers](#51-get-equivalent-oem-numbers)
  52. [GET  Parts Cross-Reference by Article No](#52-get-parts-cross-reference-by-article-no)
  53. [GET  Cross-References through OEM Numbers by Article ID](#53-get-cross-references-through-oem-numbers-by-article-id)
  54. [POST  Equivalent OEM Numbers](#54-post-equivalent-oem-numbers)
  55. [GET  Cross-References via OEM Number by Article ID](#55-get-cross-references-via-oem-number-by-article-id)
- **VIN**
  56. [GET  VIN Check](#56-get-vin-check)
  57. [GET  VIN Decoder (v1)](#57-get-vin-decoder-v1)
  58. [GET  VIN Decoder (v2)](#58-get-vin-decoder-v2)
  59. [GET  VIN Decoder (v3)](#59-get-vin-decoder-v3)
  60. [GET  VIN Decoder (all-in-one)](#60-get-vin-decoder-all-in-one)
- **Enhanced Article Search**
  61. [GET  * Compatible Vehicles by Article No](#61-get--compatible-vehicles-by-article-no)
  62. [GET  * Analog Spare Parts by Article No](#62-get--analog-spare-parts-by-article-no)
  63. [GET  * Analog Spare Parts by OEM](#63-get--analog-spare-parts-by-oem)
  64. [GET  * Search Articles by Article No ⚠️ DEPRECATED](#64-get--search-articles-by-article-no)
  65. [GET  * OEM/OEM Cross-Reference through Aftermarket Parts](#65-get--oemoemcross-reference-through-aftermarket-parts)
  66. [GET  ** Search Articles by OEM](#66-get--search-articles-by-oem)
  67. [POST  ** Search Articles by OEM](#67-post--search-articles-by-oem)
  68. [GET  ** Search Articles by Article No](#68-get--search-articles-by-article-no)
  69. [GET  * OEM Parts by Vehicle ID](#69-get--oem-parts-by-vehicle-id)
  70. [GET  * List Vehicles by OEM](#70-get--list-vehicles-by-oem)
  71. [GET  * Article Details by Article No](#71-get--article-details-by-article-no)
  72. [GET  * Cross-References by Article No](#72-get--cross-references-by-article-no)

---

## Template

Copy this block for each new API:

```
### [METHOD] /path/to/endpoint

**Description:** What this endpoint does.

**Auth Required:** Yes / No

**Request**

- Method: GET / POST / PUT / PATCH / DELETE
- URL: `https://api.example.com/path`
- Headers:
  - `Authorization: Bearer <token>`
  - `Content-Type: application/json`

**Query Params**

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `param1` | string | Yes | Description |
| `param2` | int | No | Description |

**Request Body**

```json
{
  "field1": "value",
  "field2": 123
}
```

**Response**

- Status: `200 OK`

```json
{
  "success": true,
  "data": {}
}
```

**Error Responses**

| Status | Code | Message |
|--------|------|---------|
| 400 | BAD_REQUEST | Invalid input |
| 401 | UNAUTHORIZED | Token missing or expired |
| 404 | NOT_FOUND | Resource not found |

**Notes**

- Any extra info, edge cases, or gotchas.
```

---

## APIs

---

### 1. GET  Languages

**Description:** Returns the full list of supported languages in the TecDoc catalog, each with a numeric ID, ISO 2-letter code, and display name.

**Auth Required:** Yes (RapidAPI key)

**Request**

- Method: `GET`
- URL: `https://tecdoc-catalog.p.rapidapi.com/languages/list`
- Headers:
  - `x-rapidapi-host: tecdoc-catalog.p.rapidapi.com`
  - `x-rapidapi-key: <YOUR_RAPIDAPI_KEY>`

**Query Params:** None

**Request Body:** None

**Response**

- Status: `200 OK`
- Response Time: ~1001 ms
- Body Size: 2 Bytes (headers only, body is JSON array)

```json
[
  { "lngId": "1",   "lngIso2": "de",   "lngDescription": "Deutsch" },
  { "lngId": "4",   "lngIso2": "en",   "lngDescription": "English (GB)" },
  { "lngId": "6",   "lngIso2": "fr",   "lngDescription": "Français" },
  { "lngId": "7",   "lngIso2": "it",   "lngDescription": "Italiano" },
  { "lngId": "8",   "lngIso2": "es",   "lngDescription": "Español" },
  { "lngId": "9",   "lngIso2": "nl",   "lngDescription": "Nederlands" },
  { "lngId": "10",  "lngIso2": "da",   "lngDescription": "Dansk" },
  { "lngId": "11",  "lngIso2": "sv",   "lngDescription": "Svenska" },
  { "lngId": "12",  "lngIso2": "no",   "lngDescription": "Norsk" },
  { "lngId": "13",  "lngIso2": "fi",   "lngDescription": "Suomi" },
  { "lngId": "14",  "lngIso2": "hu",   "lngDescription": "Magyar" },
  { "lngId": "15",  "lngIso2": "pt",   "lngDescription": "Português" },
  { "lngId": "16",  "lngIso2": "ru",   "lngDescription": "русский" },
  { "lngId": "17",  "lngIso2": "sk",   "lngDescription": "slovenčina" },
  { "lngId": "18",  "lngIso2": "cs",   "lngDescription": "čeština" },
  { "lngId": "19",  "lngIso2": "pl",   "lngDescription": "polski" },
  { "lngId": "20",  "lngIso2": "el",   "lngDescription": "Ελληvικά" },
  { "lngId": "21",  "lngIso2": "ro",   "lngDescription": "Română" },
  { "lngId": "23",  "lngIso2": "tr",   "lngDescription": "Türkçe" },
  { "lngId": "24",  "lngIso2": "hr",   "lngDescription": "Hrvatski" },
  { "lngId": "25",  "lngIso2": "sr",   "lngDescription": "Srpski" },
  { "lngId": "31",  "lngIso2": "zh",   "lngDescription": "中文（简体）" },
  { "lngId": "32",  "lngIso2": "bg",   "lngDescription": "Български" },
  { "lngId": "33",  "lngIso2": "lv",   "lngDescription": "Latviešu" },
  { "lngId": "34",  "lngIso2": "lt",   "lngDescription": "Lietuvių" },
  { "lngId": "35",  "lngIso2": "et",   "lngDescription": "Eesti" },
  { "lngId": "36",  "lngIso2": "sl",   "lngDescription": "Slovenski" },
  { "lngId": "37",  "lngIso2": "qa",   "lngDescription": "English (USA)" },
  { "lngId": "38",  "lngIso2": "qb",   "lngDescription": "English (AUS)" },
  { "lngId": "40",  "lngIso2": "qc",   "lngDescription": "português (BR)" },
  { "lngId": "41",  "lngIso2": "ja",   "lngDescription": "日本語" },
  { "lngId": "42",  "lngIso2": "ar",   "lngDescription": "عربي" },
  { "lngId": "43",  "lngIso2": "he",   "lngDescription": "עברית" },
  { "lngId": "44",  "lngIso2": "qd",   "lngDescription": "Español (MEX)" },
  { "lngId": "45",  "lngIso2": "th",   "lngDescription": "ภาษาไทย (ประเทศไทย)" },
  { "lngId": "46",  "lngIso2": "ko",   "lngDescription": "한국어" },
  { "lngId": "47",  "lngIso2": "ms",   "lngDescription": "Bahasa Melayu" },
  { "lngId": "48",  "lngIso2": "uk",   "lngDescription": "Українська" },
  { "lngId": "49",  "lngIso2": "vi",   "lngDescription": "Tiếng việt" },
  { "lngId": "50",  "lngIso2": "qe",   "lngDescription": "中文（繁體）" },
  { "lngId": "51",  "lngIso2": "id",   "lngDescription": "Bahasa Indonesia" },
  { "lngId": "255", "lngIso2": null,   "lngDescription": "Universal" }
]
```

**Response Fields**

| Field | Type | Description |
|-------|------|-------------|
| `lngId` | string | Numeric language ID used in other TecDoc API calls |
| `lngIso2` | string \| null | ISO 639-1 two-letter language code. `null` for Universal (lngId 255) |
| `lngDescription` | string | Human-readable language name in its native script |

**Notes**

- `lngId` is used as a parameter in other TecDoc endpoints (e.g., to fetch localized part names)
- `lngId: "255"` with `lngIso2: null` represents "Universal" — language-agnostic data
- Some non-standard codes are used: `qa` = English (USA), `qb` = English (AUS), `qc` = Português (BR), `qd` = Español (MEX), `qe` = 中文（繁體）
- For English (GB) use `lngId: "4"`, for English (USA) use `lngId: "37"`

---

### 2. GET  Countries

**Description:** Returns the full list of countries and regions supported by the TecDoc catalog, each with a numeric ID, country code, and name. Includes both individual countries and regional groupings (e.g., Europe, Middle East, ASEAN).

**Auth Required:** Yes (RapidAPI key)

**Request**

- Method: `GET`
- URL: `https://tecdoc-catalog.p.rapidapi.com/countries/list`
- Headers:
  - `x-rapidapi-host: tecdoc-catalog.p.rapidapi.com`
  - `x-rapidapi-key: <YOUR_RAPIDAPI_KEY>`

**Query Params:** None

**Request Body:** None

**Response**

- Status: `200 OK`
- Response Time: ~1788 ms

```json
{
  "countries": [
    { "id": 1,   "couCode": "A",   "countryName": "Austria" },
    { "id": 2,   "couCode": "ADN", "countryName": "Yemen (People's Democratic Republic)" },
    { "id": 3,   "couCode": "AEU", "countryName": "Except Europe" },
    { "id": 4,   "couCode": "AFG", "countryName": "Afghanistan" },
    { "id": 6,   "couCode": "AK",  "countryName": "Africa" },
    { "id": 20,  "couCode": "AUS", "countryName": "Australia" },
    { "id": 24,  "couCode": "B",   "countryName": "Belgium" },
    { "id": 37,  "couCode": "BR",  "countryName": "Brazil" },
    { "id": 49,  "couCode": "CDN", "countryName": "Canada" },
    { "id": 50,  "couCode": "CH",  "countryName": "Switzerland" },
    { "id": 62,  "couCode": "CZ",  "countryName": "Czech Republic" },
    { "id": 63,  "couCode": "D",   "countryName": "Germany" },
    { "id": 66,  "couCode": "DK",  "countryName": "Denmark" },
    { "id": 70,  "couCode": "E",   "countryName": "Spain" },
    { "id": 82,  "couCode": "EU",  "countryName": "Europe" },
    { "id": 85,  "couCode": "F",   "countryName": "France" },
    { "id": 93,  "couCode": "GB",  "countryName": "Great Britain" },
    { "id": 107, "couCode": "GR",  "countryName": "Greece" },
    { "id": 113, "couCode": "H",   "countryName": "Hungary" },
    { "id": 118, "couCode": "I",   "countryName": "Italy" },
    { "id": 121, "couCode": "IND", "countryName": "India" },
    { "id": 124, "couCode": "IRL", "countryName": "Ireland" },
    { "id": 127, "couCode": "J",   "countryName": "Japan" },
    { "id": 138, "couCode": "L",   "countryName": "Luxembourg" },
    { "id": 143, "couCode": "LT",  "countryName": "Lithuania" },
    { "id": 144, "couCode": "LV",  "countryName": "Latvia" },
    { "id": 149, "couCode": "MAL", "countryName": "Malaysia" },
    { "id": 153, "couCode": "MEX", "countryName": "Mexico" },
    { "id": 167, "couCode": "N",   "countryName": "Norway" },
    { "id": 175, "couCode": "NL",  "countryName": "The Netherlands" },
    { "id": 179, "couCode": "NZ",  "countryName": "New Zealand" },
    { "id": 183, "couCode": "P",   "countryName": "Portugal" },
    { "id": 188, "couCode": "PL",  "countryName": "Poland" },
    { "id": 196, "couCode": "Q",   "countryName": "Qatar" },
    { "id": 197, "couCode": "RA",  "countryName": "Argentina" },
    { "id": 218, "couCode": "RUS", "countryName": "Russia" },
    { "id": 220, "couCode": "S",   "countryName": "Sweden" },
    { "id": 221, "couCode": "SA",  "countryName": "Saudi Arabia" },
    { "id": 224, "couCode": "SF",  "countryName": "Finland" },
    { "id": 225, "couCode": "SGP", "countryName": "Singapore" },
    { "id": 228, "couCode": "SK",  "countryName": "Slovakia" },
    { "id": 248, "couCode": "TJ",  "countryName": "China" },
    { "id": 255, "couCode": "TR",  "countryName": "Turkey" },
    { "id": 258, "couCode": "UA",  "countryName": "Ukraine" },
    { "id": 259, "couCode": "UAE", "countryName": "United Arab Emirates" },
    { "id": 261, "couCode": "USA", "countryName": "United States of America" },
    { "id": 266, "couCode": "VN",  "countryName": "Vietnam" },
    { "id": 282, "couCode": "ZA",  "countryName": "South Africa" }
  ]
}
```

> Full list has **283 entries** — truncated above to key countries.

**Response Fields**

| Field | Type | Description |
|-------|------|-------------|
| `countries` | array | Top-level wrapper containing all country objects |
| `id` | integer | Numeric country ID used as a parameter in other TecDoc API calls |
| `couCode` | string | TecDoc country code (not always ISO 3166 — uses its own convention) |
| `countryName` | string | Human-readable country or region name in English |

**Notes**

- Includes **both individual countries and regional groupings** — e.g., `EU` (Europe), `MEA` (Middle East), `ASEAN`, `NAM` (North America), `AK` (Africa), `AS` (South America)
- `couCode` is NOT always ISO 3166 — TecDoc uses its own convention (e.g., `D` = Germany, `F` = France, `I` = Italy, `J` = Japan)
- Use `id` (not `couCode`) when passing the country as a parameter to other TecDoc endpoints
- Special groupings include traffic-side regions: `LVK` = Left-hand Traffic, `RHD` = Europe RHD
- Total: **283 countries/regions** in the full response

---

### 3. GET  Language Info by ID

**Description:** Returns the details of a single language by its numeric TecDoc language ID.

**Auth Required:** Yes (RapidAPI key)

**Request**

- Method: `GET`
- URL: `https://tecdoc-catalog.p.rapidapi.com/languages/get-language/lang-id/{lang_id}`
- Headers:
  - `x-rapidapi-host: tecdoc-catalog.p.rapidapi.com`
  - `x-rapidapi-key: <YOUR_RAPIDAPI_KEY>`

**Path Parameters**

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `lang_id` | integer | Yes | Numeric language ID from `/languages/list` (e.g., `4` for English GB) |

**Query Params:** None

**Request Body:** None

**Example Request**

```
GET /languages/get-language/lang-id/4
```

**Response**

- Status: `200 OK`
- Response Time: ~1293 ms

```json
{
  "lngId": "4",
  "lngIso2": "en",
  "lngDescription": "English (GB)"
}
```

**Response Fields**

| Field | Type | Description |
|-------|------|-------------|
| `lngId` | string | Numeric language ID |
| `lngIso2` | string | ISO 639-1 two-letter language code |
| `lngDescription` | string | Human-readable language name in its native script |

**Notes**

- Use `lngId` values from `/languages/list` to look up individual languages
- Returns a single object (not an array), unlike `/languages/list`
- Common IDs: `1` = Deutsch, `4` = English (GB), `6` = Français, `37` = English (USA)

---

### 4. GET  Countries by Language ID

**Description:** Returns the list of countries available for a specific language ID. The `countryName` values are returned in the language matching the given `lang_id`. Same structure as `/countries/list` but scoped to a language.

**Auth Required:** Yes (RapidAPI key)

**Request**

- Method: `GET`
- URL: `https://tecdoc-catalog.p.rapidapi.com/countries/list-countries-by-lang-id/{lang_id}`
- Headers:
  - `x-rapidapi-host: tecdoc-catalog.p.rapidapi.com`
  - `x-rapidapi-key: <YOUR_RAPIDAPI_KEY>`

**Path Parameters**

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `lang_id` | integer | Yes | Numeric language ID from `/languages/list` (e.g., `4` for English GB) |

**Query Params:** None

**Request Body:** None

**Example Request**

```
GET /countries/list-countries-by-lang-id/4
```

**Response**

- Status: `200 OK`
- Response Time: ~1568 ms

```json
{
  "countries": [
    { "id": 1,   "couCode": "A",   "countryName": "Austria" },
    { "id": 2,   "couCode": "ADN", "countryName": "Yemen (People's Democratic Republic)" },
    { "id": 3,   "couCode": "AEU", "countryName": "Except Europe" },
    { "id": 63,  "couCode": "D",   "countryName": "Germany" },
    { "id": 85,  "couCode": "F",   "countryName": "France" },
    { "id": 93,  "couCode": "GB",  "countryName": "Great Britain" },
    { "id": 261, "couCode": "USA", "countryName": "United States of America" },
    { "id": 283, "couCode": "ZW",  "countryName": "Zimbabwe" }
  ]
}
```

> Full response has **283 entries** (same count as `/countries/list` when called with `lang_id=4`). Truncated above for brevity.

**Response Fields**

| Field | Type | Description |
|-------|------|-------------|
| `countries` | array | List of country objects available for the given language |
| `id` | integer | Numeric country ID used in other TecDoc API calls |
| `couCode` | string | TecDoc country code |
| `countryName` | string | Country name — localized to the requested language |

**Notes**

- The `countryName` field is the key difference from `/countries/list` — it returns names **localized to the specified language** (e.g., `lang_id=1` returns German names, `lang_id=6` returns French names)
- With `lang_id=4` (English GB) the response is identical in structure and count (283 entries) to `/countries/list`
- Use this endpoint when you need country names in a specific user-facing language
- `id` values are consistent across all language variants — safe to use as keys

---

## Manufacturer

---

### 5. GET  Vehicle Types

**Description:** Returns the complete list of vehicle type categories supported by TecDoc. Used to scope manufacturer and vehicle lookups to a specific vehicle category (e.g., passenger cars, trucks, motorcycles).

**Auth Required:** Yes (RapidAPI key)

**Request**

- Method: `GET`
- URL: `https://tecdoc-catalog.p.rapidapi.com/types/list-vehicles-type`
- Headers:
  - `x-rapidapi-host: tecdoc-catalog.p.rapidapi.com`
  - `x-rapidapi-key: <YOUR_RAPIDAPI_KEY>`

**Query Params:** None

**Request Body:** None

**Response**

- Status: `200 OK`
- Response Time: ~995 ms

```json
[
  { "id": 1,  "vehicleType": "PC" },
  { "id": 2,  "vehicleType": "CV" },
  { "id": 3,  "vehicleType": "Motorcycle" },
  { "id": 4,  "vehicleType": "LCV" },
  { "id": 5,  "vehicleType": "DriverCab" },
  { "id": 6,  "vehicleType": "Axle" },
  { "id": 7,  "vehicleType": "Engine" },
  { "id": 8,  "vehicleType": "Bus" },
  { "id": 9,  "vehicleType": "Aftermarket" },
  { "id": 10, "vehicleType": "Tractor" },
  { "id": 11, "vehicleType": "Virtual OEM" }
]
```

**Response Fields**

| Field | Type | Description |
|-------|------|-------------|
| `id` | integer | Numeric vehicle type ID used in manufacturer/vehicle lookup endpoints |
| `vehicleType` | string | Short name of the vehicle category |

**Vehicle Type Reference**

| ID | Type | Description |
|----|------|-------------|
| 1 | PC | Passenger Car |
| 2 | CV | Commercial Vehicle (heavy trucks) |
| 3 | Motorcycle | Motorcycles and scooters |
| 4 | LCV | Light Commercial Vehicle (vans, pickups) |
| 5 | DriverCab | Driver cab / cabin assemblies |
| 6 | Axle | Axle assemblies |
| 7 | Engine | Standalone engine units |
| 8 | Bus | Buses and coaches |
| 9 | Aftermarket | Aftermarket / universal parts |
| 10 | Tractor | Agricultural tractors |
| 11 | Virtual OEM | Virtual OEM groupings |

**Notes**

- Returns a bare array (no wrapper object), same as `/languages/list`
- Pass `id` from this endpoint as the vehicle type filter in manufacturer and model lookup calls
- Most common values in practice: `1` (PC), `2` (CV), `3` (Motorcycle), `4` (LCV)

---

### 6. GET  Manufacturer IDs by Type ID

**Description:** Returns all manufacturers for a given vehicle type ID, with a total count. Use this to get `manufacturerId` values needed for model/vehicle lookup calls.

**Auth Required:** Yes (RapidAPI key)

**Request**

- Method: `GET`
- URL: `https://tecdoc-catalog.p.rapidapi.com/manufacturers/list/type-id/{type_id}`
- Headers:
  - `x-rapidapi-host: tecdoc-catalog.p.rapidapi.com`
  - `x-rapidapi-key: <YOUR_RAPIDAPI_KEY>`

**Path Parameters**

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `type_id` | integer | Yes | Vehicle type ID from `/types/list-vehicles-type` (e.g., `1` = PC, `2` = CV) |

**Query Params:** None

**Request Body:** None

**Example Request**

```
GET /manufacturers/list/type-id/1
```

**Response**

- Status: `200 OK`
- Response Time: ~969 ms

```json
{
  "countManufactures": 698,
  "manufacturers": [
    { "manufacturerId": 8232, "manufacturerName": "212" },
    { "manufacturerId": 3854, "manufacturerName": "ABARTH" },
    { "manufacturerId": 609,  "manufacturerName": "AC" },
    { "manufacturerId": 1505, "manufacturerName": "ACURA" },
    { "manufacturerId": 2,    "manufacturerName": "ALFA ROMEO" },
    { "manufacturerId": 5,    "manufacturerName": "AUDI" },
    { "manufacturerId": 16,   "manufacturerName": "BMW" },
    { "manufacturerId": 138,  "manufacturerName": "CHEVROLET" },
    { "manufacturerId": 21,   "manufacturerName": "CITROËN" },
    { "manufacturerId": 139,  "manufacturerName": "DACIA" },
    { "manufacturerId": 25,   "manufacturerName": "DAIHATSU" },
    { "manufacturerId": 29,   "manufacturerName": "DODGE" },
    { "manufacturerId": 35,   "manufacturerName": "FIAT" },
    { "manufacturerId": 700,  "manufacturerName": "FERRARI" },
    { "manufacturerId": 36,   "manufacturerName": "FORD" },
    { "manufacturerId": 776,  "manufacturerName": "FORD USA" },
    { "manufacturerId": 45,   "manufacturerName": "HONDA" },
    { "manufacturerId": 183,  "manufacturerName": "HYUNDAI" },
    { "manufacturerId": 56,   "manufacturerName": "JAGUAR" },
    { "manufacturerId": 882,  "manufacturerName": "JEEP" },
    { "manufacturerId": 184,  "manufacturerName": "KIA" },
    { "manufacturerId": 63,   "manufacturerName": "LADA" },
    { "manufacturerId": 701,  "manufacturerName": "LAMBORGHINI" },
    { "manufacturerId": 64,   "manufacturerName": "LANCIA" },
    { "manufacturerId": 1820, "manufacturerName": "LAND ROVER" },
    { "manufacturerId": 842,  "manufacturerName": "LEXUS" },
    { "manufacturerId": 74,   "manufacturerName": "MERCEDES-BENZ" },
    { "manufacturerId": 75,   "manufacturerName": "MG" },
    { "manufacturerId": 77,   "manufacturerName": "MITSUBISHI" },
    { "manufacturerId": 80,   "manufacturerName": "NISSAN" },
    { "manufacturerId": 84,   "manufacturerName": "OPEL" },
    { "manufacturerId": 88,   "manufacturerName": "PEUGEOT" },
    { "manufacturerId": 92,   "manufacturerName": "PORSCHE" },
    { "manufacturerId": 93,   "manufacturerName": "RENAULT" },
    { "manufacturerId": 705,  "manufacturerName": "ROLLS-ROYCE" },
    { "manufacturerId": 99,   "manufacturerName": "SAAB" },
    { "manufacturerId": 104,  "manufacturerName": "SEAT" },
    { "manufacturerId": 106,  "manufacturerName": "SKODA" },
    { "manufacturerId": 107,  "manufacturerName": "SUBARU" },
    { "manufacturerId": 109,  "manufacturerName": "SUZUKI" },
    { "manufacturerId": 3328, "manufacturerName": "TESLA" },
    { "manufacturerId": 111,  "manufacturerName": "TOYOTA" },
    { "manufacturerId": 112,  "manufacturerName": "TRIUMPH" }
  ]
}
```

> Full response for `type-id/1` (PC) contains **698 manufacturers**. Truncated above to key brands.

**Response Fields**

| Field | Type | Description |
|-------|------|-------------|
| `countManufactures` | integer | Total number of manufacturers for the given vehicle type |
| `manufacturers` | array | List of manufacturer objects |
| `manufacturerId` | integer | Numeric manufacturer ID used in model/vehicle lookup endpoints |
| `manufacturerName` | string | Brand name in uppercase |

**Notes**

- Use `manufacturerId` in subsequent calls to fetch models and vehicle variants
- Some brands appear multiple times with different joint-venture suffixes (e.g., `FORD`, `FORD USA`, `FORD (CHANGAN)`, `FORD (JMC)`) — each has a different `manufacturerId`
- `type-id/1` (PC) returns the largest list: **698 manufacturers**
- Manufacturers are sorted alphabetically by name
- The field name is `countManufactures` (not `countManufacturers`) — note the typo in the API response

---

### 7. GET  Manufacturer Info by ID

**Description:** Returns detailed information about a single manufacturer by their numeric ID, including which vehicle types they cover, total model count, and brand logo image URL.

**Auth Required:** Yes (RapidAPI key)

**Request**

- Method: `GET`
- URL: `https://tecdoc-catalog.p.rapidapi.com/manufacturers/find-by-id/{manufacturer_id}`
- Headers:
  - `x-rapidapi-host: tecdoc-catalog.p.rapidapi.com`
  - `x-rapidapi-key: <YOUR_RAPIDAPI_KEY>`

**Path Parameters**

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `manufacturer_id` | integer | Yes | Numeric manufacturer ID from `/manufacturers/list/type-id/{id}` |

**Query Params:** None

**Request Body:** None

**Example Request**

```
GET /manufacturers/find-by-id/184
```

**Response**

- Status: `200 OK`
- Response Time: ~603 ms

```json
{
  "manufacturerId": 184,
  "manufacturerName": "KIA",
  "vehicleTypes": "CV,Engine,PC,Bus",
  "modelCount": 159,
  "image": "https://fsn1.your-objectstorage.com/tecdoc2025/brands/184.png"
}
```

**Response Fields**

| Field | Type | Description |
|-------|------|-------------|
| `manufacturerId` | integer | Numeric manufacturer ID |
| `manufacturerName` | string | Brand name in uppercase |
| `vehicleTypes` | string | Comma-separated list of vehicle type names this manufacturer covers |
| `modelCount` | integer | Total number of vehicle models in the TecDoc catalog for this manufacturer |
| `image` | string | URL to the brand logo PNG image |

**Notes**

- `vehicleTypes` is a **comma-separated string** (not an array) — split on `,` before using
- `image` URL pattern is `https://fsn1.your-objectstorage.com/tecdoc2025/brands/{manufacturerId}.png` — can be constructed directly if the ID is known
- `modelCount` reflects all models across all vehicle types for that brand, not just one type
- Use this endpoint to display brand details (logo, name, supported types) before drilling into models

---

### 8. GET  Models by Type & Manufacturer

**Description:** Returns all vehicle models for a given combination of vehicle type, manufacturer, language, and country. Model names and year ranges are localized based on `lang_id` and filtered by `country_filter_id`.

**Auth Required:** Yes (RapidAPI key)

**Request**

- Method: `GET`
- URL: `https://tecdoc-catalog.p.rapidapi.com/models/list/type-id/{type_id}/manufacturer-id/{manufacturer_id}/lang-id/{lang_id}/country-filter-id/{country_filter_id}`
- Headers:
  - `x-rapidapi-host: tecdoc-catalog.p.rapidapi.com`
  - `x-rapidapi-key: <YOUR_RAPIDAPI_KEY>`

**Path Parameters**

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `type_id` | integer | Yes | Vehicle type ID from `/types/list-vehicles-type` (e.g., `1` = PC) |
| `manufacturer_id` | integer | Yes | Manufacturer ID from `/manufacturers/list/type-id/{id}` (e.g., `5` = AUDI) |
| `lang_id` | integer | Yes | Language ID from `/languages/list` (e.g., `4` = English GB) |
| `country_filter_id` | integer | Yes | Country ID from `/countries/list` (e.g., `63` = Germany) |

**Query Params:** None

**Request Body:** None

**Example Request**

```
GET /models/list/type-id/1/manufacturer-id/5/lang-id/4/country-filter-id/63
```
> Returns all AUDI passenger car models, in English, filtered for Germany.

**Response**

- Status: `200 OK`
- Response Time: ~1040 ms

```json
{
  "countModels": 130,
  "models": [
    { "modelId": 1,     "modelName": "80 B4 Saloon (8C2)",           "modelYearFrom": "1991-09-01", "modelYearTo": "1995-07-01" },
    { "modelId": 6,     "modelName": "80 B4 Avant (8C5)",            "modelYearFrom": "1991-09-01", "modelYearTo": "1996-01-01" },
    { "modelId": 253,   "modelName": "A4 B5 (8D2)",                  "modelYearFrom": "1994-11-01", "modelYearTo": "2001-12-01" },
    { "modelId": 258,   "modelName": "A6 C4 (4A2)",                  "modelYearFrom": "1994-06-01", "modelYearTo": "1998-01-01" },
    { "modelId": 265,   "modelName": "A8 D2 (4D2, 4D8)",             "modelYearFrom": "1994-03-01", "modelYearTo": "2005-12-01" },
    { "modelId": 1557,  "modelName": "A3 (8L1)",                     "modelYearFrom": "1996-09-01", "modelYearTo": "2006-09-01" },
    { "modelId": 3851,  "modelName": "TT (8N3)",                     "modelYearFrom": "1998-10-01", "modelYearTo": "2007-02-01" },
    { "modelId": 4731,  "modelName": "A4 B6 (8E2)",                  "modelYearFrom": "2000-11-01", "modelYearTo": "2005-12-01" },
    { "modelId": 4955,  "modelName": "A3 (8P1)",                     "modelYearFrom": "2003-05-01", "modelYearTo": "2013-12-01" },
    { "modelId": 5461,  "modelName": "Q7 (4LB)",                     "modelYearFrom": "2006-03-01", "modelYearTo": "2016-01-01" },
    { "modelId": 6244,  "modelName": "R8 (422, 423)",                "modelYearFrom": "2007-04-01", "modelYearTo": "2016-08-01" },
    { "modelId": 6418,  "modelName": "A4 B8 (8K2)",                  "modelYearFrom": "2007-08-01", "modelYearTo": "2017-06-01" },
    { "modelId": 7534,  "modelName": "Q5 (8RB)",                     "modelYearFrom": "2008-11-01", "modelYearTo": "2019-04-01" },
    { "modelId": 8604,  "modelName": "A1 (8X1, 8XK)",               "modelYearFrom": "2010-05-01", "modelYearTo": "2019-09-01" },
    { "modelId": 9154,  "modelName": "A6 C7 (4G2, 4GC)",            "modelYearFrom": "2010-11-01", "modelYearTo": "2019-11-01" },
    { "modelId": 9731,  "modelName": "Q3 (8UB, 8UG)",               "modelYearFrom": "2011-06-01", "modelYearTo": "2020-03-01" },
    { "modelId": 10253, "modelName": "A3 (8V1, 8VK)",               "modelYearFrom": "2012-04-01", "modelYearTo": "2020-10-01" },
    { "modelId": 14695, "modelName": "A4 B9 (8W2, 8WC)",            "modelYearFrom": "2015-05-01", "modelYearTo": null },
    { "modelId": 36543, "modelName": "Q2 (GAB, GAG)",               "modelYearFrom": "2016-06-01", "modelYearTo": null },
    { "modelId": 37161, "modelName": "Q5 (FYB, FYG)",               "modelYearFrom": "2016-05-01", "modelYearTo": null },
    { "modelId": 38843, "modelName": "A6 C8 (4A2)",                 "modelYearFrom": "2018-02-01", "modelYearTo": null },
    { "modelId": 39213, "modelName": "E-TRON (GEN)",                "modelYearFrom": "2018-09-01", "modelYearTo": null },
    { "modelId": 41812, "modelName": "E-TRON GT Saloon (F83, F8P)", "modelYearFrom": "2020-07-01", "modelYearTo": null },
    { "modelId": 41930, "modelName": "Q4 SUV (F4B)",                "modelYearFrom": "2020-07-01", "modelYearTo": null },
    { "modelId": 43700, "modelName": "Q8 E-TRON SUV (GEG)",        "modelYearFrom": "2022-11-01", "modelYearTo": null },
    { "modelId": 45332, "modelName": "Q6 (GFB)",                    "modelYearFrom": "2024-04-01", "modelYearTo": null },
    { "modelId": 45817, "modelName": "Q5 (GUB)",                    "modelYearFrom": "2025-01-01", "modelYearTo": null }
  ]
}
```

> Full response has **130 models** for AUDI PC in Germany. Truncated above for brevity.

**Response Fields**

| Field | Type | Description |
|-------|------|-------------|
| `countModels` | integer | Total number of models returned for the given filters |
| `models` | array | List of vehicle model objects |
| `modelId` | integer | Numeric model ID used in subsequent vehicle/part lookup calls |
| `modelName` | string | Full model name including generation code and body codes in parentheses |
| `modelYearFrom` | string | Production start date in `YYYY-MM-DD` format |
| `modelYearTo` | string \| null | Production end date in `YYYY-MM-DD` format. `null` = model still in production |

**Notes**

- `modelYearTo: null` means the model is **currently in production**
- `modelName` format: `<Series> <Generation> <Body type> (<chassis codes>)` — e.g., `A4 B9 (8W2, 8WC)`
- `country_filter_id` scopes results to market-specific variants — same model may appear/disappear depending on the country
- `lang_id` affects the language of `modelName` labels
- Use `modelId` in the next step to fetch vehicle variants (engines, trims) within a model
- The 4-parameter URL is the only way to call this endpoint — all 4 path params are required

---

### 9. GET  Model Details by Model ID

**Description:** Returns the details of a single vehicle model by its ID, scoped to vehicle type, language, and country.

**Auth Required:** Yes (RapidAPI key)

**Request**

- Method: `GET`
- URL: `https://tecdoc-catalog.p.rapidapi.com/models/type-id/{type_id}/model-id/{model_id}/lang-id/{lang_id}/country-filter-id/{country_filter_id}`
- Headers:
  - `x-rapidapi-host: tecdoc-catalog.p.rapidapi.com`
  - `x-rapidapi-key: <YOUR_RAPIDAPI_KEY>`

**Path Parameters**

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `type_id` | integer | Yes | Vehicle type ID (e.g., `1` = PC) |
| `model_id` | integer | Yes | Model ID from `/models/list` (e.g., `5626`) |
| `lang_id` | integer | Yes | Language ID (e.g., `4` = English GB) |
| `country_filter_id` | integer | Yes | Country ID (e.g., `63` = Germany) |

**Query Params:** None

**Request Body:** None

**Example Request**

```
GET /models/type-id/1/model-id/5626/lang-id/4/country-filter-id/63
```

**Response**

- Status: `200 OK`
- Response Time: ~1339 ms

```json
{
  "modelId": 5626,
  "modelName": "CEE'D Hatchback (ED)"
}
```

**Response Fields**

| Field | Type | Description |
|-------|------|-------------|
| `modelId` | integer | Numeric model ID |
| `modelName` | string | Full model name including body type and chassis code |

**Notes**

- Same 4 path params as `/models/list` — type, model, language, country all required
- Returns a single object (not an array), unlike `/models/list`
- Use this to resolve a `modelId` back to its human-readable name

---

### 10. GET  Model Details by Vehicle ID

**Description:** Returns the parent model details (model ID and name) for a given vehicle ID. Same response shape as endpoint #9 but looks up by `vehicle_id` instead of `model_id`.

**Auth Required:** Yes (RapidAPI key)

**Request**

- Method: `GET`
- URL: `https://tecdoc-catalog.p.rapidapi.com/models/type-id/{type_id}/vehicles/{vehicle_id}/lang-id/{lang_id}/country-filter-id/{country_filter_id}`
- Headers:
  - `x-rapidapi-host: tecdoc-catalog.p.rapidapi.com`
  - `x-rapidapi-key: <YOUR_RAPIDAPI_KEY>`

**Path Parameters**

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `type_id` | integer | Yes | Vehicle type ID (e.g., `1` = PC) |
| `vehicle_id` | integer | Yes | Vehicle ID (trim/engine variant level, e.g., `19942`) |
| `lang_id` | integer | Yes | Language ID (e.g., `4` = English GB) |
| `country_filter_id` | integer | Yes | Country ID (e.g., `63` = Germany) |

**Query Params:** None

**Request Body:** None

**Example Request**

```
GET /models/type-id/1/vehicles/19942/lang-id/4/country-filter-id/63
```

**Response**

- Status: `200 OK`
- Response Time: ~1074 ms

```json
{
  "modelId": 5626,
  "modelName": "CEE'D Hatchback (ED)"
}
```

**Response Fields**

| Field | Type | Description |
|-------|------|-------------|
| `modelId` | integer | Parent model ID that this vehicle belongs to |
| `modelName` | string | Full model name including body type and chassis code |

**Notes**

- Response is identical to endpoint #9 — the difference is the input: this takes a `vehicle_id` (trim/engine level), endpoint #9 takes a `model_id` (model family level)
- Use this when you have a `vehicle_id` and need to find which model it belongs to
- `vehicle_id` `19942` maps to model `5626` (KIA CEE'D Hatchback ED)

---

### 11. GET  Model Image by Model ID

**Description:** Returns the image URL for a vehicle model by its model ID and type ID. Only 2 path params — no lang or country needed.

**Auth Required:** Yes (RapidAPI key)

**Request**

- Method: `GET`
- URL: `https://tecdoc-catalog.p.rapidapi.com/models/type-id/{type_id}/model-id/{model_id}`
- Headers:
  - `x-rapidapi-host: tecdoc-catalog.p.rapidapi.com`
  - `x-rapidapi-key: <YOUR_RAPIDAPI_KEY>`

**Path Parameters**

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `type_id` | integer | Yes | Vehicle type ID (e.g., `1` = PC) |
| `model_id` | integer | Yes | Model ID from `/models/list` (e.g., `151`) |

**Query Params:** None

**Request Body:** None

**Example Request**

```
GET /models/type-id/1/model-id/151
```

**Response**

- Status: `200 OK`
- Response Time: ~847 ms

```json
{
  "modelImage": "https://fsn1.your-objectstorage.com/tecdoc2025/models/151.jpg"
}
```

**Response Fields**

| Field | Type | Description |
|-------|------|-------------|
| `modelImage` | string | URL to the model image (JPG) |

**Notes**

- Image URL pattern: `https://fsn1.your-objectstorage.com/tecdoc2025/models/{model_id}.jpg` — can be constructed directly without calling this endpoint
- No `lang_id` or `country_filter_id` needed — images are language/country agnostic
- Compare with manufacturer logo URL pattern: `/brands/{manufacturer_id}.png` (endpoint #7)

---

### 12. GET  Engine Types by Model

**Description:** Returns all engine/trim variants for a given vehicle model. Each variant includes full technical specs — power, fuel type, displacement, engine codes, and production interval.

**Auth Required:** Yes (RapidAPI key)

**Request**

- Method: `GET`
- URL: `https://tecdoc-catalog.p.rapidapi.com/types/type-id/{type_id}/list-vehicles-types/{model_id}/lang-id/{lang_id}/country-filter-id/{country_filter_id}`
- Headers:
  - `x-rapidapi-host: tecdoc-catalog.p.rapidapi.com`
  - `x-rapidapi-key: <YOUR_RAPIDAPI_KEY>`

**Path Parameters**

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `type_id` | integer | Yes | Vehicle type ID (e.g., `1` = PC) |
| `model_id` | integer | Yes | Model ID from `/models/list` (e.g., `5626` = KIA CEE'D Hatchback ED) |
| `lang_id` | integer | Yes | Language ID (e.g., `4` = English GB) |
| `country_filter_id` | integer | Yes | Country ID (e.g., `63` = Germany) |

**Query Params:** None

**Request Body:** None

**Example Request**

```
GET /types/type-id/1/list-vehicles-types/5626/lang-id/4/country-filter-id/63
```

**Response**

- Status: `200 OK`
- Response Time: ~1456 ms

```json
{
  "modelType": "PC",
  "countModelTypes": 17,
  "modelTypes": [
    {
      "vehicleId": 19942,
      "manufacturerName": "KIA",
      "modelName": "CEE'D Hatchback (ED)",
      "typeEngineName": "1.6 CRDi 115",
      "constructionIntervalStart": "2006-12-01",
      "constructionIntervalEnd": "2012-12-01",
      "powerKw": "85.0000",
      "powerPs": "115.0000",
      "capacityTax": null,
      "fuelType": "Diesel",
      "bodyType": "Hatchback",
      "numberOfCylinders": 4,
      "capacityLt": "1.6000",
      "capacityTech": "1582.0000",
      "engineCodes": "D4FB",
      "engId": 19228
    },
    {
      "vehicleId": 5972,
      "manufacturerName": "KIA",
      "modelName": "CEE'D Hatchback (ED)",
      "typeEngineName": "1.4 CVVT",
      "constructionIntervalStart": "2009-08-01",
      "constructionIntervalEnd": "2012-12-01",
      "powerKw": "66.0000",
      "powerPs": "90.0000",
      "capacityTax": null,
      "fuelType": "Petrol",
      "bodyType": "Hatchback",
      "numberOfCylinders": 4,
      "capacityLt": "1.4000",
      "capacityTech": "1396.0000",
      "engineCodes": "G4FA",
      "engId": 19226
    }
  ]
}
```

> Full response has **17 engine variants** for KIA CEE'D Hatchback (ED). Truncated above for brevity.

**Response Fields**

| Field | Type | Description |
|-------|------|-------------|
| `modelType` | string | Vehicle type name (e.g., `"PC"`) |
| `countModelTypes` | integer | Total number of engine/trim variants for this model |
| `modelTypes` | array | List of engine variant objects |
| `vehicleId` | integer | Unique vehicle ID for this specific trim — used in parts lookup |
| `manufacturerName` | string | Brand name |
| `modelName` | string | Full model name with body type and chassis code |
| `typeEngineName` | string | Engine name/trim label (e.g., `"1.6 CRDi 115"`) |
| `constructionIntervalStart` | string | Production start date (`YYYY-MM-DD`) |
| `constructionIntervalEnd` | string | Production end date (`YYYY-MM-DD`) |
| `powerKw` | string | Power output in kilowatts |
| `powerPs` | string | Power output in PS (horsepower) |
| `capacityTax` | string \| null | Tax displacement value — often `null` |
| `fuelType` | string | Fuel type (e.g., `"Petrol"`, `"Diesel"`, `"Petrol/Liquified Petroleum Gas (LPG)"`) |
| `bodyType` | string | Body style (e.g., `"Hatchback"`) |
| `numberOfCylinders` | integer | Number of engine cylinders |
| `capacityLt` | string | Engine displacement in litres (e.g., `"1.6000"`) |
| `capacityTech` | string | Exact technical displacement in cc (e.g., `"1582.0000"`) |
| `engineCodes` | string | OEM engine code(s) (e.g., `"D4FB"`, `"G4FA"`) |
| `engId` | integer | TecDoc engine ID — used for engine-specific part lookups |

**Notes**

- `vehicleId` is the key value — pass it to parts lookup endpoints to find compatible parts for a specific trim
- `powerKw` and `powerPs` are strings with 4 decimal places — parse to float before use
- `capacityLt` and `capacityTech` are also strings — `capacityLt` is rounded, `capacityTech` is the exact value in cc
- Multiple variants can share the same `engId` (e.g., different power outputs on the same engine family)
- `fuelType` can be a combined value for bi-fuel vehicles (e.g., `"Petrol/Liquified Petroleum Gas (LPG)"`)
- `capacityTax` is frequently `null` — do not rely on it

---

### 13. GET  Engine Details

**Description:** Returns full technical specifications for a single engine by its TecDoc engine ID and language.

**Auth Required:** Yes (RapidAPI key)

**Request**

- Method: `GET`
- URL: `https://tecdoc-catalog.p.rapidapi.com/engines/engine-details/engine-id/{engine_id}/lang-id/{lang_id}`
- Headers:
  - `x-rapidapi-host: tecdoc-catalog.p.rapidapi.com`
  - `x-rapidapi-key: <YOUR_RAPIDAPI_KEY>`

**Path Parameters**

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `engine_id` | integer | Yes | Engine ID (`engId`) from `/types/list-vehicles-types` endpoint #12 |
| `lang_id` | integer | Yes | Language ID (e.g., `4` = English GB) |

**Query Params:** None

**Request Body:** None

**Example Request**

```
GET /engines/engine-details/engine-id/19228/lang-id/4
```

**Response**

- Status: `200 OK`
- Response Time: ~1276 ms

```json
{
  "engId": 19228,
  "manufacturerName": "KIA",
  "engineCodes": "D4FB",
  "engPowerKwStart": "66.000",
  "engPowerKwUpto": "100.000",
  "engPowerPsStart": "90.000",
  "engPowerPsUpto": "136.000",
  "engCapacityCcmStart": "1582.000",
  "engCapacityCcmUpto": null,
  "engCiFrom": null,
  "engCiTo": null,
  "engCompressionStart": "1730.000",
  "engCompressionUpto": null,
  "engTorqueNmStart": null,
  "engTorqueNmUpto": null,
  "engBore": "77200.000",
  "engStroke": "84500.000",
  "engNumberOfCylinders": 4,
  "engNumberOfMainBearings": 5,
  "engNumberOfValves": 16,
  "engineConstruction": "Straight",
  "fuelType": "Diesel",
  "fuelMixture": "Motronic",
  "chargeType": "Exhaust Turbocharger",
  "emissionNorm": "Euro 4",
  "cylinderConstruction": "DOHC",
  "engineManagement": "Timing Chain",
  "valveManagement": null,
  "coolingType": null,
  "engineType": null
}
```

**Response Fields**

| Field | Type | Description |
|-------|------|-------------|
| `engId` | integer | TecDoc engine ID |
| `manufacturerName` | string | Brand name |
| `engineCodes` | string | OEM engine code(s) (e.g., `"D4FB"`) |
| `engPowerKwStart` | string | Minimum power output in kW across all variants |
| `engPowerKwUpto` | string | Maximum power output in kW across all variants |
| `engPowerPsStart` | string | Minimum power output in PS |
| `engPowerPsUpto` | string | Maximum power output in PS |
| `engCapacityCcmStart` | string | Engine displacement in cc |
| `engCapacityCcmUpto` | string \| null | Upper displacement limit (if range) |
| `engCiFrom` | string \| null | Cubic inch displacement from |
| `engCiTo` | string \| null | Cubic inch displacement to |
| `engCompressionStart` | string | Compression ratio start value |
| `engCompressionUpto` | string \| null | Compression ratio upper limit |
| `engTorqueNmStart` | string \| null | Minimum torque in Nm |
| `engTorqueNmUpto` | string \| null | Maximum torque in Nm |
| `engBore` | string | Cylinder bore in mm × 1000 (e.g., `"77200.000"` = 77.2 mm) |
| `engStroke` | string | Piston stroke in mm × 1000 (e.g., `"84500.000"` = 84.5 mm) |
| `engNumberOfCylinders` | integer | Number of cylinders |
| `engNumberOfMainBearings` | integer | Number of main crankshaft bearings |
| `engNumberOfValves` | integer | Total number of valves |
| `engineConstruction` | string | Engine layout (e.g., `"Straight"`, `"V"`) |
| `fuelType` | string | Fuel type (e.g., `"Diesel"`, `"Petrol"`) |
| `fuelMixture` | string | Fuel mixture system (e.g., `"Motronic"`) |
| `chargeType` | string | Forced induction type (e.g., `"Exhaust Turbocharger"`) |
| `emissionNorm` | string | Emission standard (e.g., `"Euro 4"`) |
| `cylinderConstruction` | string | Valve train type (e.g., `"DOHC"`, `"SOHC"`) |
| `engineManagement` | string | Timing system (e.g., `"Timing Chain"`, `"Timing Belt"`) |
| `valveManagement` | string \| null | Variable valve timing system if equipped |
| `coolingType` | string \| null | Cooling method (e.g., `"Water"`) |
| `engineType` | string \| null | Additional engine type classification |

**Notes**

- `engBore` and `engStroke` values are stored as mm × 1000 — divide by 1000 to get actual mm (e.g., `77200.000` → `77.2 mm`)
- `engPowerKwStart`/`engPowerKwUpto` represent the power range across all vehicle variants using this engine — one engine code can power multiple trims at different outputs
- Many fields are `null` when data is not available in TecDoc — handle gracefully
- `engId` from endpoint #12 (`modelTypes[].engId`) is the input here

---

### 14. GET  Vehicle IDs by Model ID

**Description:** Returns a lightweight list of all vehicle variants (trims) for a model — only `vehicleId` and engine name, no full technical specs. Use this when you only need vehicle IDs for parts lookup without the overhead of full engine data.

**Auth Required:** Yes (RapidAPI key)

**Request**

- Method: `GET`
- URL: `https://tecdoc-catalog.p.rapidapi.com/types/type-id/{type_id}/list-vehicles-id/{model_id}/lang-id/{lang_id}/country-filter-id/{country_filter_id}`
- Headers:
  - `x-rapidapi-host: tecdoc-catalog.p.rapidapi.com`
  - `x-rapidapi-key: <YOUR_RAPIDAPI_KEY>`

**Path Parameters**

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `type_id` | integer | Yes | Vehicle type ID (e.g., `1` = PC) |
| `model_id` | integer | Yes | Model ID from `/models/list` (e.g., `5626`) |
| `lang_id` | integer | Yes | Language ID (e.g., `4` = English GB) |
| `country_filter_id` | integer | Yes | Country ID (e.g., `63` = Germany) |

**Query Params:** None

**Request Body:** None

**Example Request**

```
GET /types/type-id/1/list-vehicles-id/5626/lang-id/4/country-filter-id/63
```

**Response**

- Status: `200 OK`
- Response Time: ~656 ms

```json
{
  "modelType": "PC",
  "countModelTypes": 17,
  "modelTypes": [
    { "vehicleId": 5972,   "manufacturerName": "KIA", "modelName": "CEE'D Hatchback (ED)", "typeEngineName": "1.4 CVVT" },
    { "vehicleId": 8448,   "manufacturerName": "KIA", "modelName": "CEE'D Hatchback (ED)", "typeEngineName": "1.6 CVVT" },
    { "vehicleId": 8449,   "manufacturerName": "KIA", "modelName": "CEE'D Hatchback (ED)", "typeEngineName": "1.6 CRDi 128" },
    { "vehicleId": 9809,   "manufacturerName": "KIA", "modelName": "CEE'D Hatchback (ED)", "typeEngineName": "1.6" },
    { "vehicleId": 9810,   "manufacturerName": "KIA", "modelName": "CEE'D Hatchback (ED)", "typeEngineName": "1.4" },
    { "vehicleId": 19938,  "manufacturerName": "KIA", "modelName": "CEE'D Hatchback (ED)", "typeEngineName": "1.4" },
    { "vehicleId": 19939,  "manufacturerName": "KIA", "modelName": "CEE'D Hatchback (ED)", "typeEngineName": "1.6" },
    { "vehicleId": 19940,  "manufacturerName": "KIA", "modelName": "CEE'D Hatchback (ED)", "typeEngineName": "2.0" },
    { "vehicleId": 19941,  "manufacturerName": "KIA", "modelName": "CEE'D Hatchback (ED)", "typeEngineName": "1.6 CRDi 90" },
    { "vehicleId": 19942,  "manufacturerName": "KIA", "modelName": "CEE'D Hatchback (ED)", "typeEngineName": "1.6 CRDi 115" },
    { "vehicleId": 23289,  "manufacturerName": "KIA", "modelName": "CEE'D Hatchback (ED)", "typeEngineName": "2.0 CRDi 140" },
    { "vehicleId": 26637,  "manufacturerName": "KIA", "modelName": "CEE'D Hatchback (ED)", "typeEngineName": "1.6" },
    { "vehicleId": 53618,  "manufacturerName": "KIA", "modelName": "CEE'D Hatchback (ED)", "typeEngineName": "2.0 CRDi" },
    { "vehicleId": 133892, "manufacturerName": "KIA", "modelName": "CEE'D Hatchback (ED)", "typeEngineName": "1.6 LPG" },
    { "vehicleId": 133893, "manufacturerName": "KIA", "modelName": "CEE'D Hatchback (ED)", "typeEngineName": "1.4 LPG" },
    { "vehicleId": 133895, "manufacturerName": "KIA", "modelName": "CEE'D Hatchback (ED)", "typeEngineName": "1.6 LPG" },
    { "vehicleId": 133900, "manufacturerName": "KIA", "modelName": "CEE'D Hatchback (ED)", "typeEngineName": "1.4 LPG" }
  ]
}
```

**Response Fields**

| Field | Type | Description |
|-------|------|-------------|
| `modelType` | string | Vehicle type name (e.g., `"PC"`) |
| `countModelTypes` | integer | Total number of variants for this model |
| `modelTypes` | array | Lightweight list of vehicle variants |
| `vehicleId` | integer | Vehicle ID for this trim — use in parts lookup endpoints |
| `manufacturerName` | string | Brand name |
| `modelName` | string | Full model name with body type and chassis code |
| `typeEngineName` | string | Engine/trim label (e.g., `"1.6 CRDi 115"`) |

**Notes**

- This is a **lighter version of endpoint #12** — same URL structure but `list-vehicles-id` instead of `list-vehicles-types`
- Returns only 4 fields per variant vs 17 fields in #12 — use this when you only need `vehicleId` values
- Response time is significantly faster (~656 ms vs ~1456 ms) due to reduced payload
- All 17 `vehicleId` values are returned in full — no truncation

---

### 15. GET  Vehicles by KBA Number (Germany)

**Description:** Looks up a passenger car by its German KBA number (Kraftfahrtbundesamt — Federal Motor Transport Authority). Returns vehicle details including manufacturer, model, engine, body type, production interval, and power output.

**Auth Required:** Yes (RapidAPI key)

**Request**

- Method: `GET`
- URL: `https://tecdoc-catalog.p.rapidapi.com/types/searching-the-passenger-car-by-ltn-number/lang-id/{lang_id}/country-filter-id/{country_id}/ltn-number/{ltn_number}/number-type/{number_type}`
- Headers:
  - `x-rapidapi-host: tecdoc-catalog.p.rapidapi.com`
  - `x-rapidapi-key: <YOUR_RAPIDAPI_KEY>`

**Path Parameters**

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `lang_id` | integer | Yes | Language ID for response labels (e.g., `4` = English GB) |
| `country_id` | integer | Yes | Country filter ID (e.g., `63` = Germany) |
| `ltn_number` | string | Yes | KBA number to look up (e.g., `0588549`) |
| `number_type` | integer | Yes | Number type — use `1` for KBA numbers |

**Query Params:** None

**Request Body:** None

**Response**

- Status: `200 OK`
- Response Time: ~671 ms
- Body Size: 2 Bytes (headers only, body is JSON array)

```json
[
  {
    "manufacturerName": "AUDI",
    "modelName": "80 B4 Avant (8C5)",
    "typeEngineName": "2.8 quattro",
    "bodyType": "Estate",
    "constructionIntervalStart": "1992-08-01",
    "constructionIntervalEnd": "1995-07-01",
    "powerKw": "128.0000",
    "powerPs": "174.0000",
    "capacityTax": "2771.0000"
  }
]
```

**Response Fields**

| Field | Type | Description |
|-------|------|-------------|
| `manufacturerName` | string | Brand name (e.g., `"AUDI"`) |
| `modelName` | string | Full model name with body type and chassis code |
| `typeEngineName` | string | Engine/trim label (e.g., `"2.8 quattro"`) |
| `bodyType` | string | Body style (e.g., `"Estate"`, `"Hatchback"`, `"Saloon"`) |
| `constructionIntervalStart` | string (date) | Production start date in `YYYY-MM-DD` format |
| `constructionIntervalEnd` | string (date) | Production end date in `YYYY-MM-DD` format |
| `powerKw` | string (decimal) | Engine power in kilowatts |
| `powerPs` | string (decimal) | Engine power in PS (metric horsepower) |
| `capacityTax` | string (decimal) | Engine displacement in cc used for tax calculation |

**Notes**

- KBA numbers are German vehicle identification codes issued by the Kraftfahrtbundesamt (Federal Motor Transport Authority)
- `number_type: 1` is used for KBA lookups — other values may support different number formats
- Returns an **array** — a single KBA number can match multiple vehicles if the same code was assigned to multiple trims
- Power and capacity fields are returned as **decimal strings** (e.g., `"128.0000"`) — cast to float as needed
- Use `country_id: 63` (Germany) and `lang_id: 4` (English GB) for standard German KBA lookups

---

### 16. GET  Vehicles by License Plate (Netherlands / Kenteken)

**Description:** Looks up a passenger car by its Dutch license plate number (Kenteken). Uses the same endpoint as KBA lookup but with `number-type: 2`. Returns vehicle details including manufacturer, model, engine, body type, production interval, and power output.

**Auth Required:** Yes (RapidAPI key)

**Request**

- Method: `GET`
- URL: `https://tecdoc-catalog.p.rapidapi.com/types/searching-the-passenger-car-by-ltn-number/lang-id/{lang_id}/country-filter-id/{country_id}/ltn-number/{ltn_number}/number-type/{number_type}`
- Headers:
  - `x-rapidapi-host: tecdoc-catalog.p.rapidapi.com`
  - `x-rapidapi-key: <YOUR_RAPIDAPI_KEY>`

**Path Parameters**

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `lang_id` | integer | Yes | Language ID for response labels (e.g., `4` = English GB) |
| `country_id` | integer | Yes | Country filter ID (e.g., `63` = Germany) |
| `ltn_number` | string | Yes | Dutch license plate (Kenteken) to look up (e.g., `2VXT04`) |
| `number_type` | integer | Yes | Number type — use `2` for Dutch license plates |

**Query Params:** None

**Request Body:** None

**Response**

- Status: `200 OK`
- Response Time: ~1017 ms
- Body Size: 2 Bytes (headers only, body is JSON array)

```json
[
  {
    "manufacturerName": "OPEL",
    "modelName": "COMBO Box Body/MPV (X12)",
    "typeEngineName": "1.3 CDTI (B05)",
    "bodyType": "Box Body/MPV",
    "constructionIntervalStart": "2012-02-01",
    "constructionIntervalEnd": null,
    "powerKw": "66.0000",
    "powerPs": "90.0000",
    "capacityTax": null
  }
]
```

**Response Fields**

| Field | Type | Description |
|-------|------|-------------|
| `manufacturerName` | string | Brand name (e.g., `"OPEL"`) |
| `modelName` | string | Full model name with body type and chassis code |
| `typeEngineName` | string | Engine/trim label (e.g., `"1.3 CDTI (B05)"`) |
| `bodyType` | string | Body style (e.g., `"Box Body/MPV"`, `"Hatchback"`, `"Estate"`) |
| `constructionIntervalStart` | string (date) | Production start date in `YYYY-MM-DD` format |
| `constructionIntervalEnd` | string (date) \| null | Production end date, or `null` if still in production |
| `powerKw` | string (decimal) | Engine power in kilowatts |
| `powerPs` | string (decimal) | Engine power in PS (metric horsepower) |
| `capacityTax` | string (decimal) \| null | Engine displacement in cc for tax calculation, or `null` if unavailable |

**Notes**

- Same endpoint as [#15 KBA lookup](#15-get-vehicles-by-kba-number-germany) — only `number_type` and `ltn_number` differ
- `number_type: 2` targets Dutch Kenteken (license plate) format
- Dutch license plates follow formats like `2VXT04`, `AB-123-C` — pass without dashes
- `constructionIntervalEnd: null` means the vehicle is still in active production
- `capacityTax: null` indicates the displacement data is not available for this record
- Returns an **array** — a plate can theoretically match multiple records if reassigned

---

### 17. GET  Part Criteria for Vehicle

**Description:** Returns the technical criteria (specifications) for articles (parts) that match a given vehicle, product group, and supplier. Each article can have multiple criteria entries covering electrical, physical, and classification attributes. Used to compare or filter parts by spec before selection.

**Auth Required:** Yes (RapidAPI key)

**Request**

- Method: `GET`
- URL: `https://tecdoc-catalog.p.rapidapi.com/articles/selection-of-the-criteria-for-articles-and-vehicle/type-id/{type_id}/product-id/{product_id}/vehicle-id/{vehicle_id}/supplier-id/{supplier_id}/lang-id/{lang_id}/country-filter-id/{country_id}`
- Headers:
  - `x-rapidapi-host: tecdoc-catalog.p.rapidapi.com`
  - `x-rapidapi-key: <YOUR_RAPIDAPI_KEY>`

**Path Parameters**

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `type_id` | integer | Yes | Vehicle type ID (e.g., `1` = Passenger Car) |
| `product_id` | integer | Yes | Product group / generic article ID (e.g., `1` = Battery) |
| `vehicle_id` | integer | Yes | TecDoc vehicle ID (e.g., `108275`) |
| `supplier_id` | integer | Yes | Supplier/brand ID to filter results (e.g., `434`) |
| `lang_id` | integer | Yes | Language ID for criteria labels (e.g., `4` = English GB) |
| `country_id` | integer | Yes | Country filter ID (e.g., `63` = Germany) |

**Query Params:** None

**Request Body:** None

**Response**

- Status: `200 OK`
- Response Time: ~1065 ms
- Body Size: 2 Bytes (headers only, body is JSON object)

```json
{
  "countArticles": 27,
  "articles": [
    {
      "articleId": 6522838,
      "criteriaName": "Voltage [V]",
      "criteriaValue": "12",
      "type": "MANDATORY,ONLY_ARTICLE"
    },
    {
      "articleId": 6522838,
      "criteriaName": "Cold-test Current, EN [A]",
      "criteriaValue": "540",
      "type": "OPTIONAL,ONLY_ARTICLE"
    },
    {
      "articleId": 6522838,
      "criteriaName": "Battery Capacity [Ah]",
      "criteriaValue": "53",
      "type": "MANDATORY,ONLY_ARTICLE"
    },
    {
      "articleId": 6522838,
      "criteriaName": "Length [mm]",
      "criteriaValue": "207",
      "type": "OPTIONAL,ONLY_ARTICLE"
    },
    {
      "articleId": 6522838,
      "criteriaName": "Width [mm]",
      "criteriaValue": "175",
      "type": "OPTIONAL,ONLY_ARTICLE"
    },
    {
      "articleId": 6522838,
      "criteriaName": "Height [mm]",
      "criteriaValue": "190",
      "type": "OPTIONAL,ONLY_ARTICLE"
    },
    {
      "articleId": 6522838,
      "criteriaName": "Terminal Type",
      "criteriaValue": "EN",
      "type": "OPTIONAL"
    },
    {
      "articleId": 6522838,
      "criteriaName": "Hold-down Type",
      "criteriaValue": "13",
      "type": "OPTIONAL"
    },
    {
      "articleId": 6522838,
      "criteriaName": "Post Positions",
      "criteriaValue": "20",
      "type": "OPTIONAL"
    }
  ]
}
```

> Full response has **27 criteria entries** across 3 articles — truncated above to first article only.

**Response Fields**

| Field | Type | Description |
|-------|------|-------------|
| `countArticles` | integer | Total number of criteria entries across all matched articles |
| `articles` | array | Flat list of criteria entries — one object per criterion per article |
| `articleId` | integer | TecDoc article ID the criterion belongs to |
| `criteriaName` | string | Human-readable criterion label including unit (e.g., `"Voltage [V]"`, `"Length [mm]"`) |
| `criteriaValue` | string | Value for this criterion as a string (numeric or text) |
| `type` | string | Comma-separated flags indicating importance and scope (see type flags below) |

**Criteria `type` Flags**

| Flag | Meaning |
|------|---------|
| `MANDATORY` | Required spec — must match for the part to fit |
| `OPTIONAL` | Supplementary spec — informational only |
| `ONLY_ARTICLE` | Criterion applies to the article itself (not vehicle-fitment logic) |

**Notes**

- The response is a **flat list** — group by `articleId` to get the full spec sheet per part
- `countArticles` reflects the total number of criteria rows, not the number of distinct articles — divide by criteria-per-article to estimate unique parts
- `criteriaName` includes the unit in brackets (e.g., `[V]`, `[Ah]`, `[mm]`, `[A]`) — parse or strip as needed
- `criteriaValue` is always a string — cast to number where appropriate
- `type` can be a single flag (`"OPTIONAL"`) or a comma-separated combination (`"MANDATORY,ONLY_ARTICLE"`)
- Use this endpoint after retrieving article IDs to build a spec comparison table before presenting parts to the user

---

### 18. GET  TypeId by VehicleId and ManufacturerId

**Description:** Resolves the vehicle type ID (`typeId`) and type name for a given vehicle ID and manufacturer ID. Used to determine which vehicle category (e.g., Passenger Car, Commercial Vehicle) a specific vehicle belongs to before making type-dependent API calls.

**Auth Required:** Yes (RapidAPI key)

**Request**

- Method: `GET`
- URL: `https://tecdoc-catalog.p.rapidapi.com/types/get-typeid-by-vehicleid`
- Headers:
  - `x-rapidapi-host: tecdoc-catalog.p.rapidapi.com`
  - `x-rapidapi-key: <YOUR_RAPIDAPI_KEY>`

**Query Params**

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `vehicleId` | integer | Yes | TecDoc vehicle ID (e.g., `100`) |
| `manufacturerId` | integer | Yes | TecDoc manufacturer ID (e.g., `2`) |

**Request Body:** None

**Response**

- Status: `200 OK`
- Response Time: ~1056 ms
- Body Size: 2 Bytes (headers only, body is JSON array)

```json
[
  {
    "typeId": 1,
    "vehicleType": "PC"
  }
]
```

**Response Fields**

| Field | Type | Description |
|-------|------|-------------|
| `typeId` | integer | Numeric vehicle type ID used as a parameter in other TecDoc endpoints |
| `vehicleType` | string | Short vehicle type code (e.g., `"PC"` = Passenger Car) |

**Known `vehicleType` Values**

| Code | Meaning |
|------|---------|
| `PC` | Passenger Car |
| `CV` | Commercial Vehicle |
| `MC` | Motorcycle |
| `AX` | Axle / Trailer |
| `ENG` | Engine |

**Notes**

- This is a **utility lookup** — use it when you only have a `vehicleId` and need the `typeId` before calling type-dependent endpoints (e.g., parts search, criteria)
- Returns an **array** but typically contains a single entry
- `typeId: 1` = Passenger Car (`PC`) is the most common result for standard vehicle IDs
- Both `vehicleId` and `manufacturerId` are required — passing only one will likely return an empty array

---

### 19. GET  Search Articles by Article No

**Description:** Searches for parts by article number (OEM or supplier reference). Returns matching articles with product name, supplier info, and a direct image URL. Useful for looking up a specific part when the article number is already known.

**Auth Required:** Yes (RapidAPI key)

**Request**

- Method: `GET`
- URL: `https://tecdoc-catalog.p.rapidapi.com/artlookup/search-articles-by-article-no`
- Headers:
  - `x-rapidapi-host: tecdoc-catalog.p.rapidapi.com`
  - `x-rapidapi-key: <YOUR_RAPIDAPI_KEY>`

**Query Params**

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `articleNo` | string | Yes | Article number to search (e.g., `0 242 236 561`). URL-encode spaces as `+` |
| `articleType` | string | Yes | Search mode — use `ArticleNumber` for direct part number lookup |
| `langId` | integer | Yes | Language ID for product name labels (e.g., `4` = English GB) |

**Request Body:** None

**Response**

- Status: `200 OK`
- Response Time: ~655 ms
- Body Size: 2 Bytes (headers only, body is JSON object)

```json
{
  "countArticles": 1,
  "articles": [
    {
      "articleSearchNo": "0 242 236 561",
      "articleId": 18068,
      "articleNo": "0 242 236 561",
      "articleProductName": "Spark Plug",
      "supplierName": "BOSCH",
      "supplierId": 30,
      "articleMediaType": "JPEG",
      "articleMediaFileName": "5a3c2f64ca542c51697df1749eea8e751ffcc2b3.webp",
      "s3image": "https://fsn1.your-objectstorage.com/tecdoc2025/media_files/images/30/5a3c2f64ca542c51697df1749eea8e751ffcc2b3.webp"
    }
  ]
}
```

**Response Fields**

| Field | Type | Description |
|-------|------|-------------|
| `countArticles` | integer | Total number of matched articles |
| `articles` | array | List of matched article objects |
| `articleSearchNo` | string | The article number as matched in the search index |
| `articleId` | integer | TecDoc internal article ID — use in downstream part detail endpoints |
| `articleNo` | string | Canonical article number from the supplier |
| `articleProductName` | string | Generic product category name (e.g., `"Spark Plug"`) |
| `supplierName` | string | Brand/supplier name (e.g., `"BOSCH"`) |
| `supplierId` | integer | TecDoc supplier ID — use to filter by brand in other endpoints |
| `articleMediaType` | string | Original image format before conversion (e.g., `"JPEG"`) |
| `articleMediaFileName` | string | Image filename stored in S3 (`.webp` format) |
| `s3image` | string | Direct public URL to the part image in WebP format |

**Notes**

- URL-encode spaces in `articleNo` as `+` (e.g., `0+242+236+561`)
- `articleMediaType` reflects the **original** format — actual served file is always `.webp`
- `s3image` is a direct CDN URL — can be used in `<img>` tags without additional processing
- `articleId` is the key identifier for downstream calls (e.g., part details, criteria, OE numbers)
- `supplierId` can be reused in vehicle-parts endpoints to filter results by this brand

---

### 20. GET  Search Articles by OEM No

**Description:** Searches for aftermarket parts that match a given OEM (Original Equipment Manufacturer) reference number. Uses the same endpoint as [#19](#19-get-search-articles-by-article-no) but with `articleType=OENumber`. Returns all supplier articles cross-referenced to that OEM number, potentially from multiple brands.

**Auth Required:** Yes (RapidAPI key)

**Request**

- Method: `GET`
- URL: `https://tecdoc-catalog.p.rapidapi.com/artlookup/search-articles-by-article-no`
- Headers:
  - `x-rapidapi-host: tecdoc-catalog.p.rapidapi.com`
  - `x-rapidapi-key: <YOUR_RAPIDAPI_KEY>`

**Query Params**

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `articleNo` | string | Yes | OEM reference number to search (e.g., `1001`) |
| `articleType` | string | Yes | Must be `OENumber` to search by OEM cross-reference |
| `langId` | integer | Yes | Language ID for product name labels (e.g., `4` = English GB) |

**Request Body:** None

**Response**

- Status: `200 OK`
- Response Time: ~1059 ms
- Body Size: 2 Bytes (headers only, body is JSON object)

```json
{
  "countArticles": 8,
  "articles": [
    {
      "articleSearchNo": "1001",
      "articleId": 3229594,
      "articleNo": "41490",
      "articleProductName": "Paint",
      "supplierName": "MOTIP",
      "supplierId": 168,
      "articleMediaType": "JPEG",
      "articleMediaFileName": "40de504086fc82255bda3c43d64097dc0360f10e.webp",
      "s3image": "https://fsn1.your-objectstorage.com/tecdoc2025/media_files/images/168/40de504086fc82255bda3c43d64097dc0360f10e.webp"
    },
    {
      "articleSearchNo": "1001",
      "articleId": 25114596,
      "articleNo": "MV OP8344",
      "articleProductName": "Oil Pump",
      "supplierName": "MV Parts",
      "supplierId": 5645,
      "articleMediaType": null,
      "articleMediaFileName": null,
      "s3image": null
    }
  ]
}
```

> Full response has **8 articles** across multiple suppliers — truncated above to first and last entries.

**Response Fields**

| Field | Type | Description |
|-------|------|-------------|
| `countArticles` | integer | Total number of aftermarket articles matched to this OEM number |
| `articles` | array | List of matched article objects |
| `articleSearchNo` | string | The OEM number as matched in the search index |
| `articleId` | integer | TecDoc internal article ID — use in downstream part detail endpoints |
| `articleNo` | string | Supplier's own article number (differs from the OEM search number) |
| `articleProductName` | string | Generic product category name (e.g., `"Spark Plug"`, `"Oil Pump"`) |
| `supplierName` | string | Brand/supplier name (e.g., `"BOSCH"`, `"MOTIP"`) |
| `supplierId` | integer | TecDoc supplier ID |
| `articleMediaType` | string \| null | Original image format before conversion, or `null` if no image |
| `articleMediaFileName` | string \| null | Image filename in S3 (`.webp`), or `null` if no image |
| `s3image` | string \| null | Direct public CDN URL to the part image, or `null` if unavailable |

**Notes**

- Same endpoint as [#19](#19-get-search-articles-by-article-no) — only `articleType` differs (`OENumber` vs `ArticleNumber`)
- OEM numbers are manufacturer reference codes (e.g., Bosch, Valeo, Denso part numbers used by vehicle makers)
- A single OEM number can match articles from **many different aftermarket suppliers** — expect multiple results
- `articleNo` in the response is the **supplier's own number**, not the OEM number searched
- `articleMediaType`, `articleMediaFileName`, and `s3image` can all be `null` — always null-check before rendering images
- Short or generic OEM numbers (e.g., `"1001"`) may return unrelated parts from different product categories — prefer full, specific OEM numbers for accurate results

---

### 21. GET  Search Articles by EAN No

**Description:** Searches for a part by its EAN (European Article Number / barcode). Uses the same endpoint as [#19](#19-get-search-articles-by-article-no) and [#20](#20-get-search-articles-by-oem-no) but with `articleType=EAN`. EAN is a globally unique barcode — typically returns a single exact match.

**Auth Required:** Yes (RapidAPI key)

**Request**

- Method: `GET`
- URL: `https://tecdoc-catalog.p.rapidapi.com/artlookup/search-articles-by-article-no`
- Headers:
  - `x-rapidapi-host: tecdoc-catalog.p.rapidapi.com`
  - `x-rapidapi-key: <YOUR_RAPIDAPI_KEY>`

**Query Params**

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `articleNo` | string | Yes | EAN barcode number to search (e.g., `4011558383008`) |
| `articleType` | string | Yes | Must be `EAN` to search by barcode |
| `langId` | integer | Yes | Language ID for product name labels (e.g., `4` = English GB) |

**Request Body:** None

**Response**

- Status: `200 OK`
- Response Time: ~977 ms
- Body Size: 2 Bytes (headers only, body is JSON object)

```json
{
  "countArticles": 1,
  "articles": [
    {
      "articleSearchNo": "4011558383008",
      "articleId": 6159438,
      "articleNo": "C 2029",
      "articleProductName": "Air Filter",
      "supplierName": "MANN-FILTER",
      "supplierId": 4,
      "articleMediaType": "JPG",
      "articleMediaFileName": "5e27f118885fa0253374358b3585240c6c9a53af.webp",
      "s3image": "https://fsn1.your-objectstorage.com/tecdoc2025/media_files/images/4/5e27f118885fa0253374358b3585240c6c9a53af.webp"
    }
  ]
}
```

**Response Fields**

| Field | Type | Description |
|-------|------|-------------|
| `countArticles` | integer | Total number of matched articles (typically `1` for EAN) |
| `articles` | array | List of matched article objects |
| `articleSearchNo` | string | The EAN barcode as matched in the search index |
| `articleId` | integer | TecDoc internal article ID — use in downstream part detail endpoints |
| `articleNo` | string | Supplier's own article number (e.g., `"C 2029"`) |
| `articleProductName` | string | Generic product category name (e.g., `"Air Filter"`) |
| `supplierName` | string | Brand/supplier name (e.g., `"MANN-FILTER"`) |
| `supplierId` | integer | TecDoc supplier ID |
| `articleMediaType` | string \| null | Original image format before conversion (e.g., `"JPG"`) |
| `articleMediaFileName` | string \| null | Image filename in S3 (`.webp`), or `null` if no image |
| `s3image` | string \| null | Direct public CDN URL to the part image, or `null` if unavailable |

**Notes**

- Same endpoint as [#19](#19-get-search-articles-by-article-no) and [#20](#20-get-search-articles-by-oem-no) — only `articleType` differs (`EAN`)
- EAN is a globally unique 13-digit barcode — searches are highly precise and almost always return `countArticles: 1`
- `articleNo` in the response is the **supplier's own part number**, not the EAN
- EAN lookup is the most reliable of the three search modes — use it when a barcode scan is available
- `articleMediaType` reflects the original upload format — the served file is always `.webp`

---

### 22. GET  Search Articles by IAM No

**Description:** Searches for parts by IAM number (Independent Aftermarket number — a supplier's own part reference). Uses the same endpoint as [#19](#19-get-search-articles-by-article-no)–[#21](#21-get-search-articles-by-ean-no) but with `articleType=IAMNumber`. Because many aftermarket suppliers share cross-references to the same IAM number, this search typically returns the largest result set of the four article search modes.

**Auth Required:** Yes (RapidAPI key)

**Request**

- Method: `GET`
- URL: `https://tecdoc-catalog.p.rapidapi.com/artlookup/search-articles-by-article-no`
- Headers:
  - `x-rapidapi-host: tecdoc-catalog.p.rapidapi.com`
  - `x-rapidapi-key: <YOUR_RAPIDAPI_KEY>`

**Query Params**

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `articleNo` | string | Yes | IAM part number to search (e.g., `0 242 236 561`). URL-encode spaces as `+` |
| `articleType` | string | Yes | Must be `IAMNumber` to search by aftermarket part number |
| `langId` | integer | Yes | Language ID for product name labels (e.g., `4` = English GB) |

**Request Body:** None

**Response**

- Status: `200 OK`
- Response Time: ~664 ms
- Body Size: 2 Bytes (headers only, body is JSON object)

```json
{
  "countArticles": 35,
  "articles": [
    {
      "articleSearchNo": "0242236561",
      "articleId": 541207,
      "articleNo": "062609000031",
      "articleProductName": "Spark Plug",
      "supplierName": "MAGNETI MARELLI",
      "supplierId": 95,
      "articleMediaType": null,
      "articleMediaFileName": null,
      "s3image": null
    },
    {
      "articleSearchNo": "0 242 236 561",
      "articleId": 2974346,
      "articleNo": "3696",
      "articleProductName": "Spark Plug",
      "supplierName": "NGK",
      "supplierId": 15,
      "articleMediaType": "GIF",
      "articleMediaFileName": "050af6526c6206cbed165226d9765c2ac78a0003.gif",
      "s3image": "https://fsn1.your-objectstorage.com/tecdoc2025/media_files/images/15/050af6526c6206cbed165226d9765c2ac78a0003.gif"
    },
    {
      "articleSearchNo": "0 242 236 561",
      "articleId": 98689134,
      "articleNo": "Z154",
      "articleProductName": "Spark Plug",
      "supplierName": "BorgWarner (BERU)",
      "supplierId": 11,
      "articleMediaType": null,
      "articleMediaFileName": null,
      "s3image": null
    }
  ]
}
```

> Full response has **35 articles** across multiple suppliers — truncated above to 3 representative entries.

**Response Fields**

| Field | Type | Description |
|-------|------|-------------|
| `countArticles` | integer | Total number of matched aftermarket articles |
| `articles` | array | List of matched article objects |
| `articleSearchNo` | string | The IAM number as matched — may appear with or without spaces depending on index normalisation |
| `articleId` | integer | TecDoc internal article ID — use in downstream part detail endpoints |
| `articleNo` | string | Supplier's own article number |
| `articleProductName` | string | Generic product category name (e.g., `"Spark Plug"`) |
| `supplierName` | string | Brand/supplier name (e.g., `"NGK"`, `"HELLA"`, `"DENSO"`) |
| `supplierId` | integer | TecDoc supplier ID |
| `articleMediaType` | string \| null | Original image format (e.g., `"JPEG"`, `"GIF"`), or `null` if no image |
| `articleMediaFileName` | string \| null | Image filename in S3, or `null` if no image. May be `.webp` or `.gif` |
| `s3image` | string \| null | Direct public CDN URL to the part image, or `null` if unavailable |

**Notes**

- Same endpoint as [#19](#19-get-search-articles-by-article-no)–[#21](#21-get-search-articles-by-ean-no) — only `articleType=IAMNumber` differs
- IAM searches return the **most results** of the four modes — a popular part number can match 30+ articles across brands such as NGK, HELLA, DENSO, CHAMPION, BOSCH, etc.
- `articleSearchNo` normalisation is inconsistent — the same search may return entries with and without spaces (e.g., `"0242236561"` and `"0 242 236 561"`) — treat them as equivalent
- `articleMediaFileName` may be `.gif` (not `.webp`) for some older supplier images — do not assume all images are `.webp`
- URL-encode spaces in `articleNo` as `+` (e.g., `0+242+236+561`)
- Use this mode when the user provides a generic aftermarket part number and you want to find all cross-referenced alternatives across suppliers

---

### 23. GET  Search Articles by Trade No

**Description:** Searches for parts by trade number (distributor or wholesaler reference). Uses the same endpoint as [#19](#19-get-search-articles-by-article-no)–[#22](#22-get-search-articles-by-iam-no) but with `articleType=TradeNumber`. Trade numbers are less commonly indexed in TecDoc — queries may return `null` results even for valid part numbers.

**Auth Required:** Yes (RapidAPI key)

**Request**

- Method: `GET`
- URL: `https://tecdoc-catalog.p.rapidapi.com/artlookup/search-articles-by-article-no`
- Headers:
  - `x-rapidapi-host: tecdoc-catalog.p.rapidapi.com`
  - `x-rapidapi-key: <YOUR_RAPIDAPI_KEY>`

**Query Params**

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `articleNo` | string | Yes | Trade number to search (e.g., `0 242 236 561`). URL-encode spaces as `+` |
| `articleType` | string | Yes | Must be `TradeNumber` to search by trade/distributor reference |
| `langId` | integer | Yes | Language ID for product name labels (e.g., `4` = English GB) |

**Request Body:** None

**Response**

- Status: `200 OK`
- Response Time: ~1278 ms
- Body Size: 2 Bytes (headers only, body is JSON object)

```json
{
  "countArticles": null,
  "articles": null
}
```

**Response Fields**

| Field | Type | Description |
|-------|------|-------------|
| `countArticles` | integer \| null | Total number of matched articles, or `null` if no trade number index match |
| `articles` | array \| null | List of matched article objects, or `null` if no results found |

**Notes**

- Same endpoint as [#19](#19-get-search-articles-by-article-no)–[#22](#22-get-search-articles-by-iam-no) — only `articleType=TradeNumber` differs
- Trade numbers are distributor or wholesaler-assigned references — coverage in TecDoc is sparse compared to ArticleNumber, OENumber, EAN, or IAMNumber
- Both `countArticles` and `articles` return `null` (not an empty array) when no match is found — **always null-check both fields before use**
- A `200 OK` with `null` body fields is a valid "no results" response — do not treat it as an error
- Response time (~1278 ms) is notably slower than other search modes despite returning no data
- Try falling back to `IAMNumber` or `ArticleNumber` mode if `TradeNumber` returns null

---

### 24. POST  Article Details by Article No

**Description:** Returns full article details for a given article number — including product info, all technical specifications, EAN barcode, OEM cross-references, compatible vehicles, and a direct image URL. This is the richest article endpoint, combining data from multiple lookup endpoints into a single response.

**Auth Required:** Yes (RapidAPI key)

**Request**

- Method: `POST`
- URL: `https://tecdoc-catalog.p.rapidapi.com/articles/article-number-details`
- Headers:
  - `x-rapidapi-host: tecdoc-catalog.p.rapidapi.com`
  - `x-rapidapi-key: <YOUR_RAPIDAPI_KEY>`
  - `Content-Type: application/json`

**Request Body**

```json
{
  "articleNo": "C 2029",
  "langId": 4
}
```

**Request Body Fields**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `articleNo` | string | Yes | Supplier article number to look up (e.g., `"C 2029"`) |
| `langId` | integer | Yes | Language ID for labels (e.g., `4` = English GB) |

**Query Params:** None

**Response**

- Status: `200 OK`
- Response Time: ~966 ms
- Body Size: 2 Bytes (headers only, body is JSON object)

```json
{
  "articleNo": "C 2029",
  "countArticles": 1,
  "articles": [
    {
      "articleId": 6159438,
      "articleNo": "C 2029",
      "articleProductName": "Air Filter",
      "supplierName": "MANN-FILTER",
      "supplierId": 4,
      "articleMediaType": "JPG",
      "articleMediaFileName": "5e27f118885fa0253374358b3585240c6c9a53af.webp",
      "articleInfo": {
        "articleId": 6159438,
        "articleNo": "C 2029",
        "supplierId": 4,
        "supplierName": "MANN-FILTER",
        "isAccessory": 0,
        "articleProductName": "Air Filter"
      },
      "allSpecifications": [
        { "criteriaName": "Length [mm]", "criteriaValue": "190" },
        { "criteriaName": "Width [mm]",  "criteriaValue": "200" },
        { "criteriaName": "Height [mm]", "criteriaValue": "50" },
        { "criteriaName": "Filter type", "criteriaValue": "9" }
      ],
      "eanNo": {
        "eanNumbers": "4011558383008"
      },
      "oemNo": [
        { "oemBrand": "HYUNDAI (BEIJING)", "oemDisplayNo": "28113-0Q000" },
        { "oemBrand": "HYUNDAI",           "oemDisplayNo": "28113-2H000" }
      ],
      "compatibleCars": [
        {
          "vehicleId": 4851,
          "modelId": 6234,
          "manufacturerName": "KIA",
          "modelName": "CEE'D SW (ED)",
          "typeEngineName": "1.4 CVVT",
          "constructionIntervalStart": "2009-07-01",
          "constructionIntervalEnd": "2012-12-01"
        }
      ],
      "s3image": "https://fsn1.your-objectstorage.com/tecdoc2025/media_files/images/4/5e27f118885fa0253374358b3585240c6c9a53af.webp"
    }
  ]
}
```

> `compatibleCars` in this example had **90+ vehicles** — truncated above to 1 entry for brevity.

**Response Fields — Top Level**

| Field | Type | Description |
|-------|------|-------------|
| `articleNo` | string | The article number echoed from the request |
| `countArticles` | integer | Number of matched articles |
| `articles` | array | List of full article detail objects |

**Response Fields — Article Object**

| Field | Type | Description |
|-------|------|-------------|
| `articleId` | integer | TecDoc internal article ID |
| `articleNo` | string | Supplier article number |
| `articleProductName` | string | Generic product category name |
| `supplierName` | string | Brand/supplier name |
| `supplierId` | integer | TecDoc supplier ID |
| `articleMediaType` | string \| null | Original image format (e.g., `"JPG"`) |
| `articleMediaFileName` | string \| null | Image filename in S3 (`.webp`) |
| `s3image` | string \| null | Direct CDN URL to part image |
| `articleInfo` | object | Duplicate summary of core article fields (see below) |
| `allSpecifications` | array | List of technical criteria objects `{criteriaName, criteriaValue}` |
| `eanNo` | object | EAN barcode info — `{ "eanNumbers": "<barcode>" }` |
| `oemNo` | array | OEM cross-references — `[{ oemBrand, oemDisplayNo }]` |
| `compatibleCars` | array | All vehicles this part fits (see below) |

**Response Fields — `articleInfo`**

| Field | Type | Description |
|-------|------|-------------|
| `articleId` | integer | Same as parent article ID |
| `articleNo` | string | Same as parent article number |
| `supplierId` | integer | Supplier ID |
| `supplierName` | string | Supplier name |
| `isAccessory` | integer | `0` = primary part, `1` = accessory |
| `articleProductName` | string | Generic product category name |

**Response Fields — `compatibleCars` items**

| Field | Type | Description |
|-------|------|-------------|
| `vehicleId` | integer | TecDoc vehicle ID — use in parts lookup endpoints |
| `modelId` | integer | TecDoc model ID |
| `manufacturerName` | string | Brand name (e.g., `"KIA"`, `"HYUNDAI"`) |
| `modelName` | string | Full model name with body type and chassis code |
| `typeEngineName` | string | Engine/trim label |
| `constructionIntervalStart` | string (date) | Production start date in `YYYY-MM-DD` format |
| `constructionIntervalEnd` | string (date) \| null | Production end date, or `null` if still in production |

**Notes**

- This is the **most comprehensive single article endpoint** — returns specs, EAN, OEM numbers, and full vehicle compatibility in one call
- `compatibleCars` can be very large (90+ entries for popular parts) — consider paginating or filtering on the client side
- `articleInfo` duplicates several top-level fields — it appears to be a legacy sub-object; prefer top-level fields
- `eanNo.eanNumbers` is a **string**, not an array — even if multiple EANs exist they may be comma-separated or the field may only return one
- `oemNo` lists OEM part numbers by brand — useful for cross-referencing to OE catalogues
- `constructionIntervalEnd: null` in `compatibleCars` means the vehicle trim is still in active production
- `allSpecifications` `criteriaName` includes units in brackets — strip brackets for display if needed

---

### 25. GET  List All Suppliers

**Description:** Returns the complete list of all aftermarket part suppliers in the TecDoc catalog, each with a unique ID, display name, parent company match code, logo filename, and a direct CDN URL to the supplier logo image.

**Auth Required:** Yes (RapidAPI key)

**Request**

- Method: `GET`
- URL: `<!-- TODO: confirm URL from RapidAPI dashboard -->`
- Headers:
  - `x-rapidapi-host: tecdoc-catalog.p.rapidapi.com`
  - `x-rapidapi-key: <YOUR_RAPIDAPI_KEY>`

**Query Params:** None

**Request Body:** None

**Response**

- Status: `200 OK`

```json
[
  {
    "supplierId": 1,
    "supplierName": "SPIDAN",
    "supplierMatchCode": "GKN (SPIDAN)",
    "supplierLogoName": "SPIDAN.PNG",
    "s3image": "https://fsn1.your-objectstorage.com/tecdoc2025/suppliers_logo/SPIDAN.PNG"
  },
  {
    "supplierId": 2,
    "supplierName": "HELLA",
    "supplierMatchCode": "HELLA",
    "supplierLogoName": "HELLA.PNG",
    "s3image": "https://fsn1.your-objectstorage.com/tecdoc2025/suppliers_logo/HELLA.PNG"
  },
  {
    "supplierId": 30,
    "supplierName": "BOSCH",
    "supplierMatchCode": "Robert Bosch GmbH",
    "supplierLogoName": "BOSCH.PNG",
    "s3image": "https://fsn1.your-objectstorage.com/tecdoc2025/suppliers_logo/BOSCH.PNG"
  },
  {
    "supplierId": 66,
    "supplierName": "DENSO",
    "supplierMatchCode": "DENSO Europe B.V.",
    "supplierLogoName": "DENSO.PNG",
    "s3image": "https://fsn1.your-objectstorage.com/tecdoc2025/suppliers_logo/DENSO.PNG"
  }
]
```

> Full response contains **300+ suppliers** — truncated above to 4 representative entries.

**Response Fields**

| Field | Type | Description |
|-------|------|-------------|
| `supplierId` | integer | TecDoc unique supplier ID — use in parts search and filter endpoints |
| `supplierName` | string | Brand/trade name as displayed in the catalog (e.g., `"BOSCH"`, `"MANN-FILTER"`) |
| `supplierMatchCode` | string | Parent company or legal entity name — useful for grouping brands under the same corporate owner |
| `supplierLogoName` | string | Filename of the supplier logo in PNG format (e.g., `"BOSCH.PNG"`) |
| `s3image` | string | Direct public CDN URL to the supplier logo PNG image |

**Notes**

- Returns a flat **array** with no wrapper object — iterate directly
- `supplierId` values are not sequential — IDs are sparse (gaps exist between entries)
- `supplierMatchCode` can reveal corporate relationships — e.g., `"SWF"`, `"FTE"`, and `"VALEO"` all share `"Valeo Service"` as their match code
- Multiple `supplierName` brands may share the same `supplierMatchCode` (same parent company, different sub-brands)
- Logo images are hosted at `https://fsn1.your-objectstorage.com/tecdoc2025/suppliers_logo/` — filenames may contain spaces (e.g., `"Schaeffler LuK.PNG"`) so URL-encode when building image URLs
- Use this endpoint to build a **brand filter UI** — cache the result as it changes infrequently

---

### 26. POST  Get OEM by Article ID

**Description:** Returns OEM (Original Equipment Manufacturer) cross-reference numbers for a batch of article IDs in a single request. Useful for bulk OEM lookups without calling a per-article endpoint repeatedly.

**Auth Required:** Yes (RapidAPI key)

**Request**

- Method: `POST`
- URL: `https://tecdoc-catalog.p.rapidapi.com/articles/get-oems-by-list-of-articles-ids`
- Headers:
  - `x-rapidapi-host: tecdoc-catalog.p.rapidapi.com`
  - `x-rapidapi-key: <YOUR_RAPIDAPI_KEY>`
  - `Content-Type: application/json`

**Request Body**

```json
{
  "articleIds": [5522538, 6822931, 75733765]
}
```

**Request Body Fields**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `articleIds` | array of integers | Yes | List of TecDoc article IDs to look up OEM numbers for |

**Query Params:** None

**Response**

- Status: `200 OK`
- Response Time: ~1511 ms
- Body Size: 2 Bytes (headers only, body is JSON object)

```json
{
  "count": 3,
  "articles": [
    {
      "articleId": 5522538,
      "oemNo": [
        {
          "oemBrand": "HYUNDAI",
          "oemDisplayNo": "28113-2H000"
        }
      ]
    },
    {
      "articleId": 6822931,
      "oemNo": [
        {
          "oemBrand": "HYUNDAI",
          "oemDisplayNo": "28113-2H000"
        }
      ]
    },
    {
      "articleId": 75733765,
      "oemNo": [
        {
          "oemBrand": "HYUNDAI",
          "oemDisplayNo": "281132H000"
        },
        {
          "oemBrand": "KIA",
          "oemDisplayNo": "281132H000"
        },
        {
          "oemBrand": "HYUNDAI (BEIJING)",
          "oemDisplayNo": "281132H000"
        },
        {
          "oemBrand": "KIA (DYK)",
          "oemDisplayNo": "281132H000"
        }
      ]
    }
  ]
}
```

**Response Fields**

| Field | Type | Description |
|-------|------|-------------|
| `count` | integer | Number of articles returned in this response |
| `articles` | array | List of article OEM result objects |
| `articleId` | integer | TecDoc article ID matching the request input |
| `oemNo` | array | List of OEM cross-reference objects for this article |
| `oemBrand` | string | Vehicle manufacturer brand the OEM number belongs to (e.g., `"HYUNDAI"`, `"KIA"`) |
| `oemDisplayNo` | string | OEM part number as displayed (may include hyphens or be normalised without) |

**Notes**

- Batch endpoint — submit multiple `articleIds` in a single request to avoid N+1 API calls
- `count` reflects the number of articles in the response, not the total OEM entries
- `oemDisplayNo` formatting is **inconsistent** — the same OEM number may appear with hyphens (`"28113-2H000"`) or without (`"281132H000"`) depending on which article record it came from — normalise (strip hyphens/spaces) before comparing
- A single article can have OEM numbers from **multiple brands** — e.g., `articleId: 75733765` maps to HYUNDAI, KIA, HYUNDAI (BEIJING), and KIA (DYK) all sharing the same number
- Regional variants are listed as separate `oemBrand` entries (e.g., `"KIA (DYK)"` for China-market KIA)
- Use this endpoint after a parts search to enrich article results with OEM cross-references for display

---

## Part Info (by Article ID)

---

### 27. GET  List All Categories

**Description:** Returns the full TecDoc parts category tree as a nested object. Categories are organised hierarchically up to 4 levels deep (Level 1 = top-level group → Level 4 = specific part type). Each node contains a `categoryId`, `categoryName`, `level`, and a `children` object (empty array `[]` at leaf nodes).

**Auth Required:** Yes (RapidAPI key)

**Request**

- Method: `GET`
- URL: `<!-- TODO: confirm URL from RapidAPI dashboard -->`
- Headers:
  - `x-rapidapi-host: tecdoc-catalog.p.rapidapi.com`
  - `x-rapidapi-key: <YOUR_RAPIDAPI_KEY>`

**Query Params:** None

**Request Body:** None

**Response**

- Status: `200 OK`

```json
{
  "Accessories": {
    "categoryId": 100733,
    "categoryName": "Accessories",
    "level": 1,
    "children": {
      "Armrest": {
        "categoryId": 100860,
        "categoryName": "Armrest",
        "level": 2,
        "children": []
      },
      "Floor Mats": {
        "categoryId": 100857,
        "categoryName": "Floor Mats",
        "level": 2,
        "children": []
      }
    }
  },
  "Belt Drive": {
    "categoryId": 100016,
    "categoryName": "Belt Drive",
    "level": 1,
    "children": {
      "Timing Belt/Set": {
        "categoryId": 100085,
        "categoryName": "Timing Belt/Set",
        "level": 2,
        "children": {
          "Timing Belt": {
            "categoryId": 100452,
            "categoryName": "Timing Belt",
            "level": 3,
            "children": []
          },
          "Timing Belt Kit": {
            "categoryId": 100453,
            "categoryName": "Timing Belt Kit",
            "level": 3,
            "children": []
          }
        }
      }
    }
  },
  "Body": {
    "categoryId": 100001,
    "categoryName": "Body",
    "level": 1,
    "children": {
      "Additional Headlight/Parts": {
        "categoryId": 101340,
        "categoryName": "Additional Headlight/Parts",
        "level": 2,
        "children": {
          "Front Fog Light/Parts": {
            "categoryId": 101341,
            "categoryName": "Front Fog Light/Parts",
            "level": 3,
            "children": {
              "Fog Light Bulb": {
                "categoryId": 101343,
                "categoryName": "Fog Light Bulb",
                "level": 4,
                "children": []
              }
            }
          }
        }
      }
    }
  }
}
```

> Full response contains **many top-level categories** with hundreds of nested children — truncated above to representative entries only.

**Response Fields**

| Field | Type | Description |
|-------|------|-------------|
| *(root)* | object | Keys are category names; values are category objects |
| `categoryId` | integer | Unique TecDoc category ID — use when filtering parts by category |
| `categoryName` | string | Human-readable category name (matches the parent key) |
| `level` | integer | Depth in the hierarchy: `1` = top-level, `2` = sub-category, `3` = sub-sub-category, `4` = leaf group |
| `children` | object \| array | Nested child categories (object) or empty array `[]` at leaf nodes |

**Known Top-Level Categories (Level 1)**

| Category | `categoryId` |
|----------|-------------|
| Accessories | 100733 |
| Air Conditioning | 100243 |
| Axle Drive | 100400 |
| Axle Mounting / Steering / Wheels | 100013 |
| Belt Drive | 100016 |
| Body | 100001 |

> Many more Level 1 categories exist in the full response.

**Notes**

- The root response is a **keyed object**, not an array — iterate with `Object.entries()` or `Object.values()` to process programmatically
- `children` is an **empty array `[]`** at leaf nodes but a **keyed object** at non-leaf nodes — check `Array.isArray(children)` before recursing
- Maximum observed depth is **4 levels** (Level 1 → Level 4)
- `categoryId` values at any level can be used in part-search endpoints to filter results by category
- Cache this response — the category tree changes infrequently and is large to fetch repeatedly
- Use this endpoint to build a **category browser / drill-down navigation UI**

---

### 28. GET  List Categories by Vehicle ID (v1)

**Description:** Returns the category tree filtered specifically for a given vehicle — only categories that have parts available for that vehicle are included. Unlike [#27](#27-get-list-all-categories) which returns the full nested tree, this endpoint returns a **flat array** where each row represents one node in the hierarchy, with the full breadcrumb path encoded as numbered column pairs (`categoryName1`/`categoryId1` through `categoryName4`/`categoryId4`).

**Auth Required:** Yes (RapidAPI key)

**Request**

- Method: `GET`
- URL: `<!-- TODO: confirm URL from RapidAPI dashboard -->`
- Headers:
  - `x-rapidapi-host: tecdoc-catalog.p.rapidapi.com`
  - `x-rapidapi-key: <YOUR_RAPIDAPI_KEY>`

**Query Params**

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `vehicleId` | integer | Yes | TecDoc vehicle ID to filter categories for (e.g., `108275`) |

**Request Body:** None

**Response**

- Status: `200 OK`

```json
{
  "categories": [
    {
      "level": 1,
      "categoryName1": "Accessories",
      "categoryId1": 100733,
      "categoryName2": null,
      "categoryId2": null,
      "categoryName3": null,
      "categoryId3": null,
      "categoryName4": null,
      "categoryId4": null
    },
    {
      "level": 2,
      "categoryName1": "Accessories",
      "categoryId1": 100733,
      "categoryName2": "Floor Mats",
      "categoryId2": 100857,
      "categoryName3": null,
      "categoryId3": null,
      "categoryName4": null,
      "categoryId4": null
    },
    {
      "level": 3,
      "categoryName1": "Axle Drive",
      "categoryId1": 100400,
      "categoryName2": "Propshaft",
      "categoryId2": 100703,
      "categoryName3": "Universal Joint",
      "categoryId3": 100707,
      "categoryName4": null,
      "categoryId4": null
    },
    {
      "level": 4,
      "categoryName1": "Body",
      "categoryId1": 100001,
      "categoryName2": "Lights",
      "categoryId2": 101407,
      "categoryName3": "Direction Indicator/Parts",
      "categoryId3": 101420,
      "categoryName4": "Direction Indicator",
      "categoryId4": 101421
    }
  ]
}
```

> Full response contains **hundreds of rows** across all levels — truncated above to 4 representative entries.

**Response Fields**

| Field | Type | Description |
|-------|------|-------------|
| `categories` | array | Flat list of category breadcrumb rows |
| `level` | integer | Depth of this node: `1` = top-level, `2` = sub-category, `3` = sub-sub-category, `4` = leaf |
| `categoryName1` | string | Level 1 (top-level) category name |
| `categoryId1` | integer | Level 1 category ID |
| `categoryName2` | string \| null | Level 2 category name, or `null` if this row is at level 1 |
| `categoryId2` | integer \| null | Level 2 category ID, or `null` |
| `categoryName3` | string \| null | Level 3 category name, or `null` if this row is at level 1 or 2 |
| `categoryId3` | integer \| null | Level 3 category ID, or `null` |
| `categoryName4` | string \| null | Level 4 (leaf) category name, or `null` if this row is above level 4 |
| `categoryId4` | integer \| null | Level 4 category ID, or `null` |

**Key Difference vs #27 (List All Categories)**

| Aspect | [#27 List All Categories](#27-get-list-all-categories) | #28 List Categories by Vehicle ID |
|--------|------------------------------------------------------|----------------------------------|
| Scope | All categories in TecDoc | Only categories with parts for this vehicle |
| Format | Nested object tree | Flat array of breadcrumb rows |
| Structure | Recursive `children` object | Numbered column pairs per level |
| Use case | Build full category browser | Show relevant categories for a specific car |

**Notes**

- Each row is a **breadcrumb snapshot** — a level 4 row repeats `categoryName1`–`categoryName3` from its ancestors. Group by `categoryId1` to reconstruct the tree on the client
- The `level` field tells you which numbered column holds the **deepest** (current) category: `level: 2` means `categoryName2`/`categoryId2` is the node, `level: 3` means `categoryName3`/`categoryId3`, etc.
- Level 1 rows have `categoryName2`–`categoryName4` all `null` — they serve as group headers
- The **active/deepest category ID** for any row is `categoryId{level}` — e.g., for a `level: 3` row use `categoryId3`
- This is more useful than #27 for building a **vehicle-specific parts menu** since it only shows categories that actually have fitment data for the selected vehicle

---

### 29. GET  List Categories by Vehicle ID (v2)

**Description:** Returns the category tree scoped to a specific vehicle, in the same **nested object format** as [#27 List All Categories](#27-get-list-all-categories). Only categories that have fitment data for the given vehicle are included. This is the "best of both worlds" endpoint: vehicle-filtered scope (like #28) combined with the developer-friendly recursive tree structure (like #27).

**Auth Required:** Yes (RapidAPI key)

**Request**

- Method: `GET`
- URL: `<!-- TODO: confirm URL from RapidAPI dashboard -->`
- Headers:
  - `x-rapidapi-host: tecdoc-catalog.p.rapidapi.com`
  - `x-rapidapi-key: <YOUR_RAPIDAPI_KEY>`

**Path / Query Parameters**

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `vehicle_id` | integer | Yes | TecDoc vehicle ID (e.g., `108275`) |
| `lang_id` | integer | Yes | Language ID for category names (e.g., `4` = English GB) |
| `country_id` | integer | Yes | Country filter ID (e.g., `63` = Germany) |

> Confirm exact param names and whether they are path params or query params from the RapidAPI dashboard.

**Request Body:** None

**Response**

- Status: `200 OK`
- Response Time: ~(confirm from RapidAPI dashboard)
- Body:

```json
{
  "categories": {
    "100003": {
      "categoryId": 100003,
      "categoryName": "Engine",
      "level": 1,
      "children": {
        "100100": {
          "categoryId": 100100,
          "categoryName": "Lubrication",
          "level": 2,
          "children": {
            "100101": {
              "categoryId": 100101,
              "categoryName": "Engine Oil",
              "level": 3,
              "children": []
            },
            "100102": {
              "categoryId": 100102,
              "categoryName": "Oil Filter",
              "level": 3,
              "children": []
            }
          }
        },
        "100200": {
          "categoryId": 100200,
          "categoryName": "Cooling System",
          "level": 2,
          "children": {
            "100201": {
              "categoryId": 100201,
              "categoryName": "Water Pump",
              "level": 3,
              "children": []
            }
          }
        }
      }
    },
    "100400": {
      "categoryId": 100400,
      "categoryName": "Axle Drive",
      "level": 1,
      "children": {
        "100703": {
          "categoryId": 100703,
          "categoryName": "Propshaft",
          "level": 2,
          "children": {
            "100707": {
              "categoryId": 100707,
              "categoryName": "Universal Joint",
              "level": 3,
              "children": []
            }
          }
        }
      }
    }
  }
}
```

> Full response contains **all vehicle-relevant categories** in nested form — truncated above to 2 top-level nodes for illustration.

**Response Fields**

| Field | Type | Description |
|-------|------|-------------|
| `categories` | object | Root wrapper; keys are top-level `categoryId` strings |
| `categories[id]` | object | A category node |
| `categories[id].categoryId` | integer | Numeric category ID |
| `categories[id].categoryName` | string | Human-readable category name (language from `lang_id`) |
| `categories[id].level` | integer | Depth in tree: `1` = top-level, `2` = sub, `3` = sub-sub, etc. |
| `categories[id].children` | object \| array | Keyed object of child nodes at non-leaf levels; empty array `[]` at leaf nodes |

**Three-Way Comparison: Category Endpoints**

| Aspect | [#27 List All Categories](#27-get-list-all-categories) | [#28 List Categories by Vehicle ID (v1)](#28-get-list-categories-by-vehicle-id-v1) | #29 List Categories by Vehicle ID (v2) |
|--------|------------------------------------------------------|------------------------------------------------------------------------------------|----------------------------------------|
| Scope | All TecDoc categories | Only categories with parts for this vehicle | Only categories with parts for this vehicle |
| Format | Nested object tree | Flat array of breadcrumb rows | Nested object tree |
| Structure | Recursive `children` object | Numbered column pairs per level (`categoryId1`–`categoryId4`) | Recursive `children` object |
| Root key | `categories` (keyed object) | `categories` (array) | `categories` (keyed object) |
| Reconstruct tree? | Ready to use | Requires client-side grouping | Ready to use |
| Use case | Build full category browser | Flat list, useful for server-side filtering | Vehicle-specific parts menu (recommended) |

**Notes**

- `children` has a **type inconsistency**: non-leaf nodes use a **keyed object** (`{ "100101": {...}, "100102": {...} }`), while leaf nodes use an **empty array** (`[]`). Always check `Array.isArray(children)` before iterating
- This is the same structural quirk as [#27](#27-get-list-all-categories) — handle it the same way
- The root `categories` object is also keyed by `categoryId` string (not an array) — use `Object.values(categories)` to iterate top-level nodes
- Prefer this endpoint over #28 when you need to render a **collapsible tree UI** — the nested format eliminates the client-side grouping step required by the flat array from #28
- Prefer this endpoint over #27 when building a **vehicle-specific parts menu** — results are pre-filtered to only categories that have matching parts for the selected vehicle

---

### 30. GET  List Categories by Vehicle ID (v3)

**Description:** Returns the category tree scoped to a specific vehicle in the most **compact nested format** of all category endpoints. Like v2 (#29), only vehicle-relevant categories are included. Unlike v2, each node contains only `text` (the category name) and `children` — the category ID exists only as the object key, and there is no `level` field.

**Auth Required:** Yes (RapidAPI key)

**Request**

- Method: `GET`
- URL: `<!-- TODO: confirm URL from RapidAPI dashboard -->`
- Headers:
  - `x-rapidapi-host: tecdoc-catalog.p.rapidapi.com`
  - `x-rapidapi-key: <YOUR_RAPIDAPI_KEY>`

**Path / Query Parameters**

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `vehicle_id` | integer | Yes | TecDoc vehicle ID (e.g., `108275`) |
| `lang_id` | integer | Yes | Language ID for category names (e.g., `4` = English GB) |
| `country_id` | integer | Yes | Country filter ID (e.g., `63` = Germany) |

> Confirm exact param names and whether they are path params or query params from the RapidAPI dashboard.

**Request Body:** None

**Response**

- Status: `200 OK`
- Response Time: ~(confirm from RapidAPI dashboard)
- Body:

```json
{
  "categories": {
    "100001": {
      "text": "Body",
      "children": {
        "100216": {
          "text": "Fuel Tank/Parts",
          "children": []
        },
        "100743": {
          "text": "Body Parts/Wing/Bumper",
          "children": {
            "100185": {
              "text": "Wing/parts",
              "children": []
            },
            "100187": {
              "text": "Bumper/Parts",
              "children": []
            }
          }
        },
        "101407": {
          "text": "Lights",
          "children": {
            "101420": {
              "text": "Direction Indicator/Parts",
              "children": {
                "101421": {
                  "text": "Direction Indicator",
                  "children": []
                }
              }
            }
          }
        }
      }
    },
    "100002": {
      "text": "Engine",
      "children": {
        "100003": {
          "text": "Engine Timing",
          "children": {
            "100396": {
              "text": "Timing Belt/Tensioner/Guide",
              "children": {
                "100404": {
                  "text": "Timing Belt",
                  "children": []
                }
              }
            }
          }
        }
      }
    }
  }
}
```

> Full response covers all vehicle-relevant categories — truncated above for illustration.

**Response Fields**

| Field | Type | Description |
|-------|------|-------------|
| `categories` | object | Root wrapper; keys are top-level category ID strings |
| `categories[id]` | object | A category node keyed by its numeric category ID (as string) |
| `categories[id].text` | string | Human-readable category name (language from `lang_id`) |
| `categories[id].children` | object \| array | Keyed object of child nodes at non-leaf levels; empty array `[]` at leaf nodes |

**Four-Way Comparison: Category Endpoints**

| Aspect | [#27 All Categories](#27-get-list-all-categories) | [#28 by Vehicle (v1)](#28-get-list-categories-by-vehicle-id-v1) | [#29 by Vehicle (v2)](#29-get-list-categories-by-vehicle-id-v2) | #30 by Vehicle (v3) |
|--------|--------------------------------------------------|----------------------------------------------------------------|----------------------------------------------------------------|---------------------|
| Scope | All TecDoc | Vehicle-filtered | Vehicle-filtered | Vehicle-filtered |
| Format | Nested tree | Flat breadcrumb array | Nested tree | Nested tree |
| Node fields | `categoryId`, `categoryName`, `level`, `children` | `level`, `categoryId1`–`4`, `categoryName1`–`4` | `categoryId`, `categoryName`, `level`, `children` | `text`, `children` only |
| Category ID location | Inside node (`categoryId`) | Inside node (`categoryId1`–`4`) | Inside node (`categoryId`) | Object key only |
| `level` field | Yes | Yes (column selector) | Yes | **No** |
| Payload size | Largest | Medium | Large | **Smallest** |
| Use case | Full browser | Server-side filtering | Vehicle menu with IDs | Lightweight tree UI |

**Notes**

- The **category ID is only the object key** — there is no `categoryId` field inside the node. Parse it as: `Object.entries(categories).map(([id, node]) => ({ id, ...node }))`
- There is **no `level` field** — depth must be inferred from how deep in the recursion you are
- `children` has the same **type inconsistency** as #27 and #29: non-leaf nodes use a keyed object, leaf nodes use `[]`. Always check `Array.isArray(children)` before iterating
- This is the **most compact** of the four category endpoints — smallest payload, ideal for bandwidth-sensitive or mobile clients
- Trade-off: you lose `level` depth info and must track depth yourself while traversing
- Use `Object.values(categories)` to iterate top-level nodes (same as #29)

---

### 31. GET  List Main Category by Article ID

**Description:** Returns the single primary/main category that an article belongs to, given its article ID. Unlike the vehicle-category endpoints (#27–#30), this is article-centric — it answers "what category is this part in?" rather than "what categories exist for a vehicle?". Returns a flat single object with just `categoryId` and `categoryName`.

**Auth Required:** Yes (RapidAPI key)

**Request**

- Method: `GET`
- URL: `https://tecdoc-catalog.p.rapidapi.com/articles/get-article-category/article-id/{article_id}/lang-id/{lang_id}`
- Headers:
  - `x-rapidapi-host: tecdoc-catalog.p.rapidapi.com`
  - `x-rapidapi-key: <YOUR_RAPIDAPI_KEY>`

**Path Parameters**

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `article_id` | integer | Yes | TecDoc internal article ID (e.g., `6159438`) |
| `lang_id` | integer | Yes | Language ID for the category name (e.g., `4` = English GB) |

**Query Params:** None

**Request Body:** None

**Response**

- Status: `200 OK`
- Response Time: ~1180 ms
- Body:

```json
{
  "categoryId": 706695,
  "categoryName": "Filter for traction battery"
}
```

**Response Fields**

| Field | Type | Description |
|-------|------|-------------|
| `categoryId` | integer | TecDoc category ID the article belongs to |
| `categoryName` | string | Human-readable category name in the requested language |

**Notes**

- Returns a **single flat object** — not an array, not a tree. One article maps to one primary category
- `article_id` here is the **TecDoc internal article ID** (e.g., `6159438`), not the supplier article number. Use [#24 Article Details](#24-post-article-details-by-article-no) or a search endpoint to resolve an article number to its internal ID first
- The returned `categoryId` can be used to look up the full category tree position via [#27 List All Categories](#27-get-list-all-categories)
- `lang_id` only affects the `categoryName` label — the `categoryId` is language-independent

---

### 32. GET  List Categories by Article ID

**Description:** Returns **all** categories an article belongs to, each with its parent breadcrumb chain. Unlike [#31](#31-get-list-main-category-by-article-id) which returns one primary category, this endpoint returns every category the article is cross-listed under (e.g., the same air filter may appear under "Filters", "Engine > Air Supply", and "Maintenance Service Parts"). Each entry includes the full ancestor path via `categoryParentName`.

**Auth Required:** Yes (RapidAPI key)

**Request**

- Method: `GET`
- URL: `https://tecdoc-catalog.p.rapidapi.com/articles/get-article-categories/article-id/{article_id}/lang-id/{lang_id}`
- Headers:
  - `x-rapidapi-host: tecdoc-catalog.p.rapidapi.com`
  - `x-rapidapi-key: <YOUR_RAPIDAPI_KEY>`

**Path Parameters**

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `article_id` | integer | Yes | TecDoc internal article ID (e.g., `6159438`) |
| `lang_id` | integer | Yes | Language ID for category names (e.g., `4` = English GB) |

**Query Params:** None

**Request Body:** None

**Response**

- Status: `200 OK`
- Response Time: ~1433 ms
- Body:

```json
[
  {
    "articleId": 6159438,
    "articleNo": "C 2029",
    "categoryId": 100260,
    "categoryParentId": 100005,
    "categoryName": "Air Filter",
    "vehicleTypes": "PC,Motorcycle",
    "categoryParentName": [
      {
        "categoryId": 100005,
        "categoryName": "Filters"
      }
    ]
  },
  {
    "articleId": 6159438,
    "articleNo": "C 2029",
    "categoryId": 100384,
    "categoryParentId": 100383,
    "categoryName": "Air Filter/ Housing",
    "vehicleTypes": "PC,Motorcycle",
    "categoryParentName": [
      {
        "categoryId": 100383,
        "categoryName": "Air Supply"
      },
      {
        "categoryId": 100002,
        "categoryName": "Engine"
      }
    ]
  },
  {
    "articleId": 6159438,
    "articleNo": "C 2029",
    "categoryId": 100597,
    "categoryParentId": 100019,
    "categoryName": "Service Intervals",
    "vehicleTypes": "PC,Motorcycle",
    "categoryParentName": [
      {
        "categoryId": 100019,
        "categoryName": "Maintenance Service Parts"
      }
    ]
  },
  {
    "articleId": 6159438,
    "articleNo": "C 2029",
    "categoryId": 103780,
    "categoryParentId": 103777,
    "categoryName": "Air Filter",
    "vehicleTypes": "PC,Motorcycle",
    "categoryParentName": [
      {
        "categoryId": 103777,
        "categoryName": "Filters"
      },
      {
        "categoryId": 103671,
        "categoryName": "Motorcycle"
      }
    ]
  }
]
```

**Response Fields**

| Field | Type | Description |
|-------|------|-------------|
| `[]` | array | One entry per category the article is listed under |
| `articleId` | integer | TecDoc internal article ID (same as path param) |
| `articleNo` | string | Supplier article number (e.g., `"C 2029"`) |
| `categoryId` | integer | Category ID this article belongs to |
| `categoryParentId` | integer | Direct parent category ID of `categoryId` |
| `categoryName` | string | Name of this category (language from `lang_id`) |
| `vehicleTypes` | string | Comma-separated vehicle type codes this listing applies to (e.g., `"PC,Motorcycle"`) |
| `categoryParentName` | array | Breadcrumb ancestor chain from direct parent up to root; ordered nearest-first |
| `categoryParentName[].categoryId` | integer | Ancestor category ID |
| `categoryParentName[].categoryName` | string | Ancestor category name |

**#31 vs #32 Comparison**

| Aspect | [#31 List Main Category](#31-get-list-main-category-by-article-id) | #32 List Categories |
|--------|---------------------------------------------------------------------|---------------------|
| URL segment | `get-article-category` (singular) | `get-article-categories` (plural) |
| Returns | Single flat object | Array of all categories |
| Parent info | None | Full breadcrumb chain per entry |
| Vehicle types | Not included | Included per entry |
| Use case | Quick category lookup | Full cross-listing and breadcrumb display |

**Notes**

- An article can belong to **multiple categories** — the same part is often cross-listed (e.g., "Air Filter" appears under both `Filters` and `Engine > Air Supply > Air Filter/ Housing`)
- `categoryParentName` is ordered **nearest ancestor first** — index `[0]` is the direct parent, last index is the root
- `categoryParentId` always matches `categoryParentName[0].categoryId`
- `vehicleTypes` is a comma-separated string, not an array — split on `","` to process programmatically
- `article_id` is the **TecDoc internal ID**, not the supplier article number (`articleNo`). Resolve via a search endpoint first if you only have the article number
- The `categoryId` values returned here can be cross-referenced against [#27 List All Categories](#27-get-list-all-categories) to get the full tree position

---

### 33. GET  Search (sub)Categories by Text

**Description:** Full-text search across TecDoc category names and generic article/product names. Returns a nested tree of matching results organized by top-level category → sub-category → matched generic article names. Each leaf node includes a `productId` (TecDoc generic article/product group ID) which can be used for further part lookups. Useful for implementing a search-as-you-type category finder.

**Auth Required:** Yes (RapidAPI key)

**Request**

- Method: `GET`
- URL: `<!-- TODO: confirm URL from RapidAPI dashboard -->`
- Headers:
  - `x-rapidapi-host: tecdoc-catalog.p.rapidapi.com`
  - `x-rapidapi-key: <YOUR_RAPIDAPI_KEY>`

**Query / Path Parameters**

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `search_text` | string | Yes | Keyword to search for (e.g., `"valve"`) |
| `lang_id` | integer | Yes | Language ID for result names (e.g., `4` = English GB) |
| `type_id` | integer | No | Vehicle type filter (e.g., `1` = Passenger Car) |

> Confirm exact param names from the RapidAPI dashboard.

**Request Body:** None

**Response**

- Status: `200 OK`
- Response Time: ~(confirm from RapidAPI dashboard)
- Body:

```json
{
  "Air Conditioning": {
    "categoryId": 100243,
    "categoryName": "Air Conditioning",
    "level": 1,
    "children": {
      "Compressor/Parts": {
        "categoryId": null,
        "categoryName": "Compressor/Parts",
        "level": 2,
        "children": {
          "Control Valve, air conditioning compressor": {
            "categoryId": 100354,
            "categoryName": "Compressor/Parts",
            "level": 2,
            "children": [],
            "productId": 2920
          },
          "Gasket Set, compressor control valve": {
            "categoryId": 100354,
            "categoryName": "Compressor/Parts",
            "level": 2,
            "children": [],
            "productId": 2921
          }
        }
      },
      "Valves": {
        "categoryId": null,
        "categoryName": "Valves",
        "level": 2,
        "children": {
          "Expansion Valve, air conditioning": {
            "categoryId": 100358,
            "categoryName": "Valves",
            "level": 2,
            "children": [],
            "productId": 183
          }
        }
      }
    }
  },
  "Braking System": {
    "categoryId": 100006,
    "categoryName": "Braking System",
    "level": 1,
    "children": {
      "Brake Caliper": {
        "categoryId": null,
        "categoryName": "Brake Caliper",
        "level": 2,
        "children": {
          "Bleeder Screw/Valve, brake caliper": {
            "categoryId": 100027,
            "categoryName": "Brake Caliper",
            "level": 2,
            "children": {
              "Brake Caliper Parts": {
                "categoryId": null,
                "categoryName": "Brake Caliper Parts",
                "level": 4,
                "children": {
                  "Bleeder Screw/Valve, brake caliper": {
                    "categoryId": 100806,
                    "categoryName": "Brake Caliper Parts",
                    "level": 3,
                    "children": [],
                    "productId": 5213
                  }
                }
              }
            },
            "productId": 5213
          }
        }
      }
    }
  }
}
```

> Full response contains dozens of top-level categories each with multiple matched products — truncated above to 2 categories for illustration.

**Response Fields**

| Field | Type | Description |
|-------|------|-------------|
| `{CategoryName}` | object | Top-level category node; object key is the category name string |
| `{CategoryName}.categoryId` | integer | Top-level category ID |
| `{CategoryName}.categoryName` | string | Top-level category name (duplicates the key) |
| `{CategoryName}.level` | integer | Always `1` at top level |
| `{CategoryName}.children` | object | Sub-category grouping nodes, keyed by sub-category name |
| `children.{SubCategoryName}.categoryId` | integer \| null | Sub-category ID, or `null` for intermediate grouping nodes |
| `children.{SubCategoryName}.categoryName` | string | Sub-category name |
| `children.{SubCategoryName}.level` | integer | Depth indicator (unreliable — see notes) |
| `children.{SubCategoryName}.children` | object \| array | Nested children (object) or empty (`[]`) at leaf |
| `{ProductName}.productId` | integer | TecDoc generic article/product group ID — only present on leaf nodes that match the search |
| `{ProductName}.categoryId` | integer | Category ID the matched product belongs to |
| `{ProductName}.categoryName` | string | Category name the matched product belongs to |

**Node Types Summary**

| Node type | `categoryId` | Has `productId` | `children` type | Key meaning |
|-----------|-------------|-----------------|-----------------|-------------|
| Top-level category | integer | No | keyed object | Category name |
| Intermediate grouping | `null` | No | keyed object | Sub-category name |
| Matched product (leaf) | integer | **Yes** | `[]` | Generic article/product name |
| Deep match (has sub-path) | integer | **Yes** | keyed object | Generic article name (also appears deeper) |

**Notes**

- Object **keys serve three different semantic roles** depending on depth: top-level category name → sub-category grouping name → matched generic article/product name
- `productId` is the **TecDoc generic article / product group ID** — not an article ID. Use it to look up actual articles that match the search within a specific vehicle context
- **`level` values are unreliable** — a child node can have a lower or equal `level` value than its parent (e.g., parent `level: 4`, child `level: 3`). Do not use `level` for depth tracking; use your own recursion depth counter instead
- `categoryId: null` marks **intermediate grouping nodes** with no direct category mapping — they exist purely to group matched products under a sub-heading
- `children` has the same **type inconsistency** as other category endpoints: non-leaf nodes use a keyed object, leaf nodes use `[]`. Always check `Array.isArray(children)` before iterating
- The same product can appear **multiple times** at different tree paths (same `productId` under different categories) — deduplicate by `productId` if building a flat list
- The search matched the word **"valve"** in this example — results span many top-level categories (Air Conditioning, Braking System, Clutch, Engine, etc.) showing the cross-category scope of the search

---

### 34. GET  List All Product Names

**Description:** Returns the complete flat list of all TecDoc generic article / product group names with their IDs. These `productId` values are the same IDs referenced in [#33 Search Categories by Text](#33-get-search-subcategories-by-text) leaf nodes and throughout the TecDoc catalog. Use this as a lookup table to resolve a `productId` to a human-readable name, or to build a full product name autocomplete.

**Auth Required:** Yes (RapidAPI key)

**Request**

- Method: `GET`
- URL: `<!-- TODO: confirm URL from RapidAPI dashboard -->`
- Headers:
  - `x-rapidapi-host: tecdoc-catalog.p.rapidapi.com`
  - `x-rapidapi-key: <YOUR_RAPIDAPI_KEY>`

**Path / Query Parameters**

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `lang_id` | integer | Yes | Language ID for product names (e.g., `4` = English GB) |

> Confirm exact param name and whether it is a path param or query param from the RapidAPI dashboard.

**Request Body:** None

**Response**

- Status: `200 OK`
- Response Time: ~(confirm from RapidAPI dashboard)
- Body:

```json
[
  {
    "productId": 1,
    "productName": "Starter Battery"
  },
  {
    "productId": 2,
    "productName": "Starter"
  },
  {
    "productId": 4,
    "productName": "Alternator"
  },
  {
    "productId": 5,
    "productName": "Joint Kit, drive shaft"
  },
  {
    "productId": 7,
    "productName": "Oil Filter"
  },
  {
    "productId": 8,
    "productName": "Air Filter"
  },
  {
    "productId": 9,
    "productName": "Fuel Filter"
  },
  {
    "productId": 10,
    "productName": "V-Belt"
  }
]
```

> Full response contains **thousands of entries** covering the entire TecDoc product catalog — truncated above to 8 entries for illustration.

**Response Fields**

| Field | Type | Description |
|-------|------|-------------|
| `[]` | array | Flat list of all product/generic article name entries |
| `productId` | integer | TecDoc generic article / product group ID |
| `productName` | string | Human-readable product name in the requested language |

**Notes**

- `productId` values are **not sequential** — there are intentional gaps (e.g., `3`, `6`, `11` are absent), so never assume a product exists by ID range
- `productId` here is the **same ID** returned in the `productId` field of [#33 Search (sub)Categories by Text](#33-get-search-subcategories-by-text) leaf nodes — use this endpoint to resolve those IDs to names
- This is a **reference/lookup list** — it contains the names of generic article types (e.g., "Oil Filter", "Timing Belt Kit"), not actual supplier articles. To get supplier articles for a given product, use the article search endpoints (#19–#24)
- The full list is large (thousands of entries) — consider caching it client-side or in a database rather than calling it on every request
- `lang_id` controls the language of `productName` — the `productId` is language-independent

---

### 35. GET  Article Details by Article ID

**Description:** Returns full details for a single article by its TecDoc internal article ID, including article basics, all technical specifications, EAN number, and OEM cross-reference numbers. This is the GET equivalent of [#24 POST Article Details by Article No](#24-post-article-details-by-article-no) — use this when you already have the `articleId` and want to avoid a POST.

**Auth Required:** Yes (RapidAPI key)

**Request**

- Method: `GET`
- URL: `https://tecdoc-catalog.p.rapidapi.com/articles/details/article-id/{article_id}/lang-id/{lang_id}`
- Headers:
  - `x-rapidapi-host: tecdoc-catalog.p.rapidapi.com`
  - `x-rapidapi-key: <YOUR_RAPIDAPI_KEY>`

**Path Parameters**

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `article_id` | integer | Yes | TecDoc internal article ID (e.g., `6925928`) |
| `lang_id` | integer | Yes | Language ID for specification labels (e.g., `4` = English GB) |

**Query Params:** None

**Request Body:** None

**Response**

- Status: `200 OK`
- Response Time: ~1431 ms
- Body:

```json
{
  "articleId": "6925928",
  "article": {
    "articleId": 6925928,
    "articleNo": "F 026 400 063",
    "supplierId": 30,
    "supplierName": "BOSCH",
    "isAccessory": 0,
    "articleProductName": "Air Filter"
  },
  "articleAllSpecifications": [
    {
      "criteriaName": "Length [mm]",
      "criteriaValue": "190"
    },
    {
      "criteriaName": "Width [mm]",
      "criteriaValue": "200"
    },
    {
      "criteriaName": "Height [mm]",
      "criteriaValue": "50"
    },
    {
      "criteriaName": "Quantity",
      "criteriaValue": "1"
    },
    {
      "criteriaName": "Filter type",
      "criteriaValue": "9"
    }
  ],
  "articleEanNo": {
    "eanNumbers": "4047024328792"
  },
  "articleOemNo": [
    {
      "oemBrand": "HYUNDAI",
      "oemDisplayNo": "28113 0Q000"
    },
    {
      "oemBrand": "KIA",
      "oemDisplayNo": "28113 2H000"
    },
    {
      "oemBrand": "HYUNDAI",
      "oemDisplayNo": "281132H000"
    }
  ]
}
```

**Response Fields**

| Field | Type | Description |
|-------|------|-------------|
| `articleId` | string | TecDoc article ID echoed back as a **string** (note: different type from `article.articleId`) |
| `article` | object | Core article identity fields |
| `article.articleId` | integer | TecDoc internal article ID (same value as root `articleId`, but as an **integer**) |
| `article.articleNo` | string | Supplier article/part number (e.g., `"F 026 400 063"`) |
| `article.supplierId` | integer | TecDoc supplier/brand ID |
| `article.supplierName` | string | Supplier/brand name (e.g., `"BOSCH"`) |
| `article.isAccessory` | integer | Flag: `0` = main article, `1` = accessory |
| `article.articleProductName` | string | Generic product type name (e.g., `"Air Filter"`) |
| `articleAllSpecifications` | array | List of all technical specification entries for this article |
| `articleAllSpecifications[].criteriaName` | string | Specification label including unit (e.g., `"Length [mm]"`) |
| `articleAllSpecifications[].criteriaValue` | string | Specification value as a string (e.g., `"190"`) |
| `articleEanNo` | object | EAN barcode information |
| `articleEanNo.eanNumbers` | string | EAN-13 barcode number(s) as a string |
| `articleOemNo` | array | List of OEM cross-reference numbers from vehicle manufacturers |
| `articleOemNo[].oemBrand` | string | OEM brand/manufacturer name (e.g., `"HYUNDAI"`) |
| `articleOemNo[].oemDisplayNo` | string | OEM part number as displayed (may include spaces) |

**#24 vs #35 Comparison**

| Aspect | [#24 POST Article Details by Article No](#24-post-article-details-by-article-no) | #35 GET Article Details by Article ID |
|--------|-----------------------------------------------------------------------------------|---------------------------------------|
| Method | POST | GET |
| Input identifier | Supplier article number (e.g., `"F 026 400 063"`) | TecDoc internal article ID (e.g., `6925928`) |
| Specs field name | (confirm from #24 response) | `articleAllSpecifications` |
| `supplierName` | Not included directly | Included in `article.supplierName` |
| Use case | When you have the part number | When you already have the `articleId` |

**Notes**

- **Type inconsistency**: root `articleId` is a **string** (`"6925928"`), but `article.articleId` is an **integer** (`6925928`) — parse accordingly
- `articleEanNo.eanNumbers` is a **plain string**, not an array — if multiple EANs exist they may be comma-separated or space-separated; confirm format with actual multi-EAN responses
- `articleOemNo` can contain **duplicate brands** with different part numbers (e.g., two HYUNDAI entries with different formats of the same number — `"28113 0Q000"` vs another variant)
- `criteriaValue` is always a **string** even for numeric values — cast to number before arithmetic
- The `article_id` here is the **TecDoc internal ID**, not the supplier article number. Obtain it first via any search endpoint (#19–#23) or from [#24](#24-post-article-details-by-article-no)

---

### 36. POST  Article Details by Article ID (Complete)

**Description:** Returns the most complete article record available — including basics, all technical specifications, EAN, OEM cross-references, a direct S3 image URL, and a **full list of compatible vehicles**. This is the richest article detail endpoint and is the primary choice when you need fitment data alongside article info. Uses POST with the article ID in the request body.

**Auth Required:** Yes (RapidAPI key)

**Request**

- Method: `POST`
- URL: `https://tecdoc-catalog.p.rapidapi.com/articles/article-id-complete-details`
- Headers:
  - `x-rapidapi-host: tecdoc-catalog.p.rapidapi.com`
  - `x-rapidapi-key: <YOUR_RAPIDAPI_KEY>`
  - `Content-Type: application/json`

**Request Body**

```json
{
  "articleId": 131540,
  "langId": 4
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `articleId` | integer | Yes | TecDoc internal article ID |
| `langId` | integer | Yes | Language ID for spec labels (e.g., `4` = English GB) |

**Response**

- Status: `200 OK`
- Response Time: ~1340 ms
- Body:

```json
{
  "article": {
    "articleId": 131540,
    "articleNo": "002-001-000001R",
    "articleProductName": "Injection Pump",
    "supplierName": "REMANTE",
    "supplierId": 814,
    "articleMediaType": "JPEG",
    "articleMediaFileName": "a87fb8344298bbf9babc7be7c284fef7bd75cac3.webp",
    "articleInfo": {
      "articleId": 131540,
      "articleNo": "002-001-000001R",
      "supplierId": 814,
      "supplierName": "REMANTE",
      "isAccessory": 0,
      "articleProductName": "Injection Pump"
    },
    "allSpecifications": [
      {
        "criteriaName": "Weight [kg]",
        "criteriaValue": "9,20"
      },
      {
        "criteriaName": "Fuel Type",
        "criteriaValue": "5"
      },
      {
        "criteriaName": "Exchange Part",
        "criteriaValue": ""
      }
    ],
    "eanNo": {
      "eanNumbers": "08595706500449"
    },
    "oemNo": [
      {
        "oemBrand": "VW",
        "oemDisplayNo": "059 130 105 A"
      },
      {
        "oemBrand": "VW",
        "oemDisplayNo": "059 130 106 A"
      }
    ],
    "s3image": "https://fsn1.your-objectstorage.com/tecdoc2025/media_files/images/814/a87fb8344298bbf9babc7be7c284fef7bd75cac3.webp",
    "compatibleCars": [
      {
        "vehicleId": 7742,
        "modelId": 265,
        "manufacturerName": "AUDI",
        "modelName": "A8 D2 (4D2, 4D8)",
        "typeEngineName": "2.5 TDI",
        "constructionIntervalStart": "1997-01-01",
        "constructionIntervalEnd": "2000-04-01"
      },
      {
        "vehicleId": 10179,
        "modelId": 1568,
        "manufacturerName": "VW",
        "modelName": "PASSAT B5 (3B2)",
        "typeEngineName": "2.5 TDI",
        "constructionIntervalStart": "1998-07-01",
        "constructionIntervalEnd": "2000-11-01"
      }
    ]
  }
}
```

> `allSpecifications` and `compatibleCars` are truncated — full response contains all specs and all matching vehicles.

**Response Fields**

| Field | Type | Description |
|-------|------|-------------|
| `article` | object | Root wrapper for all article data |
| `article.articleId` | integer | TecDoc internal article ID |
| `article.articleNo` | string | Supplier article/part number |
| `article.articleProductName` | string | Generic product type name |
| `article.supplierName` | string | Supplier/brand name |
| `article.supplierId` | integer | TecDoc supplier ID |
| `article.articleMediaType` | string | Declared media type (e.g., `"JPEG"`) — may not match actual file extension |
| `article.articleMediaFileName` | string | Image filename (used to construct the S3 URL) |
| `article.articleInfo` | object | Duplicate of core article fields (same as top-level minus media fields) |
| `article.articleInfo.isAccessory` | integer | `0` = main article, `1` = accessory |
| `article.allSpecifications` | array | Technical specification entries |
| `article.allSpecifications[].criteriaName` | string | Spec label with unit (e.g., `"Weight [kg]"`) |
| `article.allSpecifications[].criteriaValue` | string | Spec value as string; may be empty `""` for optional specs |
| `article.eanNo` | object | EAN barcode info |
| `article.eanNo.eanNumbers` | string | EAN barcode number(s) as a string |
| `article.oemNo` | array | OEM cross-reference numbers |
| `article.oemNo[].oemBrand` | string | OEM manufacturer name |
| `article.oemNo[].oemDisplayNo` | string | OEM part number with original formatting |
| `article.s3image` | string \| null | Full S3 URL to the article image; `null` if no image available |
| `article.compatibleCars` | array | All vehicles this article fits |
| `article.compatibleCars[].vehicleId` | integer | TecDoc vehicle ID |
| `article.compatibleCars[].modelId` | integer | TecDoc model ID |
| `article.compatibleCars[].manufacturerName` | string | Manufacturer name (e.g., `"AUDI"`, `"VW"`) |
| `article.compatibleCars[].modelName` | string | Full model name including generation code (e.g., `"A6 C5 (4B2, 4B4)"`) |
| `article.compatibleCars[].typeEngineName` | string | Engine variant name (e.g., `"2.5 TDI quattro"`) |
| `article.compatibleCars[].constructionIntervalStart` | string | Production start date in `YYYY-MM-DD` format |
| `article.compatibleCars[].constructionIntervalEnd` | string \| null | Production end date; `null` if still in production |

**#35 vs #36 Comparison**

| Aspect | [#35 GET Article Details by Article ID](#35-get-article-details-by-article-id) | #36 POST Article Details by Article ID (Complete) |
|--------|---------------------------------------------------------------------------------|---------------------------------------------------|
| Method | GET | POST |
| Specs field | `articleAllSpecifications` | `allSpecifications` |
| EAN field | `articleEanNo` | `eanNo` |
| OEM field | `articleOemNo` | `oemNo` |
| Image URL | Not included | `s3image` (direct S3 URL) |
| Compatible vehicles | Not included | `compatibleCars` (full fitment list) |
| Article info wrapper | Flat in root | Nested under `articleInfo` |
| Use case | Quick article lookup | Full details + fitment data |

**Notes**

- `articleMediaType` reports `"JPEG"` but `articleMediaFileName` has a `.webp` extension — the declared type does not match the actual file. Use the `s3image` URL directly rather than relying on `articleMediaType` for rendering
- `allSpecifications` entries with empty `criteriaValue: ""` are optional/unfilled specs — filter them out before display
- `criteriaValue` uses **locale-formatted decimals** (e.g., `"9,20"` with a comma) — normalize to dot-decimal before parsing as float
- `compatibleCars` can contain many entries for popular parts — consider paginating the display on the frontend
- `article.articleInfo` duplicates the top-level fields (`articleId`, `articleNo`, etc.) — it adds `isAccessory` which is not present at the top level
- `s3image` may be `null` for articles without images — always null-check before rendering

---

### 37. GET  Article Details & Compatibility by Article ID

**Description:** Returns the same complete article record as [#36](#36-post-article-details-by-article-id-complete) — basics, specifications, EAN, OEM numbers, S3 image URL, and compatible vehicles — but via a GET request with vehicle type and country filtering. Use this when you want to scope the `compatibleCars` results to a specific vehicle type (e.g., only Passenger Cars) and/or country.

**Auth Required:** Yes (RapidAPI key)

**Request**

- Method: `GET`
- URL: `https://tecdoc-catalog.p.rapidapi.com/articles/article-complete-details/type-id/{type_id}?articleId={article_id}&langId={lang_id}&countryFilterId={country_id}`
- Headers:
  - `x-rapidapi-host: tecdoc-catalog.p.rapidapi.com`
  - `x-rapidapi-key: <YOUR_RAPIDAPI_KEY>`

**Path Parameters**

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `type_id` | integer | Yes | Vehicle type filter (e.g., `1` = Passenger Car) |

**Query Parameters**

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `articleId` | integer | Yes | TecDoc internal article ID (e.g., `131540`) |
| `langId` | integer | Yes | Language ID for labels (e.g., `4` = English GB) |
| `countryFilterId` | integer | Yes | Country filter ID (e.g., `63` = Germany) |

**Request Body:** None

**Response**

- Status: `200 OK`
- Response Time: ~1224 ms
- Body: Identical structure to [#36 POST Article Details by Article ID (Complete)](#36-post-article-details-by-article-id-complete) — see that entry for the full response sample and field-by-field table.

```json
{
  "article": {
    "articleId": 131540,
    "articleNo": "002-001-000001R",
    "articleProductName": "Injection Pump",
    "supplierName": "REMANTE",
    "supplierId": 814,
    "articleMediaType": "JPEG",
    "articleMediaFileName": "a87fb8344298bbf9babc7be7c284fef7bd75cac3.webp",
    "articleInfo": { "...": "same as #36" },
    "allSpecifications": [ "...same as #36" ],
    "eanNo": { "eanNumbers": "08595706500449" },
    "oemNo": [ "...same as #36" ],
    "s3image": "https://fsn1.your-objectstorage.com/tecdoc2025/media_files/images/814/a87fb8344298bbf9babc7be7c284fef7bd75cac3.webp",
    "compatibleCars": [ "...vehicle list filtered by type_id and countryFilterId" ]
  }
}
```

**#36 vs #37 Comparison**

| Aspect | [#36 POST Complete Details](#36-post-article-details-by-article-id-complete) | #37 GET Details & Compatibility |
|--------|------------------------------------------------------------------------------|----------------------------------|
| Method | POST | GET |
| Vehicle type filter | None — returns all types | `type_id` path param |
| Country filter | None | `countryFilterId` query param |
| Parameters | Request body (`articleId`, `langId`) | Path + query params |
| Response structure | Identical | Identical |
| Use case | Full cross-vehicle details | Type- and country-scoped fitment |

**Notes**

- Response structure and all field names are **identical to #36** — refer to [#36](#36-post-article-details-by-article-id-complete) for the complete field reference
- `type_id = 1` filters `compatibleCars` to Passenger Cars only — change to other type IDs (from [#5 Vehicle Types](#5-get-vehicle-types)) to filter differently
- `countryFilterId` narrows results to vehicles sold/marketed in that country — use `63` for Germany (broadest coverage in TecDoc)
- For the same article, #36 and #37 may return different `compatibleCars` counts depending on how strict the type/country filter is
- Prefer this endpoint over #36 when building a **vehicle-specific fitment UI** where you already know the vehicle type context

---

## 38. POST Article Details by Article ID & Language ID

**Base URL:** `https://tecdoc-catalog.p.rapidapi.com/articles/details`  
**Method:** POST  
**Tested:** 2026-04-11 | Status: `200 OK` | Response Time: ~1209 ms

**Overview**

POST equivalent of [#35 GET Article Details by Article ID](#35-get-article-details-by-article-id). Accepts `articleId` and `langId` in the request body instead of URL path parameters. Returns the same core article data: technical specifications, EAN barcode, and OEM cross-references.

**Request**

**Headers:**
```
Content-Type: application/json
X-RapidAPI-Key: <your-api-key>
X-RapidAPI-Host: tecdoc-catalog.p.rapidapi.com
```

**Body:**
```json
{
  "articleId": 6925928,
  "langId": 4
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `articleId` | integer | Yes | TecDoc internal article ID |
| `langId` | integer | Yes | Language ID for localized labels (e.g., `4` = English GB) |

**Response**

```json
{
  "articleId": "6925928",
  "article": {
    "articleId": 6925928,
    "articleNo": "F 026 400 063",
    "supplierId": 30,
    "supplierName": "BOSCH",
    "isAccessory": 0,
    "articleProductName": "Air Filter"
  },
  "articleAllSpecifications": [
    { "criteriaName": "Length [mm]", "criteriaValue": "190" },
    { "criteriaName": "Width [mm]", "criteriaValue": "200" },
    { "criteriaName": "Height [mm]", "criteriaValue": "50" },
    { "criteriaName": "Quantity", "criteriaValue": "1" },
    { "criteriaName": "Filter type", "criteriaValue": "9" }
  ],
  "articleEanNo": {
    "eanNumbers": "4047024328792"
  },
  "articleOemNo": [
    { "oemBrand": "HYUNDAI", "oemDisplayNo": "28113 0Q000" },
    { "oemBrand": "KIA", "oemDisplayNo": "28113 2H000" },
    { "oemBrand": "HYUNDAI", "oemDisplayNo": "281132H000" }
  ]
}
```

**Response Fields**

| Field | Type | Description |
|-------|------|-------------|
| `articleId` | string | TecDoc internal article ID — **root-level value is a string** (e.g., `"6925928"`) |
| `article.articleId` | integer | Same ID but as integer inside the nested `article` object — type inconsistency, same as [#35](#35-get-article-details-by-article-id) |
| `article.articleNo` | string | Supplier part number (e.g., `"F 026 400 063"`) |
| `article.supplierId` | integer | TecDoc internal supplier ID |
| `article.supplierName` | string | Supplier brand name (e.g., `"BOSCH"`) |
| `article.isAccessory` | integer | `0` = main article, `1` = accessory/companion part |
| `article.articleProductName` | string | Generic product type name (e.g., `"Air Filter"`) |
| `articleAllSpecifications` | array | Technical specifications for this article |
| `articleAllSpecifications[].criteriaName` | string | Specification label including unit (e.g., `"Length [mm]"`) |
| `articleAllSpecifications[].criteriaValue` | string | Always a string; may use comma as decimal separator (e.g., `"9,20"`) — see [#36 note](#36-post-article-details-by-article-id-complete) |
| `articleEanNo.eanNumbers` | string | EAN-13 barcode number |
| `articleOemNo` | array | OEM cross-reference numbers |
| `articleOemNo[].oemBrand` | string | OEM manufacturer name (e.g., `"HYUNDAI"`, `"KIA"`) |
| `articleOemNo[].oemDisplayNo` | string | OEM part number as displayed (may include spaces) |

**#35 vs #38 Comparison**

| Aspect | [#35 GET Article Details by Article ID](#35-get-article-details-by-article-id) | #38 POST Article Details by Article ID & Language ID |
|--------|---------------------------------------------------------------------------------|------------------------------------------------------|
| Method | GET | POST |
| Parameters | Path params: `article_id`, `lang_id` | Request body: `articleId`, `langId` |
| URL pattern | `/articles/details/article-id/{id}/lang-id/{lang}` | `/articles/details` |
| Response structure | Identical | Identical |
| HTTP caching | Cacheable by URL | Not cacheable (POST) |
| Use case | Standard REST lookup | When IDs are part of a larger JSON payload |

**Notes**

- Response structure and all field names are **identical to [#35](#35-get-article-details-by-article-id)** — the only difference is HTTP method and parameter transport
- The `articleId` type inconsistency (string at root, integer inside `article`) is present here, same as in #35
- `articleOemNo` may contain **duplicate OEM numbers** across brands — e.g., the same HYUNDAI part appears twice with different spacing (`"28113 0Q000"` and `"281132H000"`); normalise by stripping whitespace before deduplication
- RapidAPI dashboard reported `Response Body Size: 2 Bytes` for this call — this is likely a measurement artefact; the actual payload is substantially larger
- For richer article data (product images, `s3image`, compatible vehicles), use [#36 POST Article Details (Complete)](#36-post-article-details-by-article-id-complete) instead

---

## 39. GET Article Criteria

**URL:** `https://tecdoc-catalog.p.rapidapi.com/articles/selection-of-all-specifications-criterias-for-the-article/article-id/{article_id}/lang-id/{lang_id}/country-filter-id/{country_filter_id}`  
**Method:** GET  
**Tested:** 2026-04-11 | Status: `200 OK` | Response Time: ~1420 ms

**Overview**

Returns a flat array of all technical and fitment criteria for a given article. Unlike the `articleAllSpecifications` field embedded in [#35](#35-get-article-details-by-article-id) / [#38](#38-post-article-details-by-article-id--language-id), this dedicated endpoint includes **vehicle fitment criteria** (construction years, VIN ranges, engine codes, transmission type, manufacturer restrictions) in addition to physical dimensions.

**Path Parameters**

| Parameter | Type | Description |
|-----------|------|-------------|
| `article_id` | integer | TecDoc internal article ID |
| `lang_id` | integer | Language ID for criterion labels (e.g., `4` = English GB) |
| `country_filter_id` | integer | Country filter (e.g., `63` = Germany) — affects which fitment data is included |

**Response**

```json
[
  { "criteriaName": "Bore Diameter [mm]",                          "criteriaValue": "10,5" },
  { "criteriaName": "Bore Diameter 2 [mm]",                        "criteriaValue": "10,5" },
  { "criteriaName": "Bore Ø 3 [mm]",                              "criteriaValue": "10,5" },
  { "criteriaName": "Clamp",                                        "criteriaValue": "30; 50" },
  { "criteriaName": "Flange Diameter [mm]",                        "criteriaValue": "67" },
  { "criteriaName": "Jaw opening angle measurement [Degree]",      "criteriaValue": "130" },
  { "criteriaName": "Length [mm]",                                  "criteriaValue": "222,5" },
  { "criteriaName": "Mounting Angle [degrees]",                    "criteriaValue": "40" },
  { "criteriaName": "Mounting bore angle measurement [degree]",    "criteriaValue": "40" },
  { "criteriaName": "Number of mounting bores",                    "criteriaValue": "3" },
  { "criteriaName": "Number of Teeth",                             "criteriaValue": "9" },
  { "criteriaName": "Number of threaded holes",                    "criteriaValue": "0" },
  { "criteriaName": "Pinion Rest Position [mm]",                   "criteriaValue": "41" },
  { "criteriaName": "Position/Degree",                             "criteriaValue": "rechts" },
  { "criteriaName": "Rated Power [kW]",                            "criteriaValue": "0,9" },
  { "criteriaName": "Rotation Direction",                          "criteriaValue": "Anticlockwise rotation" },
  { "criteriaName": "Starter Type",                                "criteriaValue": "Self-supporting" },
  { "criteriaName": "Voltage [V]",                                 "criteriaValue": "12" },
  { "criteriaName": "Construction Year from",                      "criteriaValue": "199505; 200002; 200503" },
  { "criteriaName": "Construction Year to",                        "criteriaValue": "199910; 200505" },
  { "criteriaName": "Vehicle Identification Number (VIN) from",    "criteriaValue": "YD 471064; YD 471565" },
  { "criteriaName": "Engine Code",                                 "criteriaValue": "K16<K-Serie>" },
  { "criteriaName": "Transmission Type",                           "criteriaValue": "Manual Transmission" },
  { "criteriaName": "Manufacturer Restriction",                    "criteriaValue": "Bosch" }
]
```

**Response Fields**

| Field | Type | Description |
|-------|------|-------------|
| `[].criteriaName` | string | Criterion label, often with unit in brackets (e.g., `"Length [mm]"`, `"Rated Power [kW]"`) |
| `[].criteriaValue` | string | Always a string — see value formats below |

**`criteriaValue` Format Variants**

| Format | Example | How to Parse |
|--------|---------|--------------|
| Plain integer | `"9"`, `"67"`, `"12"` | `parseInt(value)` |
| Decimal with comma | `"10,5"`, `"222,5"`, `"0,9"` | `parseFloat(value.replace(',', '.'))` |
| Semicolon-separated list | `"30; 50"`, `"199505; 200002; 200503"` | `value.split('; ')` |
| Free-text string | `"rechts"`, `"Anticlockwise rotation"`, `"Self-supporting"` | Use as-is |
| Code with annotation | `"K16<K-Serie>"` | Strip `<...>` for matching |

**Criteria Categories**

| Category | Example Criteria Names | Notes |
|----------|----------------------|-------|
| **Physical dimensions** | `Length [mm]`, `Flange Diameter [mm]`, `Bore Diameter [mm]` | Comma decimal; may have multiple numbered variants (`Bore Diameter 2`, `Bore Ø 3`) |
| **Electrical** | `Voltage [V]`, `Rated Power [kW]` | Comma decimal |
| **Mechanical** | `Number of Teeth`, `Rotation Direction`, `Starter Type`, `Mounting Angle [degrees]` | Mix of numeric and free-text |
| **Fitment — time** | `Construction Year from`, `Construction Year to` | `YYYYMM` format; semicolon-separated when multiple ranges |
| **Fitment — VIN** | `Vehicle Identification Number (VIN) from` | Semicolon-separated when multiple VIN ranges |
| **Fitment — engine** | `Engine Code` | May include `<group>` annotation after the code |
| **Fitment — vehicle** | `Transmission Type`, `Manufacturer Restriction` | Free-text; `Manufacturer Restriction` names the OEM brand |

**Notes**

- This endpoint returns **more criteria** than the `articleAllSpecifications` embedded in [#35](#35-get-article-details-by-article-id) / [#38](#38-post-article-details-by-article-id--language-id) — specifically the fitment constraints (construction years, VINs, engine codes) are exclusive to this endpoint
- `criteriaValue` is **always a string**, regardless of content — always check for comma decimal separators before calling `parseFloat`
- Semicolon-separated values (`"30; 50"`, `"199505; 200002; 200503"`) represent **multiple valid values**, not a range — split on `"; "` to get individual values
- `Construction Year from/to` values are in `YYYYMM` format (e.g., `"199505"` = May 1995) — note that `from` may have more entries than `to` if some ranges are open-ended
- `country_filter_id` affects which fitment records are returned; change to filter by another market's vehicle population
- RapidAPI dashboard reported `Response Body Size: 2 Bytes` — likely a measurement artefact; the actual payload is substantially larger

---

## 40. POST Article Specifications by Article IDs

**URL:** `https://tecdoc-catalog.p.rapidapi.com/articles/get-article-specifications-list-of-articles-ids`  
**Method:** POST  
**Tested:** 2026-04-11 | Status: `200 OK` | Response Time: ~1336 ms

**Overview**

Batch endpoint that returns technical specifications for **multiple articles in a single request**. Equivalent to calling the `allSpecifications` field from [#36](#36-post-article-details-by-article-id-complete) for each article individually, but in one round-trip. No fitment criteria (construction years, VINs) — for those, use [#39](#39-get-article-criteria).

**Request**

**Headers:**
```
Content-Type: application/json
X-RapidAPI-Key: <your-api-key>
X-RapidAPI-Host: tecdoc-catalog.p.rapidapi.com
```

**Body** *(inferred from response — confirm field names from RapidAPI dashboard):*
```json
{
  "articleIds": [5522538, 6822931],
  "langId": 4
}
```

**Response**

```json
{
  "count": 2,
  "articles": [
    {
      "articleId": 5522538,
      "allSpecifications": [
        { "criteriaName": "Length [mm]", "criteriaValue": "190" },
        { "criteriaName": "Width [mm]",  "criteriaValue": "200" },
        { "criteriaName": "Height [mm]", "criteriaValue": "50"  },
        { "criteriaName": "Filter type", "criteriaValue": "9"   }
      ]
    },
    {
      "articleId": 6822931,
      "allSpecifications": [
        { "criteriaName": "Length [mm]", "criteriaValue": "199" },
        { "criteriaName": "Width [mm]",  "criteriaValue": "189" },
        { "criteriaName": "Height [mm]", "criteriaValue": "50"  },
        { "criteriaName": "Filter type", "criteriaValue": "9"   }
      ]
    }
  ]
}
```

**Response Fields**

| Field | Type | Description |
|-------|------|-------------|
| `count` | integer | Number of articles returned |
| `articles` | array | One entry per requested article |
| `articles[].articleId` | integer | TecDoc internal article ID — integer here (no string/integer inconsistency like #35/#38) |
| `articles[].allSpecifications` | array | Technical specifications for the article |
| `articles[].allSpecifications[].criteriaName` | string | Specification label with unit (e.g., `"Length [mm]"`) |
| `articles[].allSpecifications[].criteriaValue` | string | Always a string; may use comma decimal or semicolon list — see [#39 value formats](#39-get-article-criteria) |

**Field Name Inconsistency Across Endpoints**

| Endpoint | Specifications Field Name |
|----------|--------------------------|
| [#35 GET Details](#35-get-article-details-by-article-id) | `articleAllSpecifications` |
| [#38 POST Details](#38-post-article-details-by-article-id--language-id) | `articleAllSpecifications` |
| [#36 POST Complete](#36-post-article-details-by-article-id-complete) | `allSpecifications` |
| #40 POST Batch Specs | `allSpecifications` |
| [#39 GET Article Criteria](#39-get-article-criteria) | root array (no wrapper field) |

**Notes**

- Use this endpoint when building a **comparison view** or **bulk catalogue import** — avoids N individual API calls for N articles
- `allSpecifications` here matches the field name from [#36](#36-post-article-details-by-article-id-complete), not the `articleAllSpecifications` name used in [#35](#35-get-article-details-by-article-id) / [#38](#38-post-article-details-by-article-id--language-id)
- `articleId` in the response array is an **integer** — no root-level string/integer inconsistency like in #35/#38
- Fitment criteria (construction years, VINs, engine codes) are **not included** — for those, call [#39 GET Article Criteria](#39-get-article-criteria) per article
- RapidAPI dashboard reported `Response Body Size: 2 Bytes` — likely a measurement artefact; the actual payload scales with number of articles

---

## 41. GET Article List by Vehicle ID & Category ID

**URL:** `<!-- TODO: confirm URL from RapidAPI dashboard -->`  
**Method:** GET  
**Tested:** 2026-04-11 | Status: `200 OK` *(URL truncated in source message)*

**Overview**

The core **product listing endpoint** for a fitment-aware parts catalog. Given a vehicle ID and a category ID, returns all compatible articles across all suppliers. This is the endpoint behind a "select vehicle → browse category → see matching parts" UI flow.

**Path / Query Parameters** *(infer from response — confirm exact names from RapidAPI dashboard)*

| Parameter | Type | Example | Description |
|-----------|------|---------|-------------|
| `vehicleId` | integer | `19942` | TecDoc vehicle type ID — from vehicle lookup endpoints (#1–#10) |
| `categoryId` | integer | `100260` | TecDoc category ID — from category endpoints (#27–#34) |
| `langId` | integer | `4` | Language ID for product name labels |

**Response**

```json
{
  "vehicleId": "19942",
  "categoryId": "100260",
  "countArticles": 120,
  "articles": [
    {
      "articleId": 5522538,
      "articleNo": "A63193",
      "supplierName": "1A FIRST AUTOMOTIVE",
      "supplierId": 4814,
      "articleProductName": "Air Filter",
      "productId": 8,
      "articleMediaType": "JPEG",
      "articleMediaFileName": "975108278fe2f0e674a0dd0c05fa878ba5be381c.webp",
      "s3image": "https://fsn1.your-objectstorage.com/tecdoc2025/media_files/images/4814/975108278fe2f0e674a0dd0c05fa878ba5be381c.webp"
    },
    {
      "articleId": 6822931,
      "articleNo": "EST-20-0K-K21",
      "supplierName": "4X4 ESTANFI",
      "supplierId": 6372,
      "articleProductName": "Air Filter",
      "productId": 8,
      "articleMediaType": "JPEG",
      "articleMediaFileName": "bd0012bd4a3c91ba5588b043c93605226508b457.webp",
      "s3image": "https://fsn1.your-objectstorage.com/tecdoc2025/media_files/images/6372/bd0012bd4a3c91ba5588b043c93605226508b457.webp"
    }
  ]
}
```

**Response Fields**

| Field | Type | Description |
|-------|------|-------------|
| `vehicleId` | string | Echoed vehicle ID — **returned as string** even though passed as integer |
| `categoryId` | string | Echoed category ID — **returned as string** even though passed as integer |
| `countArticles` | integer | Total number of compatible articles found |
| `articles` | array | Full list of matching articles (all returned at once — no pagination observed) |
| `articles[].articleId` | integer | TecDoc internal article ID |
| `articles[].articleNo` | string | Supplier part number |
| `articles[].supplierName` | string | Supplier brand name |
| `articles[].supplierId` | integer | TecDoc internal supplier ID |
| `articles[].articleProductName` | string | Product type name — same for all items when querying a single category |
| `articles[].productId` | integer | Generic article / product group ID — matches the queried category's product; see [#34 List All Product Names](#34-get-list-all-product-names) |
| `articles[].articleMediaType` | string | Declared media type: `JPEG`, `JPG`, `BMP`, `PNG` — **unreliable; actual file is always `.webp`** |
| `articles[].articleMediaFileName` | string | SHA-1 hash filename with `.webp` extension |
| `articles[].s3image` | string | Direct S3 image URL; pattern: `https://fsn1.your-objectstorage.com/tecdoc2025/media_files/images/{supplierId}/{articleMediaFileName}` |

**`articleMediaType` Values Observed**

| Declared value | Actual file extension | Count in sample |
|---------------|----------------------|----------------|
| `JPEG` | `.webp` | Most common |
| `JPG` | `.webp` | Common |
| `BMP` | `.webp` | Occasional |
| `PNG` | `.webp` | Occasional |
| `GIF` | `.gif` | Rare — **GIF is the one exception where file extension matches declared type** |

Do not use `articleMediaType` to determine the image format — use the file extension from `articleMediaFileName` or the `s3image` URL directly. GIF is the only declared type that reliably predicts the actual extension.

**Notes**

- `vehicleId` and `categoryId` are echoed back as **strings** in the response, despite being numeric inputs — always use string comparison when checking these against request values
- `countArticles` matches `articles.length` — no pagination: the full list is returned in one response; plan for potentially large payloads (100+ items for popular categories/vehicles)
- All articles in a single response share the same `articleProductName` and `productId` because the category filter ensures they are all the same product type
- `articleMediaFileName` uses a SHA-1 content hash — multiple suppliers may share the **same image file** (same hash, same filename) when they use the same product photo; the `supplierId` in the S3 path differentiates the URL even if the file content is identical
- The `s3image` URL is always present for this listing endpoint (unlike [#36](#36-post-article-details-by-article-id-complete) / [#37](#37-get-article-details--compatibility-by-article-id) where it can be `null`)
- `articleId` values here can be fed directly into [#35](#35-get-article-details-by-article-id), [#36](#36-post-article-details-by-article-id-complete), [#38](#38-post-article-details-by-article-id--language-id), [#39](#39-get-article-criteria), or [#40](#40-post-article-specifications-by-article-ids) for detailed specifications
- For building a comparison view across multiple results, batch their IDs into [#40 POST Article Specifications by Article IDs](#40-post-article-specifications-by-article-ids) to avoid N individual spec calls

---

## 42. POST Article List by Vehicle ID & Category ID

**URL:** `<!-- TODO: confirm URL from RapidAPI dashboard -->`  
**Method:** POST  
**Tested:** 2026-04-11 | Status: `200 OK` *(URL truncated in source message)*

**Overview**

POST equivalent of [#41 GET Article List by Vehicle ID & Category ID](#41-get-article-list-by-vehicle-id--category-id). Accepts `vehicleId` and `categoryId` in the request body instead of URL path/query parameters. Returns an **identical response structure and dataset** for the same inputs.

**Request**

**Headers:**
```
Content-Type: application/json
X-RapidAPI-Key: <your-api-key>
X-RapidAPI-Host: tecdoc-catalog.p.rapidapi.com
```

**Body** *(inferred — confirm exact field names from RapidAPI dashboard):*
```json
{
  "vehicleId": 19942,
  "categoryId": 100260,
  "langId": 4
}
```

**Response**

Response structure and all fields are **identical to [#41 GET Article List by Vehicle ID & Category ID](#41-get-article-list-by-vehicle-id--category-id)** — refer to that entry for the full response sample, field table, and `articleMediaType` reference.

**#41 vs #42 Comparison**

| Aspect | [#41 GET Article List](#41-get-article-list-by-vehicle-id--category-id) | #42 POST Article List |
|--------|-------------------------------------------------------------------------|----------------------|
| Method | GET | POST |
| Parameters | Path / query params | Request body |
| Response structure | Identical | Identical |
| HTTP caching | Cacheable by URL | Not cacheable (POST) |
| Use case | Standard REST lookup | When IDs are part of a larger JSON payload |

**Notes**

- Response is byte-for-byte identical to [#41](#41-get-article-list-by-vehicle-id--category-id) for the same inputs — there is no additional filtering or enrichment from using POST over GET
- All notes from [#41](#41-get-article-list-by-vehicle-id--category-id) apply here: `vehicleId`/`categoryId` echoed as strings, no pagination, `articleMediaType` unreliable except for `GIF`

---

## 43. GET Compatible Vehicles by Article No & Supplier ID

**URL:** `https://tecdoc-catalog.p.rapidapi.com/articles/get-compatible-cars-by-article-number/type-id/{type_id}?articleNo={article_no}&supplierId={supplier_id}&langId={lang_id}&countryFilterId={country_filter_id}`  
**Method:** GET  
**Tested:** 2026-04-11 | Status: `200 OK` | Response Time: ~1268 ms

**Overview**

Reverse fitment lookup: given a **supplier part number + supplier ID**, returns all compatible vehicles. This is the "fits X vehicles" direction, the counterpart to [#41 GET Article List by Vehicle ID & Category ID](#41-get-article-list-by-vehicle-id--category-id) which goes the other way. Input is `articleNo` (human-readable part number) rather than the internal `articleId` used by [#36](#36-post-article-details-by-article-id-complete) / [#37](#37-get-article-details--compatibility-by-article-id).

**Parameters**

| Parameter | Location | Type | Example | Description |
|-----------|----------|------|---------|-------------|
| `type_id` | path | integer | `1` | Vehicle type filter — `1` = Passenger Cars; see [#5 Vehicle Types](#5-get-vehicle-types) |
| `articleNo` | query | string | `C+2029` | Supplier part number URL-encoded (spaces as `+`) |
| `supplierId` | query | integer | `4` | TecDoc supplier ID — required to disambiguate when multiple suppliers share the same part number |
| `langId` | query | integer | `4` | Language ID for name labels (e.g., `4` = English GB) |
| `countryFilterId` | query | integer | `63` | Country filter (e.g., `63` = Germany) — narrows the vehicle population |

**Response**

```json
{
  "countArticles": 1,
  "articles": [
    {
      "articleId": 6159438,
      "articleNo": "C 2029",
      "articleProductName": "Air Filter",
      "supplierName": "MANN-FILTER",
      "supplierId": 4,
      "compatibleCars": [
        {
          "vehicleId": 4851,
          "modelId": 6234,
          "manufacturerName": "KIA",
          "modelName": "CEE'D SW (ED)",
          "typeEngineName": "1.4 CVVT",
          "constructionIntervalStart": "2009-07-01",
          "constructionIntervalEnd": "2012-12-01"
        },
        {
          "vehicleId": 19942,
          "modelId": 5626,
          "manufacturerName": "KIA",
          "modelName": "CEE'D Hatchback (ED)",
          "typeEngineName": "1.6 CRDi 115",
          "constructionIntervalStart": "2006-12-01",
          "constructionIntervalEnd": "2012-12-01"
        },
        {
          "vehicleId": 51241,
          "modelId": 36000,
          "manufacturerName": "HYUNDAI",
          "modelName": "ELANTRA V Estate",
          "typeEngineName": "2.0",
          "constructionIntervalStart": "2011-09-01",
          "constructionIntervalEnd": null
        }
      ]
    }
  ]
}
```

**Response Fields**

| Field | Type | Description |
|-------|------|-------------|
| `countArticles` | integer | Number of articles matched — typically `1` when querying a specific `articleNo + supplierId` |
| `articles` | array | One entry per matched article |
| `articles[].articleId` | integer | TecDoc internal article ID |
| `articles[].articleNo` | string | Supplier part number (decoded, spaces restored) |
| `articles[].articleProductName` | string | Product type name |
| `articles[].supplierName` | string | Supplier brand name |
| `articles[].supplierId` | integer | TecDoc internal supplier ID |
| `articles[].compatibleCars` | array | All compatible vehicle types, filtered by `type_id` and `countryFilterId` |
| `compatibleCars[].vehicleId` | integer | TecDoc vehicle type ID — usable in [#41](#41-get-article-list-by-vehicle-id--category-id) / [#42](#42-post-article-list-by-vehicle-id--category-id) |
| `compatibleCars[].modelId` | integer | TecDoc model ID — groups multiple `vehicleId` variants under one model line |
| `compatibleCars[].manufacturerName` | string | Manufacturer brand (e.g., `"KIA"`, `"HYUNDAI"`, `"HYUNDAI (BEIJING)"`) |
| `compatibleCars[].modelName` | string | Model name with body style and generation code (e.g., `"CEE'D Hatchback (ED)"`) |
| `compatibleCars[].typeEngineName` | string | Engine variant within the model (e.g., `"1.6 CRDi 115"`, `"2.0 CVVT"`, `"LPG"`) |
| `compatibleCars[].constructionIntervalStart` | string | Production start date in `YYYY-MM-DD` format |
| `compatibleCars[].constructionIntervalEnd` | string \| null | Production end date in `YYYY-MM-DD` format — **`null` if vehicle is still in production or no end date is recorded** |

**`compatibleCars` vs #36/#37 `compatibleCars` Comparison**

| Aspect | [#36](#36-post-article-details-by-article-id-complete) / [#37](#37-get-article-details--compatibility-by-article-id) `compatibleCars` | #43 `compatibleCars` |
|--------|--------------------------------------------------------------------|----------------------|
| Same fields | Yes — `vehicleId`, `modelId`, `manufacturerName`, `modelName`, `typeEngineName`, `constructionIntervalStart`, `constructionIntervalEnd` | Same |
| Date format | `YYYY-MM-DD` | `YYYY-MM-DD` |
| Null end date | Possible | Possible |
| Lookup key | `articleId` (internal) | `articleNo + supplierId` (human-readable) |
| Vehicle type filter | `type_id` path param (#37 only) | `type_id` path param |
| Country filter | `countryFilterId` query param (#37 only) | `countryFilterId` query param |

**Fitment Loop — #41 ↔ #43**

These two endpoints form a bidirectional lookup pair:

| Direction | Endpoint | Input → Output |
|-----------|----------|---------------|
| Vehicle → Parts | [#41 GET Article List](#41-get-article-list-by-vehicle-id--category-id) | `vehicleId + categoryId` → articles |
| Part → Vehicles | #43 GET Compatible Vehicles | `articleNo + supplierId` → `compatibleCars` |

**Notes**

- `articleNo` must be URL-encoded — spaces become `+` (e.g., `C 2029` → `C+2029`); pass via query string, not path
- `supplierId` is required to disambiguate — multiple suppliers can share the same `articleNo` string
- `constructionIntervalEnd: null` means the vehicle is either still in current production or TecDoc has no recorded end date — treat as "no known end date", not as an error
- `manufacturerName: "HYUNDAI (BEIJING)"` is a distinct market-specific manufacturer entry, separate from plain `"HYUNDAI"` — both may appear for the same article
- The `vehicleId` values in `compatibleCars` are the same IDs used throughout the vehicle lookup endpoints (#1–#10, #41–#42) — confirmed: `vehicleId: 19942` (KIA CEE'D Hatchback 1.6 CRDi 115) appears here as a compatible vehicle for this article, and was used as the test vehicle in #41/#42
- For an article found via `articleId`, prefer [#36](#36-post-article-details-by-article-id-complete) or [#37](#37-get-article-details--compatibility-by-article-id) to get fitment data; use this endpoint when you only have the supplier part number from an external source (OEM cross-reference, printed label, etc.)

---

## 44. GET List Accessory Parts by Article ID

<!-- TODO: confirm URL from RapidAPI dashboard -->

**Method:** GET
**Status:** 200 OK
**Response Time:** (confirm from RapidAPI dashboard)
**Response Body Size:** (confirm from RapidAPI dashboard)

### Overview

Returns all vehicle-type fitment rows for an article, one row per compatible vehicle type. The response is a denormalized flat list — the same article is repeated N times where N equals the number of vehicle types it fits, with each row carrying the fitment criteria specific to that vehicle type.

The key difference from [#43 GET Compatible Vehicles](#43-get-compatible-vehicles-by-article-no--supplier-id) (which also maps parts to vehicles) is structure: #43 nests all compatible vehicles under a single article object with a `compatibleCars` array; this endpoint is fully flat with one article row per vehicle type.

### Parameters

| Parameter | Location | Type | Required | Description |
|-----------|----------|------|----------|-------------|
| `article_id` | path | integer | Yes | TecDoc internal article ID (e.g., `2569937`) — obtain from any article search endpoint |
| (additional params) | — | — | — | Confirm full URL and query params from RapidAPI dashboard |

### Response Sample

```json
{
  "countArticles": 722,
  "articles": [
    {
      "articleId": 2569937,
      "articleNo": "30178 01",
      "articleStatus": "Normal",
      "articleProductName": "Bellow, steering",
      "typeInfo": "PC:4613",
      "groupName": null,
      "articleCriteria": "Construction Year to: 199810; Vehicle Identification Number (VIN) from: 8D-X-053 001; Vehicle Identification Number (VIN) from: 8D-Y-005 049; Vehicle Identification Number (VIN) to: 8D-X-053 000; Fitting Position: Front Axle; Fitting Position: Front Axle Left; Fitting Position: Front Axle Right; Length [mm]: 205; Length [mm]: 255; Material: Thermoplast; Material: Rubber; Left-/right-hand drive vehicles: for left-hand drive vehicles; Left-/right-hand drive vehicles: for right-hand drive vehicles; Vehicle Equipment: for vehicles with power steering; Inner Diameter 1 [mm]: 18; Inner Diameter 1 [mm]: 20; Inner Diameter 2 [mm]: 54; Inner Diameter 2 [mm]: 63"
    },
    {
      "articleId": 2569937,
      "articleNo": "30178 01",
      "articleStatus": "Normal",
      "articleProductName": "Bellow, steering",
      "typeInfo": "PC:4614",
      "groupName": null,
      "articleCriteria": "Construction Year to: 199810; Vehicle Identification Number (VIN) from: 8D-X-053 001; Vehicle Identification Number (VIN) from: 8D-X-303 810; Vehicle Identification Number (VIN) from: 8D-Y-005 049; Vehicle Identification Number (VIN) to: 8D-X-053 000; Fitting Position: Front Axle; Fitting Position: Front Axle Left; Fitting Position: Front Axle Right; Length [mm]: 205; Length [mm]: 255; Material: Thermoplast; Material: Rubber; Left-/right-hand drive vehicles: for left-hand drive vehicles; Left-/right-hand drive vehicles: for right-hand drive vehicles; Vehicle Equipment: for vehicles with power steering; Inner Diameter 1 [mm]: 18; Inner Diameter 1 [mm]: 20; Inner Diameter 2 [mm]: 54; Inner Diameter 2 [mm]: 63"
    },
    {
      "articleId": 2569937,
      "articleNo": "30178 01",
      "articleStatus": "Normal",
      "articleProductName": "Bellow, steering",
      "typeInfo": "PC:5724",
      "groupName": null,
      "articleCriteria": "Construction Year from: 199901; Construction Year from: 199902; Construction Year to: 199901; Construction Year to: 199902; Vehicle Identification Number (VIN) to: 3B XP319 680; Vehicle Identification Number (VIN) to: 3B-XE376 641; Fitting Position: Front Axle; Fitting Position: Front Axle Left; Fitting Position: Front Axle Right; Length [mm]: 205; Length [mm]: 255; Material: Thermoplast; Material: Rubber; Left-/right-hand drive vehicles: for left-hand drive vehicles; Left-/right-hand drive vehicles: for right-hand drive vehicles; Vehicle Equipment: for vehicles with power steering; Inner Diameter 1 [mm]: 18; Inner Diameter 1 [mm]: 20; Inner Diameter 2 [mm]: 54; Inner Diameter 2 [mm]: 63"
    }
  ]
}
```

### Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `countArticles` | integer | Total number of fitment rows returned — this is **rows, not distinct articles**; the same article can appear hundreds of times (once per compatible vehicle type) |
| `articles` | array | Flat list of fitment rows — one entry per compatible vehicle type |
| `articles[].articleId` | integer | TecDoc internal article ID — same value repeated for every row in the response |
| `articles[].articleNo` | string | Supplier part number (spaces preserved, e.g., `"30178 01"`) |
| `articles[].articleStatus` | string | Publication status of the article (e.g., `"Normal"`) |
| `articles[].articleProductName` | string | Product category name (e.g., `"Bellow, steering"`) |
| `articles[].typeInfo` | string | Vehicle type reference in `"PC:{typeId}"` format — `PC` = Passenger Car; `typeId` is the TecDoc vehicle type ID, usable as `vehicleId` in [#41](#41-get-article-list-by-vehicle-id--category-id) / [#42](#42-post-article-list-by-vehicle-id--category-id) |
| `articles[].groupName` | string \| null | Observed as `null` in all sample rows — purpose not determined from available data |
| `articles[].articleCriteria` | string | Semicolon-separated fitment criteria for **this specific vehicle type** — format: `"CriteriaName: value; CriteriaName: value; ..."` |

### `articleCriteria` String Format

The `articleCriteria` field is a flat inline string. Each criterion is formatted as `"Name: value"` and criteria are separated by `"; "`. A criterion name can appear multiple times when multiple values apply (e.g., two `"Length [mm]"` entries).

```
"Construction Year to: 199810; Fitting Position: Front Axle; Fitting Position: Front Axle Left; Length [mm]: 205; Length [mm]: 255; Material: Thermoplast; Material: Rubber"
```

| Pattern | Example | Meaning |
|---------|---------|---------|
| Single value | `"Fitting Position: Front Axle"` | One value for this criterion |
| Repeated name | `"Length [mm]: 205; Length [mm]: 255"` | Multiple accepted values for same criterion |
| Construction year `YYYYMM` | `"Construction Year to: 199810"` | Year 1998, month 10 (October) |
| Construction year `YYYYMM` from/to | `"Construction Year from: 199901; Construction Year to: 199902"` | Narrow production window |
| VIN range | `"VIN from: 8D-X-053 001; VIN to: 8D-X-053 000"` | Specific chassis number range |
| Equipment restriction | `"Vehicle Equipment: for vehicles with power steering"` | Fitment requires specific vehicle equipment |
| Drive side | `"Left-/right-hand drive vehicles: for left-hand drive vehicles"` | Market/drive-side restriction |

### `typeInfo` Format

| Component | Example | Meaning |
|-----------|---------|---------|
| `PC` | `"PC:4613"` | Vehicle category prefix — `PC` = Passenger Car |
| `:{typeId}` | `":4613"` | TecDoc vehicle type ID — extractable for use as `vehicleId` in other endpoints |

Extract the numeric ID with: `typeInfo.split(":")[1]` → `"4613"` → parse as integer `4613`.

### Comparison: #44 vs #43 (Part → Vehicles)

Both endpoints go from a known article to its compatible vehicles, but use different structures:

| Aspect | [#43 GET Compatible Vehicles](#43-get-compatible-vehicles-by-article-no--supplier-id) | #44 GET Accessory Parts |
|--------|---------------------------------------------------------------------------------------|-------------------------|
| Lookup key | `articleNo + supplierId` (human-readable) | `articleId` (internal) |
| Output structure | Nested — one article row with `compatibleCars[]` array | Flat — one row per vehicle type, article fields repeated |
| Vehicle identity | `vehicleId` (integer field) | `typeInfo` string (`"PC:{id}"`) |
| Vehicle details | `manufacturerName`, `modelName`, `typeEngineName`, `constructionIntervalStart/End` | Absent — vehicle info only in `articleCriteria` string |
| Fitment criteria | In `compatibleCars[].constructionIntervalStart/End` only | Full inline `articleCriteria` string per row |
| `articleStatus` | Not present | Present (`"Normal"`) |
| `groupName` | Not present | Present (null in sample) |
| `countArticles` meaning | Count of distinct articles matching the lookup | Count of total fitment rows (same article × N vehicle types) |

### Comparison: #44 `articleCriteria` vs #39 Criteria Objects

| Aspect | [#39 GET Article Criteria](#39-get-article-criteria) | #44 `articleCriteria` string |
|--------|-------------------------------------------------------|------------------------------|
| Format | Array of structured objects (`criteriaId`, `criteriaDescription`, `criteriaValue`, etc.) | Single inline semicolon-delimited string |
| Scope | All criteria for the article across all vehicles | Criteria scoped to one specific vehicle type |
| Machine-readability | High — structured fields, typed values | Low — requires string parsing |
| Criteria count | More — includes all fitment and spec criteria | Vehicle-type-specific subset |
| Construction year format | `YYYYMM` integer string (e.g., `"199810"`) | `YYYYMM` inline (e.g., `"Construction Year to: 199810"`) |

### Notes

- `countArticles` is the row count, not the distinct article count — a single article fitting 722 vehicle types yields `countArticles: 722` with the same `articleId` and `articleNo` repeated on every row
- `typeInfo: "PC:4613"` — the numeric suffix (e.g., `4613`) is the TecDoc vehicle type ID; this is the same integer used as `vehicleId` in [#41](#41-get-article-list-by-vehicle-id--category-id) / [#42](#42-post-article-list-by-vehicle-id--category-id) and returned as `vehicleId` in [#43](#43-get-compatible-vehicles-by-article-no--supplier-id)
- `groupName: null` was observed on all sample rows — this field may be populated for different article types or catalogue configurations; its purpose is not determinable from the current sample
- `articleCriteria` criteria names use free-text labels (e.g., `"Left-/right-hand drive vehicles:"`) — these match the `criteriaDescription` values returned by [#39](#39-get-article-criteria) but are not accompanied by machine-readable IDs in this endpoint
- Construction year values in `articleCriteria` use `YYYYMM` format (consistent with [#39](#39-get-article-criteria)), not `YYYY-MM-DD` (which is used for `constructionIntervalStart/End` in [#43](#43-get-compatible-vehicles-by-article-no--supplier-id))
- The "RapidAPI Response Body Size: 2 Bytes" measurement for large responses is a known dashboard artefact — actual payload for `countArticles: 722` is substantially larger

---

## 45. GET Vehicle Spare Part Criteria

<!-- TODO: confirm URL from RapidAPI dashboard -->

**Method:** GET
**Status:** 200 OK
**Response Time:** (confirm from RapidAPI dashboard)
**Response Body Size:** (confirm from RapidAPI dashboard)

### Overview

Returns a flat array of all criteria names and their aggregated possible values across all spare parts for a given vehicle. Unlike [#39 GET Article Criteria](#39-get-article-criteria) (which returns structured criteria for one specific article), this endpoint returns a catalogue-level view: every distinct `criteriaName` that appears on any spare part for the vehicle, each carrying a semicolon-separated list of all distinct values observed across all matching parts.

This is useful for building filter UIs — e.g., to show users what dimensions, materials, or specifications are available when browsing parts for a specific vehicle.

### Parameters

| Parameter | Location | Type | Required | Description |
|-----------|----------|------|----------|-------------|
| (params) | — | — | — | Confirm full URL and query params from RapidAPI dashboard |

### Response Sample

```json
[
  {
    "criteriaName": "Fabrication Number",
    "criteriaValue": "1369; 1376; 2595; A-AU-017; A-VW-013; AB-VW-002; ..."
  },
  {
    "criteriaName": "Glove Outer Surface",
    "criteriaValue": "Smooth"
  },
  {
    "criteriaName": "Diameter from [mm]",
    "criteriaValue": "48; 54,5; 56; 66"
  },
  {
    "criteriaName": "Operating temperature from [°C]",
    "criteriaValue": "-40"
  },
  {
    "criteriaName": "Packaging",
    "criteriaValue": "Blister Pack; Hard shell case; In Plastic Case; Plastic Case; Poly bag; Sheet Steel Cassette; in tool module (soft PU foam inlay)"
  },
  {
    "criteriaName": "Maintenance free",
    "criteriaValue": ""
  },
  {
    "criteriaName": "non-directional",
    "criteriaValue": ""
  },
  {
    "criteriaName": "Construction Year from",
    "criteriaValue": "200512; 200601; 200602; 200603; 200604; 200605; ..."
  },
  {
    "criteriaName": "Construction Year to",
    "criteriaValue": "200512; 200601; 200602; 200604; 200605; 200606; ..."
  },
  {
    "criteriaName": "Weight [kg]",
    "criteriaValue": "0; 0,00025; 0,00046; 0,0005; ..."
  }
]
```

### Response Structure

The response is a **raw JSON array** — there is no wrapping object, no `count` field, and no pagination envelope.

| Field | Type | Description |
|-------|------|-------------|
| `[].criteriaName` | string | Human-readable criteria label (e.g., `"Diameter from [mm]"`, `"Bellows Material"`) |
| `[].criteriaValue` | string | Semicolon-separated list of all distinct values observed across all matching parts — or **empty string `""`** for boolean/flag criteria |

### `criteriaValue` Patterns

| Pattern | Example | Meaning |
|---------|---------|---------|
| Single value | `"Smooth"` | Only one value observed across all parts |
| Semicolon list | `"48; 54,5; 56; 66"` | Multiple distinct values observed |
| Decimal comma | `"54,5"` | European decimal separator (consistent with other endpoints) |
| Empty string | `""` | Boolean/flag criterion — presence of the name indicates the property applies (no value needed) |
| Long aggregated list | `"0; 0,00025; 0,0005; ..."` | Many distinct values aggregated across hundreds of articles (e.g., `"Weight [kg]"`) |
| YYYYMM format | `"200512; 200601; ..."` | Construction year/month — consistent with [#39](#39-get-article-criteria) and [#44](#44-get-list-accessory-parts-by-article-id) |

### Boolean / Flag Criteria

Several criteria have `criteriaValue: ""` — these are boolean flags where the existence of the criterion is the information (no associated value). Examples observed:

| Criteria Name | Meaning |
|---------------|---------|
| `"Maintenance free"` | Part is maintenance-free |
| `"non-directional"` | Part is non-directional (e.g., tyre or brake disc) |
| `"replacement in pairs recommended"` | Manufacturer recommends replacing in pairs |
| `"EG/ECE conform"` | Meets EU/ECE regulation |
| `"with ECE/ABE approval"` | Has approval certificate |
| `"without ECE/ABE approval"` | Explicitly without approval |
| `"Standard Set"` | Part is a standard set |
| `"straight version"` / `"angled version"` | Orientation variant |
| `"Repair solution"` | Part is a repair solution |
| `"no performance increase"` | Part does not increase performance over OEM |
| `"Observe illustration"` | Installation note requiring visual reference |

### Criteria Categories Observed

| Category | Example Criteria Names |
|----------|----------------------|
| **Dimensions** | `Diameter from [mm]`, `Diameter up to [mm]`, `Total Length [mm]`, `Inner Diameter 1 [mm]`, `Outer Diameter [mm]`, `Ring Thickness [mm]`, `Head Height [mm]`, `Head Width [mm]`, `Core Length [mm]`, `Core Width [mm]`, `Core Depth [mm]` |
| **Material** | `Bellows Material`, `Seal Material`, `Belt Material`, `Blade material`, `Protective Sleeve Material`, `Insulation Material`, `Base body material`, `Compression ring material` |
| **Temperature / Performance** | `Operating temperature from [°C]`, `Operating temperature to [°C]`, `Temperature range from [°C]`, `Temperature range to [°C]`, `RPM from [1/min]`, `RPM to [1/min]`, `Rated Power [W]`, `Power [W]` |
| **Electrical** | `Voltage to [V]`, `Current Strength [A]`, `Operating voltage from/to [V]`, `Cable Cross Section [mm²]`, `Number of connectors` |
| **Fitment / Construction interval** | `Construction Year from`, `Construction Year to` (YYYYMM format), `Engine Number from/to`, `Model Year from/to`, `Production date from/to`, `Axle Load [kg] to` |
| **Vehicle model restrictions** | `for model code`, `not for model code`, `for type code`, `for RPO number`, `for combined PR number` |
| **Cross-references** | `Fabrication Number`, `ETN number`, `contains article number`, `Available as universal article as well (see article no.)`, `contains more articles than the OE kit (art. no.)` |
| **Packaging & weight** | `Packaging`, `Net Weight [g]`, `Gross Weight [g]`, `Weight [kg]`, `Fill quantity [l]` |
| **Surface / finish** | `Glove Outer Surface`, `Blade surface`, `Cutting Surface`, `Jaw Surface`, `Contact surface`, `Shaft surface`, `Pliers head surface`, `Tool handle surface` |
| **Standards / approvals** | `ACEA specification`, `API specification`, `DOT specification`, `SAE viscosity class`, `EU Ordinance (number)`, `Headlamp approval number`, `ABE No.`, `Goods tariff number` |
| **Boolean flags** | `Maintenance free`, `non-directional`, `replacement in pairs recommended`, `EG/ECE conform`, `with ECE/ABE approval`, `Standard Set`, `Repair solution` |
| **Installation notes** | `Observe illustration`, `Assy./disassy. by qualified personnel required!`, `Always compare old and new part`, `Vehicle manufacturer's additional parts required` |

### Comparison: #45 vs #39 (GET Article Criteria)

| Aspect | [#39 GET Article Criteria](#39-get-article-criteria) | #45 GET Vehicle Spare Part Criteria |
|--------|------------------------------------------------------|--------------------------------------|
| Lookup key | Single `articleId` | Vehicle identifier (confirm from URL) |
| Scope | Criteria for one specific article | Aggregated criteria across ALL spare parts for the vehicle |
| Response shape | Array of structured objects | Raw array |
| Fields per item | `criteriaId`, `criteriaDescription`, `criteriaValue`, `criteriaAbbrValue`, `criteriaImmutable`, `criteriaSort`, `isInterval` | `criteriaName`, `criteriaValue` only |
| `criteriaValue` meaning | Value(s) for this article in this criterion | All distinct values seen across all parts for this vehicle |
| Machine ID | Yes (`criteriaId`) | No (name-only) |
| Use case | Displaying specs/fitment for a specific part | Building filter/facet UI for parts browsing |
| Value list length | Short (few values for one part) | Potentially very long (hundreds of values aggregated across many parts) |

### Notes

- Response is a raw JSON array — no wrapping object, no `count` or `total` field; array length is the criterion count
- `criteriaValue: ""` (empty string) means a boolean flag criterion — presence of the name in the array is itself the data
- `criteriaValue` lists are sorted and deduplicated across all parts for the vehicle — the same value will not appear twice in a single criterion's list
- Large criteria like `Weight [kg]` or `Outer Diameter [mm]` can have hundreds of distinct values; parse with `.split("; ")` to get a usable array
- Decimal values use European comma notation (`"54,5"` = 54.5) — consistent across all endpoints in this API
- Construction year values follow `YYYYMM` format (same as [#39](#39-get-article-criteria) and [#44](#44-get-list-accessory-parts-by-article-id)), not `YYYY-MM-DD`
- `criteriaName` values are human-readable free-text labels — there are no machine-readable `criteriaId` fields in this endpoint (unlike [#39](#39-get-article-criteria))

---

## 46. GET Parts Diagram Coordinates

**Method:** GET
**Status:** 200 OK
**Response Time:** 1067 ms
**Date:** 2026-04-11T11:00:18.032Z
**Response Body Size:** 2 Bytes *(RapidAPI dashboard artefact — actual payload is substantially larger)*
**URL:** `https://tecdoc-catalog.p.rapidapi.com/articles/selecting-item-coordinators-on-the-parts-diagram-image-for-the-parts-list/article-id/{article_id}`

### Overview

Given any `articleId`, returns all articles plotted on the **same parts diagram image** as that article, along with their hotspot coordinates. The input article is used to look up which diagram it belongs to; the response contains every article on that diagram (which may or may not include the input article itself).

Each result item combines article identity (`articleId`, `articleNo`, `supplierId`) with diagram metadata (the shared image file) and the precise hotspot bounding box (`senCoordX`, `senCoordY`, `senCoordWidth`, `senCoordHeight`, `senCordType`) for that article's position on the diagram.

### Parameters

| Parameter | Location | Type | Required | Description |
|-----------|----------|------|----------|-------------|
| `article_id` | path | integer (passed as string) | Yes | TecDoc internal article ID — used to identify which parts diagram this article belongs to (e.g., `124926`) |

### Response Sample

```json
[
  {
    "articleId": 4952839,
    "articleNo": "862.562",
    "supplierId": 10,
    "supplierName": "ELRING",
    "articleMediaFileName": "ddf4b23512565626c8b165860fd546a71904f999.webp",
    "articleMediaType": "JPG",
    "senCoordId": 6,
    "senCoordX": 243,
    "senCoordY": 239,
    "senCoordWidth": 188,
    "senCoordHeight": 188,
    "senCordType": "Circle",
    "s3image": "https://fsn1.your-objectstorage.com/tecdoc2025/media_files/images/10/ddf4b23512565626c8b165860fd546a71904f999.webp"
  },
  {
    "articleId": 124918,
    "articleNo": "001.796",
    "supplierId": 10,
    "supplierName": "ELRING",
    "articleMediaFileName": "ddf4b23512565626c8b165860fd546a71904f999.webp",
    "articleMediaType": "JPG",
    "senCoordId": 1,
    "senCoordX": 155,
    "senCoordY": 86,
    "senCoordWidth": 158,
    "senCoordHeight": 158,
    "senCordType": "Circle",
    "s3image": "https://fsn1.your-objectstorage.com/tecdoc2025/media_files/images/10/ddf4b23512565626c8b165860fd546a71904f999.webp"
  },
  {
    "articleId": 3306735,
    "articleNo": "432.040",
    "supplierId": 10,
    "supplierName": "ELRING",
    "articleMediaFileName": "ddf4b23512565626c8b165860fd546a71904f999.webp",
    "articleMediaType": "JPG",
    "senCoordId": 3,
    "senCoordX": 503,
    "senCoordY": 304,
    "senCoordWidth": 126,
    "senCoordHeight": 126,
    "senCordType": "Circle",
    "s3image": "https://fsn1.your-objectstorage.com/tecdoc2025/media_files/images/10/ddf4b23512565626c8b165860fd546a71904f999.webp"
  },
  {
    "articleId": 3442627,
    "articleNo": "470.290",
    "supplierId": 10,
    "supplierName": "ELRING",
    "articleMediaFileName": "ddf4b23512565626c8b165860fd546a71904f999.webp",
    "articleMediaType": "JPG",
    "senCoordId": 4,
    "senCoordX": 469,
    "senCoordY": 111,
    "senCoordWidth": 128,
    "senCoordHeight": 128,
    "senCordType": "Circle",
    "s3image": "https://fsn1.your-objectstorage.com/tecdoc2025/media_files/images/10/ddf4b23512565626c8b165860fd546a71904f999.webp"
  },
  {
    "articleId": 1014216,
    "articleNo": "111.104",
    "supplierId": 10,
    "supplierName": "ELRING",
    "articleMediaFileName": "ddf4b23512565626c8b165860fd546a71904f999.webp",
    "articleMediaType": "JPG",
    "senCoordId": 5,
    "senCoordX": 532,
    "senCoordY": 206,
    "senCoordWidth": 98,
    "senCoordHeight": 98,
    "senCordType": "Circle",
    "s3image": "https://fsn1.your-objectstorage.com/tecdoc2025/media_files/images/10/ddf4b23512565626c8b165860fd546a71904f999.webp"
  }
]
```

### Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `[].articleId` | integer | TecDoc internal article ID of this part on the diagram — **note:** the input `articleId` may not appear in the response; the response contains all articles plotted on the same diagram |
| `[].articleNo` | string | Supplier part number (e.g., `"862.562"`) |
| `[].supplierId` | integer | TecDoc internal supplier ID |
| `[].supplierName` | string | Supplier brand name (e.g., `"ELRING"`) |
| `[].articleMediaFileName` | string | Filename of the parts diagram image — **same value on every item in the response** since all parts share one diagram image |
| `[].articleMediaType` | string | Declared image format (e.g., `"JPG"`) — actual file served is `.webp` regardless of declared type (consistent with [#41](#41-get-article-list-by-vehicle-id--category-id)) |
| `[].senCoordId` | integer | Unique identifier for this hotspot entry — **not guaranteed to be sequential or start at 1** (observed: 1, 3, 4, 5, 6) |
| `[].senCoordX` | integer | X pixel coordinate of the hotspot bounding box on the diagram image |
| `[].senCoordY` | integer | Y pixel coordinate of the hotspot bounding box on the diagram image |
| `[].senCoordWidth` | integer | Width of the hotspot bounding box in pixels |
| `[].senCoordHeight` | integer | Height of the hotspot bounding box in pixels |
| `[].senCordType` | string | Shape of the hotspot — `"Circle"` observed; **field name has a typo**: `senCordType` (missing `o`) vs all other fields which use `senCoord...` |
| `[].s3image` | string | Full S3 URL to the diagram image — format: `https://fsn1.your-objectstorage.com/tecdoc2025/media_files/images/{supplierId}/{articleMediaFileName}` |

### Hotspot Coordinates

Each item defines a circular hotspot on the diagram image indicating where that part is located:

| Field | Meaning | Sample values |
|-------|---------|---------------|
| `senCoordX` | Left edge of bounding box (pixels) | 155, 243, 469, 503, 532 |
| `senCoordY` | Top edge of bounding box (pixels) | 86, 111, 206, 239, 304 |
| `senCoordWidth` | Bounding box width = circle diameter (pixels) | 98, 126, 128, 158, 188 |
| `senCoordHeight` | Bounding box height = circle diameter (pixels) | Equal to `senCoordWidth` for circles |
| `senCordType` | Hotspot shape | `"Circle"` |

To render a circle hotspot on the image:
- **Centre X** = `senCoordX + senCoordWidth / 2`
- **Centre Y** = `senCoordY + senCoordHeight / 2`
- **Radius** = `senCoordWidth / 2`

### Diagram Image

All 5 items in this response share the same diagram image:

```
articleMediaFileName: ddf4b23512565626c8b165860fd546a71904f999.webp
s3image: https://fsn1.your-objectstorage.com/tecdoc2025/media_files/images/10/ddf4b23512565626c8b165860fd546a71904f999.webp
```

The filename is a SHA-1 content hash (consistent with other image endpoints). `supplierId: 10` = ELRING appears in the S3 path.

### `senCoordId` Ordering

Items are **not sorted by `senCoordId`**. In this response:

| Array index | `senCoordId` |
|-------------|-------------|
| 0 | 6 |
| 1 | 1 |
| 2 | 3 |
| 3 | 4 |
| 4 | 5 |

`senCoordId: 2` is absent — IDs may be non-contiguous (some entries may have been filtered or removed from the diagram). Do not rely on array order or ID contiguity.

### Notes

- The input `articleId` (`124926`) does **not** appear in the response — the endpoint finds which diagram the input article belongs to and returns all articles on that diagram; the input article may itself be absent from the result set
- All articles in a single response share the same `articleMediaFileName` and `s3image` — this is the parts diagram image on which all returned articles are plotted
- `articleMediaType: "JPG"` but the actual file served (and the filename) is `.webp` — consistent with the `articleMediaType` behaviour documented in [#41](#41-get-article-list-by-vehicle-id--category-id)
- `senCordType` is a **typo in the API field name** — all other coordinate fields are prefixed `senCoord`, but the type field drops the `o`: `senCordType` not `senCoordType`; handle this in client code with the exact misspelled key
- `senCoordWidth` always equals `senCoordHeight` for `"Circle"` type hotspots — the bounding box is always square, and the radius is half the width
- Articles with no associated parts diagram return an empty array `[]` or a 2-byte response — not all articles have diagram data; this endpoint is most useful for articles from suppliers that provide exploded parts diagram content (e.g., ELRING gasket sets)

---

## 47. GET List of Parts for Article ID

**Method:** GET
**Status:** 200 OK
**Response Time:** 1066 ms
**Date:** 2026-04-11T11:02:26.822Z
**Response Body Size:** 2 Bytes *(RapidAPI dashboard artefact — actual payload is substantially larger)*
**URL:** `https://tecdoc-catalog.p.rapidapi.com/articles/list-of-parts-for-article/article-id/{article_id}/lang-id/{lang_id}/country-filter-id/{country_filter_id}`

### Overview

Returns the **sub-component parts list** for a given article — i.e., the individual parts that make up an assembly or repair kit. For example, a starter motor (`articleId: 344`) returns its constituent parts: bushes, engagement lever, armature, carbon brush holder, freewheel gear, and solenoid switch.

This endpoint is the **data companion to [#46 GET Parts Diagram Coordinates](#46-get-parts-diagram-coordinates)**:
- #47 provides the **parts list** (what parts exist and in what quantities)
- #46 provides the **diagram coordinates** (where each part appears on the exploded view image)

Together they power an interactive exploded-parts-diagram UI.

### Parameters

| Parameter | Location | Type | Required | Description |
|-----------|----------|------|----------|-------------|
| `article_id` | path | integer | Yes | TecDoc internal article ID of the assembly/main part (e.g., `344`) |
| `lang_id` | path | integer | Yes | Language ID for localised product names — `4` = English |
| `country_filter_id` | path | integer | Yes | Country filter ID for market-specific availability — `63` = United Kingdom |

### Response Sample

```json
{
  "countArticles": 7,
  "articles": [
    {
      "articleNo": "1 000 301 056",
      "articleStatus": "no longer deliverable by the manufacturer",
      "articleProductName": "Bush, starter shaft",
      "articleCriteria": null,
      "quantity": 1,
      "orderInList": 1
    },
    {
      "articleNo": "1 000 301 106",
      "articleStatus": "Normal",
      "articleProductName": "Bush, starter shaft",
      "articleCriteria": null,
      "quantity": 2,
      "orderInList": 2
    },
    {
      "articleNo": "1 001 933 111",
      "articleStatus": "Normal",
      "articleProductName": "Engagement Lever, starter",
      "articleCriteria": null,
      "quantity": 1,
      "orderInList": 3
    },
    {
      "articleNo": "1 004 011 085",
      "articleStatus": "no longer deliverable by the manufacturer",
      "articleProductName": "Armature, starter",
      "articleCriteria": null,
      "quantity": 1,
      "orderInList": 4
    },
    {
      "articleNo": "1 004 336 567",
      "articleStatus": "Normal",
      "articleProductName": "Holder, carbon brushes",
      "articleCriteria": null,
      "quantity": 1,
      "orderInList": 5
    },
    {
      "articleNo": "1 006 209 789",
      "articleStatus": "on demand",
      "articleProductName": "Freewheel Gear, starter",
      "articleCriteria": null,
      "quantity": 1,
      "orderInList": 6
    },
    {
      "articleNo": "2 339 305 325",
      "articleStatus": "no longer deliverable by the manufacturer",
      "articleProductName": "Solenoid Switch, starter",
      "articleCriteria": null,
      "quantity": 1,
      "orderInList": 7
    }
  ]
}
```

### Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `countArticles` | integer | Total number of sub-component parts in the list |
| `articles` | array | Ordered list of sub-components — sorted by `orderInList` ascending |
| `articles[].articleNo` | string | Supplier part number for this sub-component (e.g., `"1 000 301 056"`) — **no `articleId` returned**; use [#19 GET Search Articles by Article No](#19-get-search-articles-by-article-no) to resolve to an `articleId` if needed |
| `articles[].articleStatus` | string | Availability status of the sub-component — see status table below |
| `articles[].articleProductName` | string | Product category name of the sub-component (language determined by `lang_id`) |
| `articles[].articleCriteria` | string \| null | Fitment criteria string — `null` in this response; may be populated for other articles |
| `articles[].quantity` | integer | Number of this part required in the assembly (e.g., `2` for dual bushes) |
| `articles[].orderInList` | integer | Display order in the parts list — sequential, starting at `1` |

### `articleStatus` Values

| Value | Meaning |
|-------|---------|
| `"Normal"` | Part is available and orderable |
| `"no longer deliverable by the manufacturer"` | Discontinued — manufacturer no longer supplies this part |
| `"on demand"` | Available but requires special order |

### `orderInList` vs Array Index

`orderInList` is always sequential (1, 2, 3 … N) and matches the array index + 1 in this response. However, always use `orderInList` for display ordering rather than relying on array position, as ordering could differ in edge cases.

### Parts Diagram — #46 + #47 Workflow

| Step | Endpoint | Action |
|------|----------|--------|
| 1 | [#47 this endpoint](#47-get-list-of-parts-for-article-id) | Get the ordered parts list — `articleNo`, `quantity`, `articleProductName` for each sub-component |
| 2 | [#46 GET Parts Diagram Coordinates](#46-get-parts-diagram-coordinates) | Get the diagram image URL and hotspot coordinates for each part |
| 3 | Render | Display the diagram image with circular hotspots; each hotspot links to the matching part in the #47 list |
| 4 | [#19 GET Search Articles by Article No](#19-get-search-articles-by-article-no) | Optionally resolve `articleNo` → `articleId` to fetch full part details |

### Notes

- Response items only contain `articleNo` — there is no `articleId`, `supplierId`, or `supplierName` in this endpoint's output; to get full article details, resolve via [#19](#19-get-search-articles-by-article-no)
- `articleCriteria: null` observed on all items in this response — may be populated for assemblies where sub-components have fitment restrictions
- `quantity` can exceed 1 — e.g., some assemblies require 2 of the same bush; always use this field when building a parts ordering UI
- `lang_id` controls the language of `articleProductName` — use `4` for English
- `country_filter_id` affects availability filtering — parts marked `"no longer deliverable"` or `"on demand"` may vary by market
- Part numbers in this response follow OEM/manufacturer numbering (e.g., Bosch-style `"1 000 301 056"`) — these are original equipment part numbers, not aftermarket catalogue numbers
- The "RapidAPI Response Body Size: 2 Bytes" is a known dashboard measurement artefact — actual payload is substantially larger

---

## 48. GET Article Media

**Method:** GET
**Status:** 200 OK
**Response Time:** 1021 ms
**Date:** 2026-04-11T11:04:01.465Z
**Response Body Size:** 2 Bytes *(RapidAPI dashboard artefact)*
**URL:** `https://tecdoc-catalog.p.rapidapi.com/articles/article-all-media-info?articleId={articleId}&langId={langId}`

### Overview

Returns all media assets associated with a specific article — images, technical drawings, PDFs, etc. Unlike the embedded `articleMediaFileName` fields returned inline by other endpoints (e.g., [#35](#35-get-article-details-by-article-id), [#41](#41-get-article-list-by-vehicle-id--category-id)), this endpoint is dedicated to media and returns the complete set of media items for the article, each with a `mediaInformation` label describing the media type.

### Parameters

| Parameter | Location | Type | Required | Description |
|-----------|----------|------|----------|-------------|
| `articleId` | query | integer | Yes | TecDoc internal article ID (e.g., `125`) |
| `langId` | query | integer | Yes | Language ID — affects `mediaInformation` label localisation; `4` = English |

### Response Sample

```json
[
  {
    "articleMediaType": "JPEG",
    "articleMediaFileName": "42a582934b5b5a50ee74236c088af79c7300d1f9.webp",
    "supplierId": 30,
    "mediaInformation": "Picture",
    "s3image": "https://fsn1.your-objectstorage.com/tecdoc2025/media_files/images/30/42a582934b5b5a50ee74236c088af79c7300d1f9.webp"
  },
  {
    "articleMediaType": "JPEG",
    "articleMediaFileName": "9b7ea545dfe75fd8d597282ff4a4ca62ae78e09f.webp",
    "supplierId": 30,
    "mediaInformation": "Picture",
    "s3image": "https://fsn1.your-objectstorage.com/tecdoc2025/media_files/images/30/9b7ea545dfe75fd8d597282ff4a4ca62ae78e09f.webp"
  },
  {
    "articleMediaType": "JPG",
    "articleMediaFileName": "3ab47e1a20d207c2c6e954f0cf84d1de0403c914.webp",
    "supplierId": 30,
    "mediaInformation": "Picture",
    "s3image": "https://fsn1.your-objectstorage.com/tecdoc2025/media_files/images/30/3ab47e1a20d207c2c6e954f0cf84d1de0403c914.webp"
  },
  {
    "articleMediaType": "JPEG",
    "articleMediaFileName": "15b81d979b16ab523adfbfcae5edcfe258b62fdc.webp",
    "supplierId": 30,
    "mediaInformation": "Picture",
    "s3image": "https://fsn1.your-objectstorage.com/tecdoc2025/media_files/images/30/15b81d979b16ab523adfbfcae5edcfe258b62fdc.webp"
  }
]
```

### Response Fields

The response is a **raw JSON array** — no wrapping object, no count field.

| Field | Type | Description |
|-------|------|-------------|
| `[].articleMediaType` | string | Declared media format — e.g., `"JPEG"`, `"JPG"` — see type table below |
| `[].articleMediaFileName` | string | SHA-1 content-addressed filename with `.webp` extension — unique per media asset |
| `[].supplierId` | integer | TecDoc supplier ID who provided this media asset |
| `[].mediaInformation` | string | Describes what the media shows — e.g., `"Picture"`, potentially `"Technical Drawing"`, `"PDF"` for other articles |
| `[].s3image` | string | Full S3 URL: `https://fsn1.your-objectstorage.com/tecdoc2025/media_files/images/{supplierId}/{articleMediaFileName}` |

### `articleMediaType` Behaviour

Both `"JPEG"` and `"JPG"` appear in the same response. All serve `.webp` files regardless of declared type — consistent with the pattern documented across all media-bearing endpoints:

| Declared `articleMediaType` | Actual file served | Extension in filename |
|-----------------------------|--------------------|-----------------------|
| `"JPEG"` | WebP | `.webp` |
| `"JPG"` | WebP | `.webp` |
| `"PNG"` | WebP | `.webp` |
| `"BMP"` | WebP | `.webp` |
| `"GIF"` | GIF | `.gif` |

### Comparison: #48 vs Inline Media Fields

Other endpoints return media inline as part of article data. This endpoint is dedicated to media and returns the full set:

| Aspect | Inline media (e.g., [#35](#35-get-article-details-by-article-id), [#41](#41-get-article-list-by-vehicle-id--category-id)) | #48 GET Article Media |
|--------|-----------------------------------------------------------|----------------------|
| Fields returned | `articleMediaType`, `articleMediaFileName` only | + `supplierId`, `mediaInformation`, `s3image` |
| Number of media items | Typically one per article | All media items (multiple images, drawings, etc.) |
| `s3image` pre-built | Sometimes (e.g., #41) | Always |
| `mediaInformation` label | Not present | Present — describes media purpose |
| Response shape | Embedded in article object | Standalone raw array |
| Parameters | Varies by endpoint | `articleId` + `langId` query params |

### Notes

- Response is a raw JSON array — no wrapping object; array length is the total media count for the article
- Both `"JPEG"` and `"JPG"` can appear in the same response for the same article — treat them identically; both serve `.webp` files
- `mediaInformation: "Picture"` observed for all items in this response — other values likely include `"Technical Drawing"`, `"360° View"`, `"PDF Document"` for articles with richer media content
- `langId` may affect the `mediaInformation` label language (e.g., `"Picture"` in English vs localised equivalent) — confirm with other `langId` values if needed
- `supplierId` in the S3 URL path matches the `supplierId` field — the media asset is stored under the supplying brand's folder
- All filenames are SHA-1 content hashes — identical images across different suppliers will share the same filename (consistent with [#41](#41-get-article-list-by-vehicle-id--category-id) notes)
- Articles with no media return an empty array `[]`

---

## 49. POST Article Media

**Method:** POST
**Status:** 200 OK
**Response Time:** 699 ms
**Date:** 2026-04-11T11:10:12.455Z
**Response Body Size:** 2 Bytes *(RapidAPI dashboard artefact)*
**URL:** `https://tecdoc-catalog.p.rapidapi.com/articles/article-all-media-info`

### Overview

POST equivalent of [#48 GET Article Media](#48-get-article-media). Accepts the same parameters as a JSON request body instead of query string. Response is identical.

### Request Body

```json
{
  "articleId": 125,
  "langId": 4
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `articleId` | integer | Yes | TecDoc internal article ID |
| `langId` | integer | Yes | Language ID — `4` = English |

### Response

Identical to [#48 GET Article Media](#48-get-article-media) — raw array of media items with `articleMediaType`, `articleMediaFileName`, `supplierId`, `mediaInformation`, and `s3image`. See #48 for full field documentation.

### GET vs POST Comparison

| Aspect | [#48 GET](#48-get-article-media) | #49 POST |
|--------|----------------------------------|----------|
| Method | GET | POST |
| Parameters | Query string (`?articleId=&langId=`) | JSON request body |
| URL | `.../article-all-media-info?articleId=125&langId=4` | `.../article-all-media-info` |
| Response | Identical | Identical |
| Response time | 1021 ms | 699 ms |

---

## 50. GET Cross-References by Article ID

<!-- TODO: confirm URL from RapidAPI dashboard -->

**Method:** GET
**Status:** 200 OK
**Response Time:** (confirm from RapidAPI dashboard)
**Section:** Parts Cross Reference

### Overview

Given an article ID, returns all **cross-reference articles** — equivalent or interchangeable parts from other suppliers that cover the same function. This is the supplier-diversity lookup: if you have a LÖBRO drive shaft, this endpoint finds the same part sold under METELLI, CIFAM, GSP, NK, RIDEX, and 24 other brands.

All results share the same `articleProductName` (e.g., `"Drive Shaft"`) confirming they are functionally equivalent. Each result is a distinct catalogue entry with its own `articleId`, `articleNo`, `supplierId`, and image.

### Parameters

| Parameter | Location | Type | Required | Description |
|-----------|----------|------|----------|-------------|
| `article_id` | path | integer | Yes | TecDoc internal article ID to find cross-references for |
| (additional params) | — | — | — | Confirm full URL and any query params from RapidAPI dashboard |

### Response Sample

```json
{
  "countArticles": 29,
  "articles": [
    {
      "articleId": 2558558,
      "articleNo": "300641",
      "supplierName": "LÖBRO",
      "supplierId": 56,
      "articleProductName": "Drive Shaft",
      "articleMediaType": "JPEG",
      "articleMediaFileName": "d8ae6f3cbdbc29f2b8e668a6261a18d9634242bc.webp",
      "s3image": "https://fsn1.your-objectstorage.com/tecdoc2025/media_files/images/56/d8ae6f3cbdbc29f2b8e668a6261a18d9634242bc.webp"
    },
    {
      "articleId": null,
      "articleNo": "T454",
      "supplierName": "SPIDAN",
      "supplierId": 1,
      "articleProductName": "Drive Shaft",
      "articleMediaType": "JPEG",
      "articleMediaFileName": "d8ae6f3cbdbc29f2b8e668a6261a18d9634242bc.webp",
      "s3image": "https://fsn1.your-objectstorage.com/tecdoc2025/media_files/images/1/d8ae6f3cbdbc29f2b8e668a6261a18d9634242bc.webp"
    },
    {
      "articleId": 2771488,
      "articleNo": "33-2326",
      "supplierName": "IPD",
      "supplierId": 262,
      "articleProductName": "Drive Shaft",
      "articleMediaType": null,
      "articleMediaFileName": null,
      "s3image": null
    }
  ]
}
```

### Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `countArticles` | integer | Total number of cross-reference articles found |
| `articles` | array | All equivalent articles across all suppliers |
| `articles[].articleId` | integer \| **null** | TecDoc internal article ID — **`null` if the cross-reference is known but not assigned an ID in TecDoc** |
| `articles[].articleNo` | string | Supplier-specific part number for this equivalent part |
| `articles[].supplierName` | string | Supplier/brand name |
| `articles[].supplierId` | integer | TecDoc internal supplier ID |
| `articles[].articleProductName` | string | Product category — same value for all items (confirms functional equivalence) |
| `articles[].articleMediaType` | string \| null | Declared image format (`"JPEG"`, `"JPG"`, `"BMP"`) — or `null` if no image available |
| `articles[].articleMediaFileName` | string \| null | SHA-1 image filename (`.webp`) — or `null` if no image |
| `articles[].s3image` | string \| null | Full S3 image URL — or `null` if no image |

### Notable Data Patterns

**`articleId: null`**

One article (SPIDAN `T454`) has `articleId: null`. This means the cross-reference exists in TecDoc's reference data but has not been assigned a TecDoc article ID — it cannot be used with article-based endpoints (#35, #39, #46, #47, etc.). Always null-check `articleId` before using it downstream.

**Null media fields**

Two articles (IPD `33-2326`, POINT GEAR `PNG70094`) have `articleMediaType: null`, `articleMediaFileName: null`, `s3image: null` — no image is available for these cross-references. Always null-check media fields before rendering.

**Same `articleNo`, different suppliers**

LPR and SAMKO both list `articleNo: "DS60097"` with different `articleId` values (`6662742` and `6662743`). The same part number string can be used by multiple suppliers — always use `supplierId` alongside `articleNo` to uniquely identify an article.

**Shared image across suppliers**

METELLI (`supplierId: 121`) and CIFAM (`supplierId: 311`) share the same `articleMediaFileName` (`226b2ed2058ebc1dd700223a79ca7164dd51ccdd.webp`) despite being different suppliers — consistent with the SHA-1 content-addressed image system documented in [#41](#41-get-article-list-by-vehicle-id--category-id).

**`articleMediaType: "BMP"` → `.webp`**

Two articles declare `"BMP"` but serve `.webp` files — consistent with the `articleMediaType` behaviour documented across all media-bearing endpoints.

### Cross-Reference vs Other Article Lookup Endpoints

| Aspect | [#19 Search by Article No](#19-get-search-articles-by-article-no) | #50 Cross-References by Article ID |
|--------|------------------------------------------------------------------|-------------------------------------|
| Input | Part number string | `articleId` |
| Output | Articles matching that specific part number | All equivalent parts across all suppliers |
| Use case | Find a known part | Discover alternatives/substitutes for a known part |
| `articleId: null` possible | No | Yes |
| `countArticles` meaning | Matches for the search term | Total cross-reference equivalents |

### Notes

- Always null-check `articleId` before using a cross-reference article in downstream endpoints — some cross-references have no TecDoc ID
- Always null-check `articleMediaType`, `articleMediaFileName`, and `s3image` — not all cross-reference articles have images
- `articleProductName` is identical across all results (e.g., all `"Drive Shaft"`) — this confirms functional equivalence between cross-references
- The same `articleNo` can appear from multiple suppliers — use `supplierId + articleNo` as the unique key, not `articleNo` alone
- The input article itself may or may not appear in the results — do not assume the source article is included
- The "RapidAPI Response Body Size: 2 Bytes" is a known dashboard measurement artefact

---

## 51. GET Equivalent OEM Numbers

**Method:** GET
**Status:** 200 OK
**Response Time:** 1342 ms
**Date:** 2026-04-11T11:16:35.647Z
**Response Body Size:** 2 Bytes *(RapidAPI dashboard artefact)*
**URL:** `https://tecdoc-catalog.p.rapidapi.com/articles-oem/search-all-equal-oem-no/lang-id/{lang_id}/article-oem-no/{article_oem_no}`

### Overview

Given an OEM part number string, returns all aftermarket articles that cross-reference to that OEM number, along with every OEM number each article covers. This is the **OEM-to-aftermarket** lookup: input a manufacturer's part number and discover every aftermarket supplier whose part claims equivalence to it.

The inverse of [#26 POST Get OEM by Article ID](#26-post-get-oem-by-article-id) (which goes article → OEM numbers). This endpoint goes OEM number → articles.

### Parameters

| Parameter | Location | Type | Required | Description |
|-----------|----------|------|----------|-------------|
| `lang_id` | path | integer | Yes | Language ID — `4` = English |
| `article_oem_no` | path | string | Yes | OEM part number to search (e.g., `517501D000`) — URL-encode if it contains special characters |

### Response Sample

```json
[
  {
    "articleId": 412619,
    "articleSearchNo": "517501D000",
    "articleNo": "04-P432",
    "oemNo": [
      { "oemBrand": "HYUNDAI", "oemDisplayNo": "517501D000" },
      { "oemBrand": "KIA",     "oemDisplayNo": "517501D000" },
      { "oemBrand": "HYUNDAI", "oemDisplayNo": "5175039600" },
      { "oemBrand": "KIA",     "oemDisplayNo": "5175039600" }
    ]
  },
  {
    "articleId": 8652983,
    "articleSearchNo": "517501D000",
    "articleNo": "PW51001",
    "oemNo": [
      { "oemBrand": "HYUNDAI", "oemDisplayNo": "517501D000" },
      { "oemBrand": "FORD",    "oemDisplayNo": "1146119" },
      { "oemBrand": "MAZDA",   "oemDisplayNo": "BP4K33062" }
    ]
  },
  {
    "articleId": 1219246,
    "articleSearchNo": "51750-1D000",
    "articleNo": "1282-011",
    "oemNo": [
      { "oemBrand": "HYUNDAI", "oemDisplayNo": "51750-1D000" },
      { "oemBrand": "HYUNDAI", "oemDisplayNo": "51750-39603" }
    ]
  }
]
```

### Response Fields

The response is a **raw JSON array** — no wrapping object, no `countArticles` field.

| Field | Type | Description |
|-------|------|-------------|
| `[].articleId` | integer | TecDoc internal article ID of the aftermarket part |
| `[].articleSearchNo` | string | The OEM number variant that caused this row to match — may differ in formatting from the input (see hyphen variants below) |
| `[].articleNo` | string | Aftermarket supplier part number |
| `[].oemNo` | array | All OEM numbers this aftermarket article covers across all manufacturers |
| `[].oemNo[].oemBrand` | string | OEM manufacturer brand (e.g., `"HYUNDAI"`, `"KIA"`, `"FORD"`, `"MAZDA"`, `"GENERAL MOTORS"`) |
| `[].oemNo[].oemDisplayNo` | string | OEM part number as displayed by that manufacturer |

### Duplicate Rows — Expected Behaviour

**The same `articleId + articleNo` can appear multiple times in a single response.** In this response, `articleId: 412619` (`"04-P432"`) appears 13+ times. This is not a data error — it is how the API works:

Each row corresponds to one **OEM number variant match**. The same article may be indexed under both `"517501D000"` and `"51750-1D000"` (hyphenated vs non-hyphenated forms of the same number). The API returns one row per matching variant, causing duplicates.

**Deduplication strategy:** Group or deduplicate by `articleId` before displaying results. The `oemNo` array is identical across duplicate rows for the same `articleId`.

### OEM Number Format Variants

The input `517501D000` matched two distinct `articleSearchNo` formats in the response:

| Format | Example | Notes |
|--------|---------|-------|
| No hyphens | `"517501D000"` | Compact format |
| With hyphens | `"51750-1D000"` | Hyphenated format — same number, different notation |

Both represent the same HYUNDAI/KIA part number. The API indexes articles under both formats and returns rows for all matches, which is the primary cause of duplication.

### `oemNo` Coverage Varies by Article

Different aftermarket articles cover different sets of OEM numbers:

| `articleNo` | OEM brands covered | Approx. OEM count |
|-------------|-------------------|-------------------|
| `"PW51001"` | HYUNDAI, KIA, FORD, MAZDA, GENERAL MOTORS | 90+ |
| `"HY-WB-11795"` | HYUNDAI, KIA | ~23 |
| `"04-P432"` | HYUNDAI, KIA | 8 |
| `"971510"` | KIA, HYUNDAI | 3 |

### Comparison: #51 vs Related OEM Endpoints

| Aspect | [#26 POST Get OEM by Article ID](#26-post-get-oem-by-article-id) | [#20 GET Search by OEM No](#20-get-search-articles-by-oem-no) | #51 GET Equivalent OEM Numbers |
|--------|------------------------------------------------------------------|--------------------------------------------------------------|-------------------------------|
| Input | `articleId` | OEM number | OEM number |
| Output | OEM numbers for that article | Articles matching OEM | Articles + full OEM networks |
| `oemNo` array | Yes | No | Yes — full OEM coverage per article |
| Direction | Article → OEM | OEM → Articles | OEM → Articles + OEM networks |
| Duplicates | No | No | Yes — one row per OEM variant |
| Response shape | Object with `articles[]` | Confirm from #20 docs | Raw array |

### Notes

- Response is a raw array — no `countArticles` wrapper; deduplicate by `articleId` to get the true distinct article count
- The same `articleId` appears multiple times — once per matching OEM format variant; this is by design
- `articleSearchNo` shows which OEM format variant triggered each row — useful for understanding duplication
- `oemNo` arrays are identical across duplicate rows for the same `articleId` — safe to use the first occurrence
- OEM numbers in `oemDisplayNo` may use hyphenated or compact notation even within the same `oemNo` array — treat as the same number when matching
- `oemBrand` values are manufacturer names as stored in TecDoc (e.g., `"GENERAL MOTORS"`, not `"GM"`)
- The URL path uses `/articles-oem/` prefix — different from all other endpoints which use `/articles/`
- The "RapidAPI Response Body Size: 2 Bytes" is a known dashboard measurement artefact

---

## 52. GET Parts Cross-Reference by Article No

<!-- TODO: confirm URL from RapidAPI dashboard -->

**Method:** GET
**Status:** 200 OK
**Response Time:** (confirm from RapidAPI dashboard)
**Section:** Parts Cross Reference

### Overview

Given a supplier article number (e.g., `"111455"`), returns all TecDoc catalogue articles whose cross-reference index includes that number — across all suppliers and product categories. This is a **broad number lookup**: the same numeric string `"111455"` can appear as a part number for completely unrelated products (Starter, Alternator, Brake Shoe Set, Radiator, Window Regulator, Steering Gear) from dozens of different suppliers.

Unlike [#50 Cross-References by Article ID](#50-get-cross-references-by-article-id) (which finds functional equivalents for one specific part), this endpoint finds every article associated with a given number string regardless of functional category. Results include both image media and **PDF documents**.

### Parameters

| Parameter | Location | Type | Required | Description |
|-----------|----------|------|----------|-------------|
| (article number) | path or query | string | Yes | Article number string to search cross-references for (e.g., `111455`) — confirm full URL from RapidAPI dashboard |
| (additional params) | — | — | — | Confirm full URL and any additional params from RapidAPI dashboard |

### Response Sample

```json
{
  "countArticles": 262,
  "articles": [
    {
      "articleSearchNo": "111455",
      "articleId": 2536234,
      "articleNo": "190.518.092.050",
      "articleProductName": "Starter",
      "supplierName": "BV PSH",
      "supplierId": 28,
      "articleMediaType": "JPEG",
      "articleMediaFileName": "7e2ca1e498a72dace76faf1d1deb6c6b7ebe12f3.webp",
      "s3image": "https://fsn1.your-objectstorage.com/tecdoc2025/media_files/images/28/7e2ca1e498a72dace76faf1d1deb6c6b7ebe12f3.webp"
    },
    {
      "articleSearchNo": "1.11455",
      "articleId": 2536234,
      "articleNo": "190.518.092.050",
      "articleProductName": "Starter",
      "supplierName": "BV PSH",
      "supplierId": 28,
      "articleMediaType": "PDF",
      "articleMediaFileName": "7e2ca1e498a72dace76faf1d1deb6c6b7ebe12f3.pdf",
      "s3image": "https://fsn1.your-objectstorage.com/tecdoc2025/media_files/PDF/28/7e2ca1e498a72dace76faf1d1deb6c6b7ebe12f3.pdf"
    },
    {
      "articleSearchNo": "11.1455",
      "articleId": 2536234,
      "articleNo": "190.518.092.050",
      "articleProductName": "Starter",
      "supplierName": "BV PSH",
      "supplierId": 28,
      "articleMediaType": "JPEG",
      "articleMediaFileName": "7e2ca1e498a72dace76faf1d1deb6c6b7ebe12f3.webp",
      "s3image": "https://fsn1.your-objectstorage.com/tecdoc2025/media_files/images/28/7e2ca1e498a72dace76faf1d1deb6c6b7ebe12f3.webp"
    },
    {
      "articleSearchNo": "11-1455",
      "articleId": 2536234,
      "articleNo": "190.518.092.050",
      "articleProductName": "Starter",
      "supplierName": "BV PSH",
      "supplierId": 28,
      "articleMediaType": "JPEG",
      "articleMediaFileName": "7e2ca1e498a72dace76faf1d1deb6c6b7ebe12f3.webp",
      "s3image": "https://fsn1.your-objectstorage.com/tecdoc2025/media_files/images/28/7e2ca1e498a72dace76faf1d1deb6c6b7ebe12f3.webp"
    },
    {
      "articleSearchNo": "111455",
      "articleId": 10440539,
      "articleNo": "10440539",
      "articleProductName": "Alternator",
      "supplierName": "ALANKO",
      "supplierId": 1161,
      "articleMediaType": null,
      "articleMediaFileName": null,
      "s3image": null
    },
    {
      "articleSearchNo": "111455",
      "articleId": 438437,
      "articleNo": "438437",
      "articleProductName": "Alternator",
      "supplierName": "VALEO",
      "supplierId": 50,
      "articleMediaType": null,
      "articleMediaFileName": null,
      "s3image": null
    }
  ]
}
```

### Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `countArticles` | integer | Total number of result rows (includes duplicates from multiple media files and format variants — not distinct articles) |
| `articles` | array | All cross-reference results |
| `articles[].articleSearchNo` | string | The format variant of the input number that matched this row (see format variants below) |
| `articles[].articleId` | integer | TecDoc internal article ID |
| `articles[].articleNo` | string | Supplier-specific part number |
| `articles[].articleProductName` | string | Product category of this article — **varies across results** (different product types can share the same number) |
| `articles[].supplierName` | string | Supplier/brand name |
| `articles[].supplierId` | integer | TecDoc internal supplier ID |
| `articles[].articleMediaType` | string \| null | Declared media format — `"JPEG"`, `"JPG"`, `"BMP"`, `"PNG"`, `"GIF"`, **`"PDF"`** — or `null` if no media |
| `articles[].articleMediaFileName` | string \| null | SHA-1 content-addressed filename with extension (`.webp`, `.gif`, or `.pdf`) — or `null` if no media |
| `articles[].s3image` | string \| null | Full S3 URL to the media file — or `null` if no media |

### PDF Media Type — NEW S3 Path Pattern

This endpoint is the first to return `articleMediaType: "PDF"`. PDF files use a **different S3 path** from image files:

| Media category | `articleMediaType` | S3 URL pattern |
|----------------|--------------------|----------------|
| Images | `"JPEG"`, `"JPG"`, `"BMP"`, `"PNG"` | `media_files/images/{supplierId}/{filename}.webp` |
| Animated | `"GIF"` | `media_files/images/{supplierId}/{filename}.gif` |
| Documents | **`"PDF"`** | **`media_files/PDF/{supplierId}/{filename}.pdf`** |

The `s3image` field name is misleading when the media type is PDF — it is a URL to a `.pdf` file, not an image. When `articleMediaType == "PDF"`, treat `s3image` as a document URL and render/download it as a PDF rather than displaying it as an image.

**Note:** The SHA-1 filename is the same for all media belonging to the same content (e.g., `7e2ca1e498a72dace76faf1d1deb6c6b7ebe12f3` appears as both `.webp` and `.pdf` for the same article — they are content-addressed separately).

### `articleSearchNo` Format Variants

The input number string is indexed under multiple normalised formats. For input `111455`, four variants are present:

| `articleSearchNo` | Format | Notes |
|-------------------|--------|-------|
| `"111455"` | Compact — no separators | Base form |
| `"1.11455"` | Dot after first digit | |
| `"11.1455"` | Dot after second digit | |
| `"11-1455"` | Hyphen after second digit | |

Each variant generates its own set of rows. An article with 3 media files will appear 3 × 4 = 12 times if all four format variants are indexed. Always deduplicate by `articleId + articleMediaFileName` to enumerate distinct media files, or by `articleId` alone for distinct articles.

### Duplicate Row Sources

Rows are multiplied by two independent factors:

| Source | Multiplier | Example |
|--------|-----------|---------|
| `articleSearchNo` format variants | ×4 (for `111455`) | Same article appears under `"111455"`, `"1.11455"`, `"11.1455"`, `"11-1455"` |
| Media files per article | ×N (1 per file) | One article with 5 PDF rows — same `articleId`, same `articleMediaFileName`, repeated 5 times |

These factors compound: an article with 2 media files indexed under 4 number variants = 8 rows for that single article.

**Exact duplicate rows** (identical `articleId + articleMediaFileName`) are also possible — observed with `articleId: 20432611BN` appearing 5 times with the same filename. Always deduplicate before display.

### Mixed Product Categories

Unlike [#50](#50-get-cross-references-by-article-id) where all results share the same `articleProductName`, this endpoint returns articles from entirely unrelated product categories because it matches on number string alone, not functional equivalence:

| `articleProductName` examples in a single response |
|-----------------------------------------------------|
| Starter |
| Alternator |
| Radiator |
| Brake Shoe Set |
| Window Regulator |
| Steering Gear |

Do **not** assume results are functionally equivalent to each other. Group by `articleProductName` if displaying in a UI to avoid implying interchangeability.

### Same `articleNo`, Different Suppliers

`articleNo: "190.518.092.050"` appears from both BV PSH (`supplierId: 28`) and AES PSH (`supplierId: 4886`), sharing the same `articleMediaFileName`. Always use `supplierId + articleNo` as the unique supplier-article key.

### Null Media Fields

Some articles (e.g., ALANKO `10440539`, VALEO `438437`) have `articleMediaType: null`, `articleMediaFileName: null`, `s3image: null` — no media available. Always null-check media fields before rendering.

### Comparison: #52 vs Related Cross-Reference Endpoints

| Aspect | [#50 Cross-Refs by Article ID](#50-get-cross-references-by-article-id) | [#51 Equivalent OEM Numbers](#51-get-equivalent-oem-numbers) | #52 Cross-Reference by Article No |
|--------|-------------------------------------------------------------------------|--------------------------------------------------------------|-----------------------------------|
| Input | `articleId` | OEM number string | Supplier article number string |
| Output | Functionally equivalent parts | Aftermarket articles covering an OEM number | All articles whose cross-ref index contains the number |
| Same product category | Yes — all results share `articleProductName` | Yes | No — mixed categories |
| Duplicates | No | Yes — per OEM format variant | Yes — per format variant × per media file |
| Media included | Yes | No | Yes — including PDF |
| `countArticles` meaning | Distinct cross-ref articles | N/A (raw array) | Total rows (not distinct) |
| PDF media | No | No | **Yes** |
| Response shape | Wrapped object | Raw array | Wrapped object |

### Notes

- `countArticles` counts rows, not distinct articles — after deduplication the true article count will be lower
- Always deduplicate by `articleId` before counting or displaying distinct results
- When `articleMediaType == "PDF"`, the `s3image` URL points to a `.pdf` document at `media_files/PDF/{supplierId}/` — render as a download link or PDF viewer, not an `<img>` tag
- `articleProductName` varies across results — do not assume functional equivalence between results
- `articleSearchNo` format variants (`"111455"`, `"1.11455"`, `"11.1455"`, `"11-1455"`) are the primary source of row multiplication
- Exact duplicate rows (same `articleId + articleMediaFileName`) are possible — always deduplicate before display
- The "RapidAPI Response Body Size: 2 Bytes" is a known dashboard measurement artefact

---

## 53. GET Cross-References through OEM Numbers by Article ID

<!-- TODO: confirm URL from RapidAPI dashboard -->

**Method:** GET
**Status:** 200 OK
**Response Time:** (confirm from RapidAPI dashboard)
**Section:** Parts Cross Reference

### Overview

Given an article ID, returns every cross-reference traceable through OEM numbers: the direct OEM numbers the article covers, and all other aftermarket brands that cover the same OEM numbers. This builds a complete **cross-reference network** for a part — both its OEM equivalents and its IAM-to-IAM indirect equivalents.

The response is one row per `crossManufacturerName + crossNumber` pair. The input article's own data (`articleBrandRoot`, `articleNumberRoot`, `articleId`, `supplierId`, media) is repeated identically on every row.

### Parameters

| Parameter | Location | Type | Required | Description |
|-----------|----------|------|----------|-------------|
| `article_id` | path or query | integer | Yes | TecDoc internal article ID to look up (e.g., `6159438`) — confirm full URL from RapidAPI dashboard |

### Response Sample

```json
{
  "countArticles": 1492,
  "articles": [
    {
      "articleBrandRoot": "MANN-FILTER",
      "articleNumberRoot": "C 2029",
      "crossManufacturerName": "HYUNDAI (BEIJING)",
      "crossNumber": "28113-0Q000",
      "searchLevel": "IAM -> OEM",
      "articleMediaFileName": "5e27f118885fa0253374358b3585240c6c9a53af.webp",
      "articleId": 6159438,
      "supplierId": 4,
      "articleMediaType": "JPG",
      "s3image": "https://fsn1.your-objectstorage.com/tecdoc2025/media_files/images/4/5e27f118885fa0253374358b3585240c6c9a53af.webp"
    },
    {
      "articleBrandRoot": "MANN-FILTER",
      "articleNumberRoot": "C 2029",
      "crossManufacturerName": "HYUNDAI",
      "crossNumber": "28113-2H000",
      "searchLevel": "IAM -> OEM",
      "articleMediaFileName": "5e27f118885fa0253374358b3585240c6c9a53af.webp",
      "articleId": 6159438,
      "supplierId": 4,
      "articleMediaType": "JPG",
      "s3image": "https://fsn1.your-objectstorage.com/tecdoc2025/media_files/images/4/5e27f118885fa0253374358b3585240c6c9a53af.webp"
    },
    {
      "articleBrandRoot": "MANN-FILTER",
      "articleNumberRoot": "C 2029",
      "crossManufacturerName": "BOSCH",
      "crossNumber": "1 457 433 955",
      "searchLevel": "IAM -> OEM -> IAM",
      "articleMediaFileName": "5e27f118885fa0253374358b3585240c6c9a53af.webp",
      "articleId": 6159438,
      "supplierId": 4,
      "articleMediaType": "JPG",
      "s3image": "https://fsn1.your-objectstorage.com/tecdoc2025/media_files/images/4/5e27f118885fa0253374358b3585240c6c9a53af.webp"
    },
    {
      "articleBrandRoot": "MANN-FILTER",
      "articleNumberRoot": "C 2029",
      "crossManufacturerName": "MANN-FILTER",
      "crossNumber": "C 2029",
      "searchLevel": "IAM -> OEM -> IAM",
      "articleMediaFileName": "5e27f118885fa0253374358b3585240c6c9a53af.webp",
      "articleId": 6159438,
      "supplierId": 4,
      "articleMediaType": "JPG",
      "s3image": "https://fsn1.your-objectstorage.com/tecdoc2025/media_files/images/4/5e27f118885fa0253374358b3585240c6c9a53af.webp"
    }
  ]
}
```

### Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `countArticles` | integer | Total number of cross-reference rows (one per `crossManufacturerName + crossNumber` pair — not distinct manufacturers) |
| `articles` | array | All cross-reference entries |
| `articles[].articleBrandRoot` | string | Brand name of the **input article** — repeated identically on every row |
| `articles[].articleNumberRoot` | string | Part number of the **input article** — repeated identically on every row |
| `articles[].crossManufacturerName` | string | Manufacturer of this cross-reference entry (OEM brand or aftermarket brand) |
| `articles[].crossNumber` | string | Part number used by `crossManufacturerName` for this equivalent part |
| `articles[].searchLevel` | string | Relationship chain — `"IAM -> OEM"` or `"IAM -> OEM -> IAM"` (see below) |
| `articles[].articleMediaFileName` | string | SHA-1 image filename of the input article — repeated identically on every row |
| `articles[].articleId` | integer | TecDoc ID of the input article — repeated identically on every row |
| `articles[].supplierId` | integer | Supplier ID of the input article — repeated identically on every row |
| `articles[].articleMediaType` | string | Declared image format of the input article (`"JPG"`, `"JPEG"`, etc.) — repeated identically on every row |
| `articles[].s3image` | string | Full S3 image URL of the input article — repeated identically on every row |

### `searchLevel` — Relationship Chain

The `searchLevel` field explains how the cross-reference was discovered:

| `searchLevel` | Meaning | `crossManufacturerName` type |
|---------------|---------|------------------------------|
| `"IAM -> OEM"` | The input IAM article directly lists this as an OEM number | Vehicle manufacturer (HYUNDAI, KIA, BMW, etc.) |
| `"IAM -> OEM -> IAM"` | Another IAM brand also covers the same OEM number(s) as the input article — indirect cross-reference | Aftermarket brand (BOSCH, MAHLE, FILTRON, etc.) |

**Example for MANN-FILTER C 2029:**
- `"IAM -> OEM"` rows: HYUNDAI `28113-0Q000`, HYUNDAI `28113-2H000` — these are the OEM numbers the filter directly covers
- `"IAM -> OEM -> IAM"` rows: BOSCH, MAHLE, HENGST FILTER, FILTRON, MAHLE, etc. — these aftermarket brands also cover those same HYUNDAI OEM numbers

The `"IAM -> OEM -> IAM"` chain means: **Input IAM → shared OEM number → other IAM brands**.

### Self-Reference Row

The input article itself always appears in its own cross-reference list:

```json
{
  "crossManufacturerName": "MANN-FILTER",
  "crossNumber": "C 2029",
  "searchLevel": "IAM -> OEM -> IAM"
}
```

This is expected — the article cross-references itself via its own OEM number coverage. Do not treat this as an error; filter it out if displaying results to users.

### Multiple Cross Numbers Per Manufacturer

One manufacturer can appear multiple times with different `crossNumber` values — one row per part number:

| `crossManufacturerName` | `crossNumber` examples |
|------------------------|------------------------|
| WILMINK GROUP | `WG1216302`, `WG1378648`, `WG1747527`, `WG1792298`, `WG2284290`, `WG2282652` |
| ACKOJA | `A52-0408`, `A52-2001`, `A52-2006`, `A53-0401` |
| MASTER-SPORT GERMANY | `2029-LF-PCS-MS`, `450001192`, `450001202`, `450002222` |
| EUROREPAR | `1646451280`, `1672354080`, `1613721180`, `1680338480` |
| CWORKS | `B13CR0077`, `B13MR0116`, `B130G0104` |

This is the primary driver of the high `countArticles` value. Group by `crossManufacturerName` to get distinct cross-reference brands.

### Same `crossNumber` from Different Manufacturers

The same part number string can be used by multiple manufacturers:

| `crossNumber` | Manufacturers |
|--------------|---------------|
| `"18386"` | MEAT & DORIA, HOFFER |
| `"HA-706"` | AMC Filter, KAVO PARTS |
| `"1714605"` | KRAFT AUTOMOTIVE, SAKURA |

Always use `crossManufacturerName + crossNumber` together as the unique key.

### Response Shape: Input Article Data Repeated

Unlike [#50 Cross-References by Article ID](#50-get-cross-references-by-article-id) where each row is a **different article**, here every row represents the **same input article** with a different cross-reference entry:

| Field group | Varies per row? |
|-------------|-----------------|
| `articleBrandRoot`, `articleNumberRoot` | No — always the input article |
| `articleId`, `supplierId` | No — always the input article |
| `articleMediaFileName`, `s3image` | No — always the input article image |
| `crossManufacturerName`, `crossNumber` | Yes — one per cross-reference entry |
| `searchLevel` | Yes — `"IAM -> OEM"` or `"IAM -> OEM -> IAM"` |

### Comparison: #53 vs Other Cross-Reference Endpoints

| Aspect | [#50 Cross-Refs by Article ID](#50-get-cross-references-by-article-id) | [#51 Equivalent OEM Numbers](#51-get-equivalent-oem-numbers) | #53 Cross-Refs through OEM by Article ID |
|--------|-------------------------------------------------------------------------|--------------------------------------------------------------|------------------------------------------|
| Input | `articleId` | OEM number string | `articleId` |
| Output rows | One per equivalent **article** | One per OEM variant match | One per `crossManufacturerName + crossNumber` |
| Varying field | `articleId`, `articleNo`, `supplierName` | `articleId`, `articleNo`, `oemNo[]` | `crossManufacturerName`, `crossNumber`, `searchLevel` |
| Repeated field | `articleProductName` | — (raw array) | Entire input article (brand, number, media) |
| `searchLevel` field | No | No | Yes |
| OEM manufacturer numbers | No | Yes (in `oemNo[]`) | Yes — `searchLevel: "IAM -> OEM"` rows |
| IAM cross-references | Yes | No | Yes — `searchLevel: "IAM -> OEM -> IAM"` rows |
| Self-reference in results | No | No | Yes |
| `countArticles` meaning | Distinct equivalent articles | N/A (raw array) | Total cross-reference rows (not distinct brands) |

### Notes

- `countArticles` counts rows (one per `crossManufacturerName + crossNumber`), not distinct cross-reference brands — group by `crossManufacturerName` to get the true distinct brand count
- The input article's data (`articleBrandRoot`, `articleNumberRoot`, `articleId`, `supplierId`, media) is the same on every row — it is not the cross-reference article's data
- The input article always appears as its own cross-reference with `searchLevel: "IAM -> OEM -> IAM"` — filter it out when showing results to users
- `searchLevel: "IAM -> OEM"` rows identify the OEM vehicle manufacturer numbers directly covered by the article
- `searchLevel: "IAM -> OEM -> IAM"` rows identify other aftermarket brands covering the same OEM numbers
- The same `crossNumber` can appear under multiple `crossManufacturerName` values — use both fields together as the unique key
- The "RapidAPI Response Body Size: 2 Bytes" is a known dashboard measurement artefact

---

## 54. POST Equivalent OEM Numbers

**Method:** POST
**Status:** 200 OK
**Response Time:** 1658 ms
**Date:** 2026-04-11T11:35:22.327Z
**Response Body Size:** 2 Bytes *(RapidAPI dashboard artefact)*
**URL:** `https://tecdoc-catalog.p.rapidapi.com/articles-oem/all-equal-oem-no`
**Section:** Parts Cross Reference

### Overview

This is the **POST variant** of [#51 GET Equivalent OEM Numbers](#51-get-equivalent-oem-numbers). Both endpoints return the same response structure: a raw JSON array of aftermarket articles that cross-reference a given OEM number, with each article's full `oemNo[]` array included. The only difference is how the input is provided — this endpoint accepts the OEM number in the POST request body rather than as a URL path parameter.

See [#51 GET Equivalent OEM Numbers](#51-get-equivalent-oem-numbers) for complete field documentation, duplicate row behaviour, and `oemNo` coverage details.

### Difference from #51 GET

| Aspect | [#51 GET Equivalent OEM Numbers](#51-get-equivalent-oem-numbers) | #54 POST Equivalent OEM Numbers |
|--------|------------------------------------------------------------------|----------------------------------|
| Method | GET | POST |
| URL | `.../articles-oem/search-all-equal-oem-no/lang-id/{lang_id}/article-oem-no/{oem_no}` | `.../articles-oem/all-equal-oem-no` |
| Input | OEM number + `lang_id` in URL path | OEM number in POST request body |
| Response shape | Raw JSON array | Raw JSON array (identical) |
| Response fields | `articleId`, `articleSearchNo`, `articleNo`, `oemNo[]` | Identical |
| `lang_id` parameter | Required in URL path | Provided in POST body (confirm exact body schema from RapidAPI) |

### Parameters

| Parameter | Location | Type | Required | Description |
|-----------|----------|------|----------|-------------|
| (OEM number) | POST body | string | Yes | OEM part number to search — confirm exact body field name from RapidAPI dashboard |
| (lang_id) | POST body | integer | Likely | Language ID — confirm whether required in POST body |

### Response

Identical structure to [#51](#51-get-equivalent-oem-numbers) — raw JSON array, one element per matching article per OEM format variant. Refer to #51 for the full response field table, duplicate row explanation, and deduplication strategy.

**Sample response fields** (same as #51):

```json
[
  {
    "articleId": 412619,
    "articleSearchNo": "517501D000",
    "articleNo": "04-P432",
    "oemNo": [
      { "oemBrand": "HYUNDAI", "oemDisplayNo": "517501D000" },
      { "oemBrand": "KIA",     "oemDisplayNo": "517501D000" },
      { "oemBrand": "HYUNDAI", "oemDisplayNo": "5175039600" },
      { "oemBrand": "KIA",     "oemDisplayNo": "5175039600" }
    ]
  }
]
```

### Notes

- Use this endpoint when submitting the OEM number via POST body is preferred over URL path encoding (avoids special character URL-encoding issues)
- The `articleId: 5850138` (`AZMT-42-050-1308`) appears with `oemNo[]` entries mixing both hyphenated (`"51750-1D000"`) and compact (`"517501D000"`) format variants within a single `oemNo` array — the array is not normalised to one format
- The "RapidAPI Response Body Size: 2 Bytes" is a known dashboard measurement artefact

---

## 55. GET Cross-References via OEM Number by Article ID

<!-- TODO: confirm URL from RapidAPI dashboard -->

**Method:** GET
**Status:** 200 OK
**Response Time:** (confirm from RapidAPI dashboard)
**Section:** Parts Cross Reference

### Overview

Given an article ID, returns all cross-reference articles discovered via shared OEM number coverage — with full media information included per result. Input an article ID to find every other aftermarket part that covers at least one of the same OEM numbers, along with each result's images.

This is structurally similar to [#50 GET Cross-References by Article ID](#50-get-cross-references-by-article-id) but differs in two important ways: the lookup path is through OEM number matching, and **each article produces one row per media file** (not one row per article). The fields are the same as #50.

### Parameters

| Parameter | Location | Type | Required | Description |
|-----------|----------|------|----------|-------------|
| `article_id` | path or query | integer | Yes | TecDoc internal article ID — confirm full URL from RapidAPI dashboard |

### Response Sample

```json
{
  "countArticles": 327,
  "articles": [
    {
      "articleId": 6159145,
      "articleNo": "C 16 134/1",
      "supplierName": "MANN-FILTER",
      "supplierId": 4,
      "articleProductName": "Air Filter",
      "articleMediaType": "JPG",
      "articleMediaFileName": "567711cc310654db6a7077432f4093598daef481.webp",
      "s3image": "https://fsn1.your-objectstorage.com/tecdoc2025/media_files/images/4/567711cc310654db6a7077432f4093598daef481.webp"
    },
    {
      "articleId": 5844103,
      "articleNo": "AZMT-41-030-1370",
      "supplierName": "A.Z. Meisterteile",
      "supplierId": 5275,
      "articleProductName": "Air Filter",
      "articleMediaType": "GIF",
      "articleMediaFileName": "76f6b2efff02f7c2f9f16453f75ba8bff68f2920.gif",
      "s3image": "https://fsn1.your-objectstorage.com/tecdoc2025/media_files/images/5275/76f6b2efff02f7c2f9f16453f75ba8bff68f2920.gif"
    },
    {
      "articleId": 2931668,
      "articleNo": "359002310260",
      "supplierName": "MAGNETI MARELLI",
      "supplierId": 95,
      "articleProductName": "Air Filter",
      "articleMediaType": null,
      "articleMediaFileName": null,
      "s3image": null
    },
    {
      "articleId": 7963716,
      "articleNo": "LX 1780/3",
      "supplierName": "KNECHT",
      "supplierId": 34,
      "articleProductName": "Air Filter",
      "articleMediaType": "JPEG",
      "articleMediaFileName": "d76fea362b5cbe119795761082b6dc148ec5dafd.webp",
      "s3image": "https://fsn1.your-objectstorage.com/tecdoc2025/media_files/images/34/d76fea362b5cbe119795761082b6dc148ec5dafd.webp"
    },
    {
      "articleId": 7963717,
      "articleNo": "LX 1780/3",
      "supplierName": "MAHLE",
      "supplierId": 287,
      "articleProductName": "Air Filter",
      "articleMediaType": "JPEG",
      "articleMediaFileName": "d76fea362b5cbe119795761082b6dc148ec5dafd.webp",
      "s3image": "https://fsn1.your-objectstorage.com/tecdoc2025/media_files/images/287/d76fea362b5cbe119795761082b6dc148ec5dafd.webp"
    }
  ]
}
```

### Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `countArticles` | integer | Total rows (includes one row per media file per article — not distinct articles) |
| `articles` | array | All cross-reference results with media |
| `articles[].articleId` | integer | TecDoc article ID of the cross-reference article |
| `articles[].articleNo` | string | Supplier-specific part number |
| `articles[].supplierName` | string | Supplier/brand name |
| `articles[].supplierId` | integer | TecDoc internal supplier ID |
| `articles[].articleProductName` | string | Product category |
| `articles[].articleMediaType` | string \| null | Declared media format (`"JPEG"`, `"JPG"`, `"BMP"`, `"PNG"`, `"GIF"`) — or `null` |
| `articles[].articleMediaFileName` | string \| null | SHA-1 filename — `.webp` for all types except `"GIF"` → `.gif` |
| `articles[].s3image` | string \| null | Full S3 URL |

### Duplication: One Row per Media File

Unlike [#50](#50-get-cross-references-by-article-id) which gives one row per cross-reference article, this endpoint gives **one row per media file per article**. Articles with multiple images appear multiple times:

| `articleId` | `articleNo` | Supplier | Row count | Reason |
|-------------|-------------|----------|-----------|--------|
| `1432888` | `153071760233` | MAGNETI MARELLI | 3 | 3 images |
| `1630242` | `180032410` | AUTOMEGA | 3 | 3 images |
| `6926328` | `F 026 400 492` | BOSCH | 4 | 4 images |
| `6960417` | `F215801` | KAMOKA | 4 | 4 images |
| `7963718` | `LX 1780/3` | METAL LEVE | 4 | 4 images |
| `5844103` | `AZMT-41-030-1370` | A.Z. Meisterteile | 3 | GIF + 2 JPG |

Deduplicate by `articleId` before counting or displaying distinct cross-reference articles.

### GIF Media Type

`articleId: 5844103` (`AZMT-41-030-1370`) has `articleMediaType: "GIF"` with `articleMediaFileName` ending in `.gif` — consistent with the GIF exception documented in [#41](#41-get-article-list-by-vehicle-id--category-id). The same article also has two `"JPG"` rows, giving it 3 total rows in the response.

### Null Media Fields

Several articles have null media: MAGNETI MARELLI `359002310260`, MASTER-SPORT GERMANY `450001863`, MOTRIO `8671018991`, REVITA `FRA00152`, FIL FILTER `HP 2633`. Always null-check before rendering.

### Same `articleNo`, Different Suppliers

Multiple patterns of shared part numbers across suppliers:

| `articleNo` | Suppliers | Notes |
|-------------|-----------|-------|
| `LX 1780/3` | KNECHT (34), MAHLE (287), METAL LEVE (4677) | 3 different `articleId`s |
| `FKFRD008` | MEAT & DORIA (244), HOFFER (341) | 2 different `articleId`s |
| `FKFRD009`, `FKFRD010`, `FKFRD011`, `FKVLV001` | Same MEAT & DORIA / HOFFER pair | Paired numbering scheme |

KNECHT and MAHLE share `articleMediaFileName: "d76fea362b5cbe119795761082b6dc148ec5dafd.webp"` despite being different suppliers with different `articleId`s — consistent SHA-1 content-addressing.

### Mixed `articleProductName`

Most results are `"Air Filter"`, but MEAT & DORIA/HOFFER `FKFRD008–011` and `FKVLV001` are `"Filter Set"`. Filter sets contain air filters, so this is expected for OEM-based cross-reference lookups — OEM number coverage can span related product categories.

### Comparison: #55 vs #50

| Aspect | [#50 Cross-Refs by Article ID](#50-get-cross-references-by-article-id) | #55 Cross-Refs via OEM Number by Article ID |
|--------|-------------------------------------------------------------------------|----------------------------------------------|
| Input | `articleId` | `articleId` |
| Lookup method | Direct cross-reference table | Via shared OEM number coverage |
| Rows per result article | 1 | 1 per media file |
| `articleId: null` possible | Yes | No (not observed) |
| Duplication source | None | Media files per article |
| `countArticles` meaning | Distinct cross-reference articles | Total rows (not distinct articles) |
| Media included | Yes (1 image per article) | Yes (all images per article) |

### Notes

- `countArticles` counts rows, not distinct articles — deduplicate by `articleId` for distinct count
- One row per media file: articles with N images appear N times
- `articleMediaType: "GIF"` yields a `.gif` URL (not `.webp`) — consistent with all other endpoints
- Same `articleNo` used by different suppliers (e.g., `LX 1780/3`) results in multiple distinct `articleId`s — use `supplierId + articleNo` as the unique article key
- The "RapidAPI Response Body Size: 2 Bytes" is a known dashboard measurement artefact

---

## 56. GET VIN Check

**Method:** GET
**Section:** VIN
**Date tested:** 2026-04-13
**Response time:** 2501 ms
**Status:** 200 OK

**URL:**
```
https://tecdoc-catalog.p.rapidapi.com/vin/tecdoc-vin-check/{vin}
```

**Path Params:**

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `vin` | string | Yes | 17-character Vehicle Identification Number |

**Example request:**
```
GET /vin/tecdoc-vin-check/WDBFA68F42F202731
```

---

### Response

```json
{
  "data": {
    "dataSource": [
      {
        "dataSourceKey": "vin_filter"
      }
    ],
    "matchingModels": {
      "array": [
        {
          "manuId": 74,
          "modelId": 39,
          "modelName": "SL (R129)"
        }
      ]
    },
    "matchingVehicles": {
      "array": [
        {
          "manuId": 74,
          "carName": "MERCEDES-BENZ SL (R129) 500 (129.068)",
          "modelId": 39,
          "vehicleId": 9433,
          "linkageTargetType": "P",
          "subLinkageTargetType": "V",
          "vehicleTypeDescription": "500 (129.068)"
        }
      ]
    },
    "matchingManufacturers": {
      "array": [
        {
          "manuId": 74,
          "manuName": "MERCEDES-BENZ"
        }
      ]
    },
    "matchingVehiclesCount": 1
  },
  "status": 200
}
```

---

### Response Fields

#### Top Level

| Field | Type | Description |
|-------|------|-------------|
| `data` | object | All VIN match results |
| `status` | int | HTTP status code echoed in body |

#### `data.dataSource[]`

| Field | Type | Description |
|-------|------|-------------|
| `dataSourceKey` | string | Decode method used. `"vin_filter"` = TecDoc VIN filter database |

#### `data.matchingManufacturers.array[]`

| Field | Type | Description |
|-------|------|-------------|
| `manuId` | int | Manufacturer ID — same ID used in #6, #7, #8 |
| `manuName` | string | Manufacturer display name |

#### `data.matchingModels.array[]`

| Field | Type | Description |
|-------|------|-------------|
| `manuId` | int | Manufacturer ID |
| `modelId` | int | Model ID — same ID used in #8, #9, #12, #14 |
| `modelName` | string | Model display name including generation code |

#### `data.matchingVehicles.array[]`

| Field | Type | Description |
|-------|------|-------------|
| `manuId` | int | Manufacturer ID |
| `modelId` | int | Model ID |
| `vehicleId` | int | **Vehicle ID — same ID used in #28, #41 for parts lookup** |
| `carName` | string | Full car name: `"{BRAND} {MODEL} {TRIM}"` |
| `vehicleTypeDescription` | string | Engine/trim variant description |
| `linkageTargetType` | string | `"P"` = Passenger car, `"N"` = Commercial vehicle, `"B"` = Motorbike |
| `subLinkageTargetType` | string | `"V"` = Vehicle |

#### `data.matchingVehiclesCount`

| Field | Type | Description |
|-------|------|-------------|
| `matchingVehiclesCount` | int | Total number of matched vehicles |

---

### Notes

- This endpoint is named "VIN Check" but it is actually a **full VIN-to-vehicle resolver**, not just a format validator — it returns `vehicleId`, `modelId`, and `manuId` directly
- The `vehicleId` returned is the **same ID used throughout the TecDoc API** (#28 categories, #41 article list, #43 compatible vehicles) — a valid VIN resolves the entire vehicle selection flow in a single call
- **Kalaax use case:** User pastes their VIN → skip the full make/model/year selection (#5 → #6 → #8 → #14) and go straight to parts browsing with the returned `vehicleId`
- `matchingVehiclesCount > 1` means the VIN matched multiple variants — show a disambiguation screen to the user
- `matchingVehiclesCount: 0` means VIN not found in TecDoc database — fall back to manual make/model/year selection
- `dataSourceKey: "vin_filter"` — TecDoc uses its own internal VIN-to-vehicle filter database, not a general VIN decoder
- Response time is ~2500 ms — notably slower than other endpoints; consider showing a loading state
- The "RapidAPI Response Body Size: 2 Bytes" is a known dashboard measurement artefact

---

## 57. GET VIN Decoder (v1)

**Method:** GET
**Section:** VIN
**Date tested:** 2026-04-13
**Response time:** 956 ms
**Status:** 200 OK

**URL:**
```
https://tecdoc-catalog.p.rapidapi.com/vin/decoder-v1/{vin}
```

**Path Params:**

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `vin` | string | Yes | 17-character Vehicle Identification Number |

**Example request:**
```
GET /vin/decoder-v1/WDBFA68F42F202731
```

---

### Response

```json
{
  "vin": "WDBFA68F42F202731",
  "wmi": "WDB",
  "vds": "FA68F4",
  "vis": "2F202731",
  "region": "Europe",
  "country": "Germany",
  "manufacturer": "Mercedes-Benz",
  "modelYear": [
    2002
  ]
}
```

---

### Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `vin` | string | Input VIN echoed back |
| `wmi` | string | World Manufacturer Identifier — first 3 chars, identifies the manufacturer and country |
| `vds` | string | Vehicle Descriptor Section — chars 4–9, encodes model, body style, engine, check digit |
| `vis` | string | Vehicle Identifier Section — chars 10–17, encodes model year, plant, serial number |
| `region` | string | World region of manufacture (e.g. `"Europe"`, `"North America"`, `"Asia"`) |
| `country` | string | Country of manufacture derived from WMI |
| `manufacturer` | string | Manufacturer name derived from WMI |
| `modelYear` | int[] | Array of possible model years decoded from VIN position 10 — can have multiple values when a year code is ambiguous (e.g. 30-year VIN cycle repeats) |

---

### Notes

- **This is a pure VIN anatomy decoder — it returns NO TecDoc IDs** (`vehicleId`, `modelId`, `manuId` are absent)
- Compare with **#56 VIN Check** which returns TecDoc `vehicleId` for parts lookup — these are two different tools:
  - `#56 VIN Check` → use to find parts (returns `vehicleId`)
  - `#57 VIN Decoder v1` → use to display decoded info to the user (returns human-readable fields)
- `modelYear` is an array because VIN position 10 follows a 30-year repeating cycle — a code can map to two possible years (e.g. `2` = 2002 or 1972). Most modern cars will have only one value
- Much faster than #56 (956 ms vs 2501 ms) — no TecDoc database lookup, pure algorithmic decode
- **Kalaax use case:** Show the decoded VIN summary ("Mercedes-Benz, Germany, 2002") as a confirmation card before handing `vehicleId` from #56 to the parts browsing flow
- No TecDoc IDs means this cannot be used alone to browse parts — must be paired with #56
- The "RapidAPI Response Body Size: 2 Bytes" is a known dashboard measurement artefact

---

## 58. GET VIN Decoder (v2)

**Method:** GET
**Section:** VIN
**Date tested:** 2026-04-13
**Response time:** 1651 ms
**Status:** 200 OK

**URL:**
```
https://tecdoc-catalog.p.rapidapi.com/vin/decoder-v2/{vin}
```

**Path Params:**

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `vin` | string | Yes | 17-character Vehicle Identification Number |

**Example request:**
```
GET /vin/decoder-v2/WDBFA68F42F202731
```

---

### Response

```json
{
  "error_text": "0 - VIN decoded clean. Check Digit (9th position) is correct",
  "vehicle_descriptor": "WDBFA68F*2F",
  "make": "MERCEDES-BENZ",
  "manufacturer_name": "MERCEDES-BENZ CARS",
  "model": "SL-Class",
  "model_year": "2002",
  "plant_city": "BRERNEN",
  "trim": "SL500",
  "vehicle_type": "PASSENGER CAR",
  "plant_country": "GERMANY",
  "note": "Line: 129",
  "body_class": "Convertible/Cabriolet",
  "doors": "2",
  "gross_vehicle_weight_rating_from": "Class 1: 6,000 lb or less (2,722 kg or less)",
  "gross_vehicle_weight_rating_to": "Class 1: 6,000 lb or less (2,722 kg or less)",
  "bed_type": "Not Applicable",
  "cab_type": "Not Applicable",
  "trailer_type_connection": "Not Applicable",
  "trailer_body_type": "Not Applicable",
  "custom_motorcycle_type": "Not Applicable",
  "motorcycle_suspension_type": "Not Applicable",
  "motorcycle_chassis_type": "Not Applicable",
  "bus_floor_configuration_type": "Not Applicable",
  "bus_type": "Not Applicable",
  "engine_number_of_cylinders": "8",
  "displacement_(cc)": "5000",
  "displacement_(ci)": "305.1187204736",
  "displacement_(l)": "5",
  "fuel_type_-_primary": "Gasoline",
  "engine_configuration": "V-Shaped",
  "engine_brake_(hp)_from": "302",
  "engine_manufacturer": "MB",
  "pretensioner": "Yes",
  "seat_belt_type": "Manual",
  "other_restraint_system_info": "Type-2 Belt with Emergency Tensioning Retractors, Air Bag, Knee Bolster, Side Impact Air Bag in Door",
  "front_air_bag_locations": "1st Row (Driver and Passenger)",
  "knee_air_bag_locations": "1st Row (Driver and Passenger)",
  "side_air_bag_locations": "1st Row (Driver and Passenger)"
}
```

---

### Response Fields

#### VIN Validation

| Field | Type | Description |
|-------|------|-------------|
| `error_text` | string | VIN validation result — despite the name, `"0 - VIN decoded clean"` means **valid**. A non-zero prefix indicates a decode issue |
| `vehicle_descriptor` | string | VIN pattern with check digit (position 9) masked as `*` — used for batch VIN pattern matching |

#### Vehicle Identity

| Field | Type | Description |
|-------|------|-------------|
| `make` | string | Brand name (e.g. `"MERCEDES-BENZ"`) |
| `manufacturer_name` | string | Full legal manufacturer name (e.g. `"MERCEDES-BENZ CARS"`) |
| `model` | string | Model line name (e.g. `"SL-Class"`) |
| `model_year` | string | Model year as string (e.g. `"2002"`) — single value unlike v1's array |
| `trim` | string | Trim/variant level (e.g. `"SL500"`) |
| `vehicle_type` | string | `"PASSENGER CAR"`, `"TRUCK"`, `"MOTORCYCLE"`, `"BUS"`, etc. |
| `body_class` | string | Body style (e.g. `"Convertible/Cabriolet"`, `"Sedan"`, `"SUV"`) |
| `doors` | string | Number of doors as string |
| `note` | string | Additional notes from the database (e.g. `"Line: 129"`) |

#### Manufacturing

| Field | Type | Description |
|-------|------|-------------|
| `plant_city` | string | City where vehicle was assembled |
| `plant_country` | string | Country where vehicle was assembled |

#### Engine

| Field | Type | Description |
|-------|------|-------------|
| `engine_number_of_cylinders` | string | Number of cylinders as string |
| `displacement_(cc)` | string | Engine displacement in cubic centimetres |
| `displacement_(ci)` | string | Engine displacement in cubic inches |
| `displacement_(l)` | string | Engine displacement in litres |
| `fuel_type_-_primary` | string | Primary fuel type (e.g. `"Gasoline"`, `"Diesel"`) |
| `engine_configuration` | string | Engine layout (e.g. `"V-Shaped"`, `"In-Line"`) |
| `engine_brake_(hp)_from` | string | Horsepower rating |
| `engine_manufacturer` | string | Engine manufacturer code |

#### Weight

| Field | Type | Description |
|-------|------|-------------|
| `gross_vehicle_weight_rating_from` | string | GVWR lower bound — US weight class system |
| `gross_vehicle_weight_rating_to` | string | GVWR upper bound |

#### Safety

| Field | Type | Description |
|-------|------|-------------|
| `pretensioner` | string | Seat belt pretensioner present (`"Yes"` / `"No"`) |
| `seat_belt_type` | string | Seat belt type |
| `other_restraint_system_info` | string | Full restraint system description |
| `front_air_bag_locations` | string | Front airbag coverage |
| `knee_air_bag_locations` | string | Knee airbag coverage |
| `side_air_bag_locations` | string | Side airbag coverage |

#### Not Applicable Fields (for passenger cars)

These fields return `"Not Applicable"` for standard passenger cars — they are only populated for trucks, motorcycles, trailers, and buses:
`bed_type`, `cab_type`, `trailer_type_connection`, `trailer_body_type`, `custom_motorcycle_type`, `motorcycle_suspension_type`, `motorcycle_chassis_type`, `bus_floor_configuration_type`, `bus_type`

---

### Notes

- **No TecDoc IDs** — like v1, this returns no `vehicleId`, `modelId`, or `manuId`. Cannot be used alone for parts lookup — must be paired with #56
- **Data source is NHTSA vPIC** (US government VIN database) — evidenced by US-centric GVWR classes (`"Class 1: 6,000 lb or less"`), `plant_city: "BRERNEN"` (likely a typo for Bremen in the NHTSA DB), and the imperial displacement fields
- **`error_text` is not an error field** — `"0 - ..."` prefix means clean decode. Only treat it as an error if the prefix is non-zero
- `model_year` is a string here vs an array in v1 — v2 resolves ambiguity and returns a single confirmed year
- **Richest human-readable decoder of the three** (v1, v2, v3) — includes engine specs, body class, trim, safety equipment, plant details
- Response time 1651 ms — faster than #56 (2501 ms), slower than v1 (956 ms)
- Many fields return `"Not Applicable"` for passenger cars — filter these out before displaying to the user
- **Kalaax use case:** Show rich car confirmation card after VIN entry — display `make`, `model`, `trim`, `model_year`, `body_class`, `engine_number_of_cylinders`, `displacement_(l)`, `fuel_type_-_primary` alongside the `vehicleId` from #56
- The "RapidAPI Response Body Size: 2 Bytes" is a known dashboard measurement artefact

---

## 59. GET VIN Decoder (v3)

**Method:** GET
**Section:** VIN
**Date tested:** 2026-04-13
**Response time:** 1144 ms
**Status:** 200 OK

**URL:**
```
https://tecdoc-catalog.p.rapidapi.com/vin/decoder-v3/{vin}
```

**Path Params:**

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `vin` | string | Yes | 17-character Vehicle Identification Number |

**Example request:**
```
GET /vin/decoder-v3/VSEFJB43C00100765
```

---

### Response

```json
[
  {
    "title": "General information",
    "information": {
      "Make": "Suzuki",
      "Model": "Jimny",
      "Model year": "2005",
      "Body style": "3 Doors Off Road",
      "Engine type": "1.3",
      "Fuel type": "Gasoline",
      "Transmission": "5-Speed Manual",
      "Vehicle class": "Mini SUV",
      "Vehicle type": "SUV",
      "Manufactured in": "Spain"
    }
  },
  {
    "title": "Manufacturer",
    "information": {
      "Manufacturer": "Santana Motor SA",
      "Adress line 1": "Avenida Primero De Mayo S/N",
      "Adress line 2": "23700 Linares",
      "Region": "Europe",
      "Country": "Spain",
      "Note": "Manufacturer builds more than 500 vehicles per year"
    }
  },
  {
    "title": "Vehicle specification",
    "information": {
      "Body type": "Off Road",
      "Number of doors": "3",
      "Number of seats": "4",
      "Displacement SI": "1328",
      "Displacement CID": "81",
      "Displacement Nominal": "1.3",
      "Engine HorsePower": "85",
      "Engine KiloWatts": "63",
      "Manual gearbox": "5MT",
      "Fuel type": "Gasoline",
      "Emission standard": "Euro 4"
    }
  }
]
```

---

### Response Structure

The response is a **flat array of section objects** — each section has a `title` and an `information` object. The number and contents of sections may vary by vehicle.

| Field | Type | Description |
|-------|------|-------------|
| `[].title` | string | Section name — e.g. `"General information"`, `"Manufacturer"`, `"Vehicle specification"` |
| `[].information` | object | Key-value pairs of decoded fields for that section. Keys are human-readable labels |

#### Section: `"General information"`

| Key | Description |
|-----|-------------|
| `Make` | Brand name |
| `Model` | Model name |
| `Model year` | Model year as string |
| `Body style` | Body style description including door count |
| `Engine type` | Engine size label (e.g. `"1.3"`) |
| `Fuel type` | Primary fuel type |
| `Transmission` | Gearbox description (e.g. `"5-Speed Manual"`) |
| `Vehicle class` | Marketing class (e.g. `"Mini SUV"`) |
| `Vehicle type` | Vehicle category (e.g. `"SUV"`) |
| `Manufactured in` | Country of assembly |

#### Section: `"Manufacturer"`

| Key | Description |
|-----|-------------|
| `Manufacturer` | Full legal manufacturer name |
| `Adress line 1` | Manufacturer address line 1 |
| `Adress line 2` | Manufacturer address line 2 (city + postal code) |
| `Region` | World region |
| `Country` | Country of manufacturer |
| `Note` | Production volume note |

#### Section: `"Vehicle specification"`

| Key | Description |
|-----|-------------|
| `Body type` | Body type (e.g. `"Off Road"`, `"Sedan"`) |
| `Number of doors` | Door count as string |
| `Number of seats` | Seat count as string |
| `Displacement SI` | Engine displacement in cc |
| `Displacement CID` | Engine displacement in cubic inches |
| `Displacement Nominal` | Engine displacement in litres (nominal label) |
| `Engine HorsePower` | Power output in HP |
| `Engine KiloWatts` | Power output in kW |
| `Manual gearbox` | Gearbox code (e.g. `"5MT"` = 5-speed manual) |
| `Fuel type` | Fuel type (repeated from General) |
| `Emission standard` | Euro emissions standard (e.g. `"Euro 4"`) |

---

### Notes

- **Completely different structure to v1 and v2** — returns an array of labelled sections instead of a flat object. Must be parsed by iterating sections and reading `information` keys
- **No TecDoc IDs** — like v1 and v2, no `vehicleId`, `modelId`, or `manuId`. Still cannot be used alone for parts lookup — must be paired with #56
- **Includes fields absent from v1 and v2:** `Transmission`, `Vehicle class`, `Number of seats`, `Engine KiloWatts`, `Emission standard`, full manufacturer address
- **Different VIN used in test** — `VSEFJB43C00100765` (Suzuki Jimny, Spain, 2005) vs `WDBFA68F42F202731` (Mercedes-Benz SL, Germany, 2002) used in v1/v2 — field availability may vary by vehicle
- `information` keys are human-readable strings with mixed casing and spaces — not machine-friendly identifiers. Must access by exact string key (e.g. `information["Number of seats"]`)
- Note the typo in source data: `"Adress line 1"` / `"Adress line 2"` (single `d`) — this comes from the upstream data source, store and display as-is
- **Kalaax use case:** Best for showing a structured confirmation card with sections — `Emission standard` is useful for Egyptian import compliance checks; `Number of seats` and `Transmission` enrich the vehicle profile
- Response time 1144 ms — faster than v2 (1651 ms) and #56 (2501 ms)
- The "RapidAPI Response Body Size: 2 Bytes" is a known dashboard measurement artefact

---

## 60. GET VIN Decoder (all-in-one)

**Method:** GET
**Section:** VIN
**Date tested:** 2026-04-13
**Response time:** 2592 ms
**Status:** 200 OK

**URL:**
```
https://tecdoc-catalog.p.rapidapi.com/vin/decoder-v5/{vin}
```

> Note: The RapidAPI dashboard calls this "all-in-one" but the actual endpoint path is `/vin/decoder-v5/` — not `/vin/decoder-all-in-one/`.

**Path Params:**

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `vin` | string | Yes | 17-character Vehicle Identification Number |

**Example request:**
```
GET /vin/decoder-v5/WDBFA68F42F202731
```

---

### Response

```json
{
  "vin-data-1": {
    "content": "{\"vin\":\"WDBFA68F42F202731\",\"wmi\":\"WDB\",\"vds\":\"FA68F4\",\"vis\":\"2F202731\",\"region\":\"Europe\",\"country\":\"Germany\",\"manufacturer\":\"Mercedes-Benz\",\"modelYear\":[2002]}",
    "statusCode": 200,
    "successful": true,
    "ok": true,
    "headers": {
      "cache-control": ["no-cache, private"],
      "content-type": ["application/json"]
    },
    "encodingOptions": 15,
    "protocolVersion": "1.0",
    "cacheable": false,
    "fresh": false,
    "age": 2,
    "date": "2026-04-13T04:39:58+00:00",
    "..."  : "... (other HTTP metadata fields omitted for brevity)"
  },
  "vin-data-2": {
    "content": "{\"error_text\":\"0 - VIN decoded clean. Check Digit (9th position) is correct\",\"make\":\"MERCEDES-BENZ\",\"model\":\"SL-Class\",\"model_year\":\"2002\",\"trim\":\"SL500\",\"body_class\":\"Convertible/Cabriolet\",\"doors\":\"2\",\"engine_number_of_cylinders\":\"8\",\"displacement_(l)\":\"5\",\"fuel_type_-_primary\":\"Gasoline\",...}",
    "statusCode": 200,
    "successful": true,
    "ok": true,
    "..."  : "... (same HTTP metadata structure as vin-data-1)"
  },
  "vin-data-3": {
    "content": "[{\"title\":\"Manufacturer\",\"information\":{\"Manufacturer\":\"Daimler AG\",\"Adress line 1\":\"Mercedesstrasse 137\",\"Adress line 2\":\"D-70546 Stuttgart\",\"Region\":\"Europe\",\"Country\":\"Germany\",\"Note\":\"Manufacturer builds more than 500 vehicles per year\"}}]",
    "statusCode": 200,
    "successful": true,
    "ok": true,
    "..."  : "... (same HTTP metadata structure as vin-data-1)"
  }
}
```

---

### Response Structure

The top-level response is an object with three fixed keys: `vin-data-1`, `vin-data-2`, `vin-data-3` — each maps to the output of one decoder.

| Key | Corresponds to | Content |
|-----|---------------|---------|
| `vin-data-1` | #57 VIN Decoder v1 | Flat object: `vin`, `wmi`, `vds`, `vis`, `region`, `country`, `manufacturer`, `modelYear[]` |
| `vin-data-2` | #58 VIN Decoder v2 | Flat object: full NHTSA fields — `make`, `model`, `trim`, `engine_*`, `body_class`, `doors`, safety fields, etc. |
| `vin-data-3` | #59 VIN Decoder v3 | Array of section objects: `[{title, information{...}}]` |

#### Per sub-result fields

| Field | Type | Description |
|-------|------|-------------|
| `content` | string | **JSON-serialised string** of the actual decoder response — must be `JSON.parse()`d to access data |
| `statusCode` | int | HTTP status of that individual decoder call |
| `successful` | bool | `true` if `statusCode` is 2xx |
| `ok` | bool | Alias of `successful` |
| `date` | string | ISO 8601 timestamp of when that sub-request was made |
| `age` | int | Seconds since the sub-response was generated |
| `headers` | object | HTTP response headers from that sub-call |
| `encodingOptions` | int | Internal encoding flag |
| `cacheable` / `fresh` / `immutable` | bool | Cache metadata — all `false` for these endpoints |
| `expires` / `maxAge` / `ttl` / `lastModified` / `etag` | null | Cache fields — all `null` |

---

### How to Parse

The `content` field is a **JSON string, not a nested object** — double parsing is required:

```python
import json

response = ...  # parsed outer JSON

v1_data = json.loads(response["vin-data-1"]["content"])
# → {"vin": "...", "wmi": "WDB", "manufacturer": "Mercedes-Benz", "modelYear": [2002], ...}

v2_data = json.loads(response["vin-data-2"]["content"])
# → {"make": "MERCEDES-BENZ", "model": "SL-Class", "trim": "SL500", "engine_number_of_cylinders": "8", ...}

v3_data = json.loads(response["vin-data-3"]["content"])
# → [{"title": "Manufacturer", "information": {"Manufacturer": "Daimler AG", ...}}]
```

---

### Notes

- **Actual endpoint is `/vin/decoder-v5/`** — the "all-in-one" label is only in the RapidAPI dashboard name
- **`content` is a JSON string, not a nested object** — always `JSON.parse()` before accessing any data fields
- **`vin-data-3` returned only the Manufacturer section** for this VIN (`WDBFA68F42F202731`) vs three sections for the Suzuki Jimny test in #59 — v3 section availability varies by vehicle and data coverage
- **Slowest of all VIN endpoints at 2592 ms** — it calls all three decoders sequentially and wraps results; `age` field increments across sub-calls (0, 1, 2) confirming sequential execution
- **No TecDoc IDs** — same as v1/v2/v3 individually. Still must pair with #56 for parts lookup
- The HTTP metadata fields (`cacheable`, `fresh`, `etag`, `vary`, `expires`, etc.) are all `null`/`false`/`[]` — these are wrapper artefacts, not meaningful cache directives
- **When to use:** Only if you need all three decoder outputs simultaneously in one call. If you only need one decoder's data, call that endpoint directly — it will be faster and simpler to parse
- **Kalaax use case:** Use if building a rich VIN detail page that shows all decoder data at once. For the standard vehicle-selection-via-VIN flow, use #56 (for `vehicleId`) + #58 (for the richest flat confirmation data) as two separate calls instead
- The "RapidAPI Response Body Size: 2 Bytes" is a known dashboard measurement artefact

---

## 61. GET * Compatible Vehicles by Article No

**Method:** GET
**Section:** Article Search (`articles/` prefix)
**Date tested:** 2026-04-13
**Response time:** 1352 ms
**Status:** 200 OK

**URL:**
```
https://tecdoc-catalog.p.rapidapi.com/articles/get-compatible-cars-by-article-number/type-id/{typeId}?langId={langId}&countryFilterId={countryId}&articleNo={articleNo}
```

**Path Params:**

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `typeId` | int | Yes | Vehicle type ID — `1` = passenger car |

**Query Params:**

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `langId` | int | Yes | Language ID — `4` = English |
| `countryFilterId` | int | Yes | Country filter ID — narrows compatible vehicles to a market. `63` = France in test |
| `articleNo` | string | Yes | Article/part number (URL-encode spaces as `+`) |

**Example request:**
```
GET /articles/get-compatible-cars-by-article-number/type-id/1?langId=4&countryFilterId=63&articleNo=C+2029
```

---

### Response

```json
{
  "countArticles": 1,
  "articles": [
    {
      "articleId": 6159438,
      "articleNo": "C 2029",
      "articleProductName": "Air Filter",
      "supplierName": "MANN-FILTER",
      "supplierId": 4,
      "compatibleCars": [
        {
          "vehicleId": 4851,
          "modelId": 6234,
          "manufacturerName": "KIA",
          "modelName": "CEE'D SW (ED)",
          "typeEngineName": "1.4 CVVT",
          "constructionIntervalStart": "2009-07-01",
          "constructionIntervalEnd": "2012-12-01"
        },
        {
          "vehicleId": 7305,
          "modelId": 7471,
          "manufacturerName": "HYUNDAI",
          "modelName": "ELANTRA IV Saloon (HD)",
          "typeEngineName": "1.6 CVVT",
          "constructionIntervalStart": "2006-06-01",
          "constructionIntervalEnd": "2011-06-01"
        },
        {
          "vehicleId": 29865,
          "modelId": 7857,
          "manufacturerName": "HYUNDAI (BEIJING)",
          "modelName": "ELANTRA / YUEDONG (HD)",
          "typeEngineName": "1.6",
          "constructionIntervalStart": "2008-04-01",
          "constructionIntervalEnd": "2009-12-01"
        },
        {
          "vehicleId": 147300,
          "modelId": 7857,
          "manufacturerName": "HYUNDAI (BEIJING)",
          "modelName": "ELANTRA / YUEDONG (HD)",
          "typeEngineName": "LPG",
          "constructionIntervalStart": "2016-05-01",
          "constructionIntervalEnd": null
        }
      ]
    }
  ]
}
```

*(100+ items in `compatibleCars`. Sample rows above show: KIA, HYUNDAI, and HYUNDAI (BEIJING) all appear for the same air filter. `constructionIntervalEnd: null` = still in production.)*

---

### Response Fields

#### Top Level

| Field | Type | Description |
|-------|------|-------------|
| `countArticles` | int | Number of articles matched (typically 1 when searching by exact article number) |
| `articles` | array | List of matched article objects, each with a nested `compatibleCars` list |

#### `articles[]`

| Field | Type | Description |
|-------|------|-------------|
| `articleId` | int | TecDoc internal article ID — use for media, detail, and OEM lookups |
| `articleNo` | string | Article number as stored in TecDoc (may include spaces, e.g. `"C 2029"`) |
| `articleProductName` | string | Generic product category name (e.g. `"Air Filter"`) |
| `supplierName` | string | Brand/supplier name (e.g. `"MANN-FILTER"`) |
| `supplierId` | int | Supplier ID — use with `articleMediaFileName` to construct S3 URL |
| `compatibleCars` | array | List of all vehicle variants this article fits |

#### `articles[].compatibleCars[]`

| Field | Type | Nullable | Description |
|-------|------|----------|-------------|
| `vehicleId` | int | No | TecDoc vehicle ID — use directly in [#28 GET Categories by Vehicle ID](#28-get-list-categories-by-vehicle-id-v1) and [#41 GET Article List](#41-get-article-list-by-vehicle-id--category-id) |
| `modelId` | int | No | TecDoc model ID — use in [#8 GET Models by Type & Manufacturer](#8-get-models-by-type--manufacturer) lookups |
| `manufacturerName` | string | No | Brand name (e.g. `"KIA"`, `"HYUNDAI"`, `"HYUNDAI (BEIJING)"`) |
| `modelName` | string | No | Model name with TecDoc range code in parentheses (e.g. `"CEE'D SW (ED)"`) |
| `typeEngineName` | string | No | Engine/trim variant label (e.g. `"1.4 CVVT"`, `"LPG"`) |
| `constructionIntervalStart` | string | No | Production start date — ISO `"YYYY-MM-DD"` |
| `constructionIntervalEnd` | string | Yes | Production end date — ISO `"YYYY-MM-DD"`, or `null` if still in production |

---

### Notes

- **Reverse fitment lookup** — given an article number, returns every vehicle it fits. This is the inverse of [#41 GET Article List by Vehicle ID + Category ID](#41-get-article-list-by-vehicle-id--category-id) which goes vehicle → parts; this goes part → vehicles
- **`vehicleId` is present** — unlike #70 which returns human-readable vehicle data with no ID, this endpoint returns the TecDoc `vehicleId` on every row, enabling chaining into vehicle-specific parts lookups
- **`countryFilterId` affects results** — changing country narrows the compatible vehicle list to models sold in that market. For Kalaax (Egypt), find the Egypt country ID via [#2 GET Countries](#2-get-countries) and substitute `63`
- **`HYUNDAI (BEIJING)`** — Beijing Hyundai joint venture (China). KIA/Hyundai/Hyundai Beijing all appear in the same fitment list for Korean platform-shared parts — relevant for Egyptian market where Korean cars are common
- **`typeEngineName: "LPG"`** — some variants are identified only by fuel type with no displacement — display as-is; do not attempt to parse as a number
- **Article confirmed across the article object and its fitment list** — `supplierId: 4` is MANN-FILTER's TecDoc ID; use it with the standard S3 path: `media_files/images/4/{filename}.webp` for media
- **Different from #43 GET Compatible Vehicles by Article No & Supplier ID** — #43 takes `articleNo` + `supplierId` as path params and returns a simpler flat vehicle list. This endpoint takes only `articleNo` + filters as query params and returns a richer response with the article details wrapped around the fitment list. Use this endpoint when you have only an article number and want both article info and fitment in one call
- **Kalaax use case:** "This part fits these vehicles" section on the product detail page — call with the article number and display `compatibleCars` grouped by `manufacturerName`, showing `modelName` + `typeEngineName` + construction interval. The returned `vehicleId` values can also be stored so the user can switch vehicle context directly from the part page
- The "RapidAPI Response Body Size: 2 Bytes" is a known dashboard measurement artefact

---

## 62. GET * Analog Spare Parts by Article No

**Method:** GET
**Section:** Enhanced Article Search (`*` tier)
**Date tested:** 2026-04-13
**Response time:** — *(message truncated — metadata not captured)*
**Status:** 200 OK

**URL:**
```
TODO — message was truncated before metadata was captured. Confirm URL from RapidAPI dashboard.
```

> Note: RapidAPI dashboard name is **"Analog Spare Parts by Article No"** — stub was originally labelled "Article Details by Article No" based on a screenshot estimate.

---

### Response

```json
{
  "countArticles": 434,
  "articles": [
    {
      "articleId": 3122568,
      "articleNo": "40219",
      "supplierName": "3RG",
      "articleProductName": "Mounting, engine",
      "foundVia": "IAMNumber"
    },
    {
      "articleId": 1713517,
      "articleNo": "1900",
      "supplierName": "BGS",
      "articleProductName": "Thread Cutter Set",
      "foundVia": "ArticleNumber"
    },
    {
      "articleId": 1910852,
      "articleNo": "20A1452",
      "supplierName": "EACLIMA",
      "articleProductName": "Compressor, air conditioning",
      "foundVia": "OENumber"
    },
    {
      "articleId": 6957862,
      "articleNo": "F1900",
      "supplierName": "FRAP",
      "articleProductName": "Inner Tie Rod",
      "foundVia": "TradeNumber"
    }
  ]
}
```

*(Response truncated — 434 total articles. Sample rows above show all four `foundVia` value types.)*

---

### Response Fields

#### Top Level

| Field | Type | Description |
|-------|------|-------------|
| `countArticles` | int | Total number of matched articles across all search modes |
| `articles` | array | List of matched article objects |

#### `articles[]`

| Field | Type | Description |
|-------|------|-------------|
| `articleId` | int | TecDoc internal article ID |
| `articleNo` | string | Article number as stored in TecDoc for this supplier |
| `supplierName` | string | Brand/supplier name |
| `articleProductName` | string | Generic product category name |
| `foundVia` | string | How this article was matched — see table below |

#### `foundVia` Values

| Value | Meaning |
|-------|---------|
| `"ArticleNumber"` | Matched the input as a direct article number |
| `"IAMNumber"` | Matched as an IAM (Independent Aftermarket) number — cross-reference via shared aftermarket catalogue number |
| `"OENumber"` | Matched as an OEM (Original Equipment Manufacturer) number |
| `"TradeNumber"` | Matched as a trade/catalogue number used in distributor price lists |

---

### Notes

- **Searches across ALL number types simultaneously** — one call queries `ArticleNumber`, `IAMNumber`, `OENumber`, and `TradeNumber` in parallel. The `foundVia` field tells you which index matched
- **Analog = Equivalent/Alternative** — this endpoint is named "Analog Spare Parts" because it returns articles that are functionally equivalent to the searched number, not just exact matches on one number field. A single input article number can match hundreds of alternatives across suppliers
- **No media fields** — unlike #64 (deprecated), this response has no `articleMediaType`, `articleMediaFileName`, or `supplierId`. Must call #48 separately to get images
- **No `articleSearchNo`** — the input number used for matching is not echoed back; use `foundVia` to understand why each row matched
- **Duplicate rows present** — same `articleId` can appear multiple times when it matched via multiple number types (e.g. EACLIMA `20A1452` appears once as `IAMNumber` and once as `OENumber`). Deduplicate by `articleId` before displaying
- Same `articleId` + same `foundVia` duplicates also appear (seen with BORG & BECK, FEBI BILSTEIN, etc.) — root cause unknown, apply deduplication by `(articleId, foundVia)` tuple before display
- **countArticles: 434** for the tested input — very broad results including unrelated products (Thread Cutter Set, Exhaust System, Trailer Hitch). Filtering by `articleProductName` or category is recommended downstream
- **Kalaax use case:** "Search by any number" feature — user pastes any number format (OEM, aftermarket, trade) and this returns all known equivalent articles. Pair with #48 for images. Filter results by vehicle compatibility using #43 after retrieving candidates
- URL not captured — confirm from RapidAPI dashboard before implementing
- The "RapidAPI Response Body Size: 2 Bytes" is a known dashboard measurement artefact

---

## 63. GET * Analog Spare Parts by OEM

**Method:** GET
**Section:** Enhanced Article Search (`*` tier)
**Date tested:** 2026-04-13
**Response time:** — *(message truncated — metadata not captured)*
**Status:** 200 OK

**URL:**
```
TODO — message was truncated before metadata was captured. Confirm URL from RapidAPI dashboard.
```

> Note: RapidAPI dashboard name is **"Analog Spare Parts by OEM"** — stub was originally labelled "Cross-References by Article" based on a truncated screenshot.

---

### Response

```json
{
  "countArticles": 2849,
  "articles": [
    {
      "supplierName": "4X4 ESTANFI",
      "articleNo": "EST-MA-HY023",
      "crossManufacturerName": "HYUNDAI",
      "crossNumber": "553112L000",
      "searchLevel": "IAM->OEM     "
    },
    {
      "supplierName": "ASAM AUTOMOTIVE",
      "articleNo": "55074",
      "crossManufacturerName": "KIA",
      "crossNumber": "553112L000",
      "searchLevel": "IAM->OEM     "
    },
    {
      "supplierName": "4X4 ESTANFI",
      "articleNo": "EST-MA-HY023",
      "crossManufacturerName": "ASHIKA",
      "crossNumber": "MAHY023",
      "searchLevel": "IAM->OEM->IAM"
    },
    {
      "supplierName": "A.Z. Meisterteile",
      "articleNo": "AZMT-42-085-0639",
      "crossManufacturerName": "ACKOJA",
      "crossNumber": "A52-0895",
      "searchLevel": "IAM->OEM->IAM"
    }
  ]
}
```

*(Response truncated — 2849 total articles. Sample rows above show both `searchLevel` values.)*

---

### Response Fields

#### Top Level

| Field | Type | Description |
|-------|------|-------------|
| `countArticles` | int | Total number of rows returned |
| `articles` | array | List of analog article cross-reference rows |

#### `articles[]`

| Field | Type | Description |
|-------|------|-------------|
| `supplierName` | string | Aftermarket brand that makes the analog part |
| `articleNo` | string | Aftermarket article number for this analog part |
| `crossManufacturerName` | string | The OEM manufacturer name (e.g. `"HYUNDAI"`, `"KIA"`) or IAM brand this row is linked through |
| `crossNumber` | string | The OEM or IAM number this row is linked through |
| `searchLevel` | string | How the match was resolved — see table below |

#### `searchLevel` Values

| Value | Meaning |
|-------|---------|
| `"IAM->OEM     "` | Aftermarket (IAM) article linked directly to the searched OEM number. Trailing spaces are a TecDoc data artefact — trim before use |
| `"IAM->OEM->IAM"` | Aftermarket article linked to the searched OEM number, which then links to other aftermarket brands via shared OEM coverage |

---

### Notes

- **Input is an OEM number** (e.g. HYUNDAI `553112L000`) — this is the `*` tier equivalent of the standard OEM search, returning all aftermarket brands that make an analog for that OEM part
- **No `articleId` field** — unlike #62 (Analog by Article No), rows here have only `supplierName` + `articleNo`. To get `articleId` for downstream calls, must search by `supplierName + articleNo` via #19 or #24
- **`countArticles: 2849`** — extremely large result set for the tested OEM number. The same OEM number is used by both HYUNDAI and KIA (shared platform), multiplying the results
- **OEM number format variants present** — same physical part appears with different dash/space formatting: `"553112L000"`, `"55311-2L000"`, `"55311 2L000"`, `"55311-2L-000"`. TecDoc stores all variants; treat them as equivalent when deduplicating
- **`searchLevel` trailing spaces** — `"IAM->OEM     "` has 5 trailing spaces. Always `.strip()` / `.trim()` the value before comparison or display. Same pattern documented in [#53](#53-get-cross-references-through-oem-numbers-by-article-id)
- **One row per (supplier × OEM manufacturer) combination** — ASAM AUTOMOTIVE `55074` appears twice: once with `crossManufacturerName: "HYUNDAI"` and once with `"KIA"`. Deduplicate by `(supplierName, articleNo)` for a clean list of unique articles
- **`IAM->OEM->IAM` rows have `crossManufacturerName` = another IAM brand** — these are second-order cross-references (input OEM → shared OEM → other IAM brands). The `crossNumber` is another IAM brand's article number, not an OEM number
- **Structurally identical to [#53](#53-get-cross-references-through-oem-numbers-by-article-id)** — same fields, same `searchLevel` values, same trailing-space issue. Difference: #53 input is a TecDoc `articleId`, this endpoint takes an OEM number string directly
- **Kalaax use case:** OEM number search — user scans the OEM part number from their car manual or old part, enters it, and this returns all aftermarket brands that make a compatible replacement. Pair with #48 after resolving `articleId` for images
- URL not captured — confirm from RapidAPI dashboard before implementing
- The "RapidAPI Response Body Size: 2 Bytes" is a known dashboard measurement artefact

---

## 64. GET * Search Articles by Article No

> ⚠️ **DEPRECATED** — This endpoint is marked as deprecated in the RapidAPI dashboard. Do not use for new integrations. Documented for reference only.

**Method:** GET
**Section:** Enhanced Article Search (`*` tier)
**Date tested:** 2026-04-13
**Response time:** 1005 ms
**Status:** 200 OK

**URL:**
```
https://tecdoc-catalog.p.rapidapi.com/artlookup/search-articles-by-article-no/lang-id/{langId}/article-type/{articleType}/article-no/{articleNo}
```

**Path Params:**

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `langId` | int | Yes | Language ID — `4` = English |
| `articleType` | string | Yes | Search type — `"ArticleNumber"` for standard part number search |
| `articleNo` | string | Yes | Article/part number to search (URL-encoded — spaces as `%20`) |

**Example request:**
```
GET /artlookup/search-articles-by-article-no/lang-id/4/article-type/ArticleNumber/article-no/0%20242%20236%20561
```

---

### Response

```json
{
  "countArticles": 1,
  "articles": [
    {
      "articleSearchNo": "0 242 236 561",
      "articleId": 18068,
      "articleNo": "0 242 236 561",
      "articleProductName": "Spark Plug",
      "supplierName": "BOSCH",
      "supplierId": 30,
      "articleMediaType": "JPEG",
      "articleMediaFileName": "5a3c2f64ca542c51697df1749eea8e751ffcc2b3.webp"
    }
  ]
}
```

---

### Response Fields

#### Top Level

| Field | Type | Description |
|-------|------|-------------|
| `countArticles` | int | Total number of matched articles |
| `articles` | array | List of matched article objects |

#### `articles[]`

| Field | Type | Description |
|-------|------|-------------|
| `articleId` | int | TecDoc internal article ID — use for subsequent detail/media lookups |
| `articleNo` | string | Article number as stored in TecDoc |
| `articleSearchNo` | string | Article number as matched by the search — may include format variants |
| `articleProductName` | string | Generic product name (e.g. `"Spark Plug"`) |
| `supplierName` | string | Brand/supplier name (e.g. `"BOSCH"`) |
| `supplierId` | int | Supplier ID — use with media filename to construct S3 URL |
| `articleMediaType` | string | Media type of the primary image (`"JPEG"`, `"PNG"`, `"GIF"`, `"PDF"`) |
| `articleMediaFileName` | string | SHA-1 content-addressed filename — construct S3 URL as `media_files/images/{supplierId}/{filename}.webp` |

---

### Notes

- **DEPRECATED** — do not build new features against this endpoint. It is present in the RapidAPI dashboard but marked deprecated; it may be removed without notice
- Response structure is identical to [#19 GET Search Articles by Article No](#19-get-search-articles-by-article-no) — same fields, same shape
- The `artlookup/` URL prefix distinguishes this from the standard `/articles/` prefix used in the non-enhanced tier
- `articleMediaType: "JPEG"` → file extension in response is `.webp` (TecDoc stores JPEG originals re-encoded as WebP) — same conversion pattern as all other media endpoints
- `articleSearchNo` may differ from `articleNo` when the search matched a format variant — always use `articleId` as the canonical identifier for downstream calls
- For new integrations use [#19 GET Search Articles by Article No](#19-get-search-articles-by-article-no) (standard tier) or the `**` tier equivalents (#65, #68) instead
- The "RapidAPI Response Body Size: 2 Bytes" is a known dashboard measurement artefact

---

## 65. GET * OEM/OEM Cross-Reference through Aftermarket Parts

**Method:** GET
**Section:** Enhanced Article Search (`*` tier)
**Date tested:** 2026-04-13
**Response time:** 1364 ms
**Status:** 200 OK

**URL:**
```
https://tecdoc-catalog.p.rapidapi.com/artlookup/search-for-the-oem-cross-references-through-aftermarket-parts-references/article-oem-no/{oemNo}
```

**Path Params:**

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `oemNo` | string | Yes | OEM part number to look up (URL-encode special characters) |

**Example request:**
```
GET /artlookup/search-for-the-oem-cross-references-through-aftermarket-parts-references/article-oem-no/4853009T50
```

---

### Response

```json
{
  "countArticles": 289,
  "articles": [
    {
      "crossManufacturerName": "HITACHI",
      "crossNumber": "2006805"
    },
    {
      "crossManufacturerName": "LEXUS",
      "crossNumber": "48530-02490"
    },
    {
      "crossManufacturerName": "NISSAN",
      "crossNumber": "4853009W10"
    },
    {
      "crossManufacturerName": "SACHS",
      "crossNumber": "314890"
    },
    {
      "crossManufacturerName": "SCION",
      "crossNumber": "48530-12E10"
    },
    {
      "crossManufacturerName": "TOYOTA",
      "crossNumber": "48530-09T50"
    },
    {
      "crossManufacturerName": "TOYOTA (FAW)",
      "crossNumber": "4853009R30"
    },
    {
      "crossManufacturerName": "METACO",
      "crossNumber": "4820-123"
    }
  ]
}
```

*(289 total rows — sample rows above show all manufacturer types present)*

---

### Response Fields

#### Top Level

| Field | Type | Description |
|-------|------|-------------|
| `countArticles` | int | Total number of OEM cross-reference rows |
| `articles` | array | List of OEM cross-reference objects |

#### `articles[]`

| Field | Type | Description |
|-------|------|-------------|
| `crossManufacturerName` | string | OEM or premium brand manufacturer name |
| `crossNumber` | string | The equivalent part number from that manufacturer |

> Only two fields per row — no `supplierName`, `articleId`, `articleNo`, `searchLevel`, or `foundVia`.

---

### Notes

- **Pure OEM-to-OEM cross-reference** — input is one OEM number, output is all other OEM numbers from all manufacturers that are equivalent, discovered by tracing through shared aftermarket (IAM) article links. No aftermarket data appears in the response
- **Manufacturers present in test response:** TOYOTA, TOYOTA (FAW), LEXUS, NISSAN, SCION, HITACHI, SACHS, METACO — both vehicle OEMs (TOYOTA, NISSAN) and premium/aftermarket brands (SACHS, HITACHI) appear as OEM cross-references
- **`TOYOTA (FAW)`** — First Automobile Works joint venture, builds Toyota models in China. Relevant for Egyptian market where Chinese-built Toyotas are imported
- **Data quality issue — scientific notation corruption:** Two rows have `crossNumber: "4.853E+16"` and `"4.853E+36"` — these are part numbers that were corrupted into Excel-style scientific notation in the upstream TecDoc database. Treat any `crossNumber` matching `^\d+\.\d+E\+\d+$` as invalid and filter out before display
- **OEM number format variants present** — same physical part has both hyphenated (`"48530-09T50"`) and compact (`"4853009T50"`) format entries. Both are valid and should be included when storing
- **289 rows for a single shock absorber OEM number** — TOYOTA/LEXUS/SCION shared platforms create many part number supersessions and variants across model years
- **Completely different from #51 GET Equivalent OEM Numbers** — #51 takes a `articleId` and returns OEM numbers for that article. This endpoint takes an OEM number and returns ALL cross-OEM equivalents discovered through the IAM network. Use this when you have an OEM number but no `articleId`
- **Kalaax use case:** When a customer provides a dealer (OEM) part number, use this to find all equivalent OEM numbers across related manufacturers — useful for verifying part compatibility across brand-shared platforms (e.g. Toyota/Lexus) before showing aftermarket alternatives from #63
- The "RapidAPI Response Body Size: 2 Bytes" is a known dashboard measurement artefact

---

## 66. GET ** Search Articles by OEM

**Method:** GET
**Section:** Enhanced Article Search (`articles-oem/` prefix)
**Date tested:** 2026-04-13
**Response time:** (truncated — not captured)
**Status:** 200 OK

**URL:**
```
TODO — message was truncated before metadata was captured. Likely:
https://tecdoc-catalog.p.rapidapi.com/articles-oem/search-by-oem-no?langId={langId}&oemNo={oemNo}
(confirm from RapidAPI dashboard)
```

**Query Params:**

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `langId` | int | Yes | Language ID — `4` = English |
| `oemNo` | string | Yes | OEM part number to search (URL-encode spaces) |

**Example request (OEM tested):**
```
GET /articles-oem/search-by-oem-no?langId=4&oemNo=8F0+513+035+N
OEM: Audi shock absorber 8F0 513 035 N
```

---

### Response Structure

**Flat JSON array** — no `countArticles` wrapper. Iterate directly over the returned array.

```json
[
  {
    "articleId": 976428,
    "articleSearchNo": "8F0 513 035 N",
    "articleNo": "11-0488",
    "articleProductName": "Shock Absorber",
    "manufacturerId": 5,
    "manufacturerName": "AUDI",
    "supplierId": 403,
    "supplierName": "MAXGEAR",
    "articleMediaType": "JPEG",
    "articleMediaFileName": "5275bb6966d882f35bff5ebb9044991a48932406.webp",
    "s3image": "https://fsn1.your-objectstorage.com/tecdoc2025/media_files/images/403/5275bb6966d882f35bff5ebb9044991a48932406.webp"
  }
]
```

### Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `articleId` | int | TecDoc internal article ID |
| `articleSearchNo` | string | The OEM number as matched — may appear with spaces (`"8F0 513 035 N"`) or compact (`"8F0513035N"`) in the same response |
| `articleNo` | string | Aftermarket supplier's own part number (e.g. `"11-0488"`) |
| `articleProductName` | string | Part category/name (e.g. `"Shock Absorber"`) |
| `manufacturerId` | int | TecDoc OEM manufacturer ID — e.g. `5` = AUDI |
| `manufacturerName` | string | OEM brand name (e.g. `"AUDI"`) — **unique to this endpoint**, not present in most others |
| `supplierId` | int | TecDoc aftermarket supplier ID |
| `supplierName` | string | Aftermarket supplier brand name (e.g. `"MAXGEAR"`, `"BILSTEIN"`) |
| `articleMediaType` | string | Image format — `"JPEG"` or `"JPG"` (inconsistent across rows — normalize on ingest) |
| `articleMediaFileName` | string | Image filename used to construct S3 URL |
| `s3image` | string | Full S3 URL to article image |

### S3 Image URL Pattern

```
https://fsn1.your-objectstorage.com/tecdoc2025/media_files/images/{supplierId}/{articleMediaFileName}
```

### Multiple Rows Per Article (Image Expansion)

One article with N images = **N rows** sharing the same `articleId` but different `articleMediaFileName` and `s3image`.

When persisting to DB: group by `articleId`, collect all `s3image` values into an image gallery array.

```python
from itertools import groupby

articles = {}
for row in response_array:
    aid = row["articleId"]
    if aid not in articles:
        articles[aid] = {**row, "images": []}
    articles[aid]["images"].append(row["s3image"])
```

### Key Notes

- **`articleSearchNo` format**: OEM numbers appear with spaces (`"8F0 513 035 N"`) AND compact (`"8F0513035N"`) in the same response. Both represent the same OEM number under different matching patterns. Normalize for storage: strip spaces before indexing.
- **`manufacturerId` / `manufacturerName`**: OEM brand fields — unique to this endpoint (and #69). Most other endpoints do not return the OEM brand identity alongside the matched article.
- **`articleMediaType` normalization**: `"JPEG"` and `"JPG"` appear inconsistently across rows from the same request. Always normalize: `media_type.upper().replace("JPEG", "JPG")` or similar.
- **No `countArticles` field**: Unlike #61, #71 which wrap the response, this endpoint returns a raw array. Use `len(response)` / `response.length` — not `.countArticles`.
- **Large result sets**: A single common OEM number (e.g. Audi shock absorber) returns 200+ rows from dozens of aftermarket suppliers. Apply supplier filtering or pagination on the client side.
- **Supplier brands observed in test**: MAXGEAR, BILSTEIN, SACHS, KYB, KONI, RIDEX, OPTIMAL, JAPKO, JAPANPARTS, Stark, KAVO PARTS, AP XENERGY, RED-LINE, DENCKERMANN, MOOG, MONROE, LESJÖFORS, and many others.
- **URL missing**: Message was truncated at 50k chars before metadata was captured. Confirm the exact URL path from RapidAPI dashboard.

### Comparison: #20 vs #66

| Feature | #20 GET Search Articles by OEM No | #66 GET ** Search Articles by OEM |
|---------|-----------------------------------|-----------------------------------|
| Tier | Standard | Enhanced (`**`) |
| OEM brand field | No | Yes (`manufacturerId`, `manufacturerName`) |
| Media included | No | Yes (S3 image URL per row) |
| Response wrapper | Object `{countArticles, articles}` | Flat array `[...]` |
| Article No included | No | Yes (`articleNo`) |

---

## 67. POST ** Search Articles by OEM

**Method:** POST
**Section:** Enhanced Article Search (`articles-oem/` prefix)
**Date tested:** 2026-04-13
**Response time:** (truncated — not captured)
**Status:** 200 OK

**URL:**
```
TODO — message was truncated before metadata was captured. Likely:
https://tecdoc-catalog.p.rapidapi.com/articles-oem/search-by-oem-no
(confirm from RapidAPI dashboard)
```

**Request Body:**

```json
{
  "langId": 4,
  "oemNo": "8F0 513 035 N"
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `langId` | int | Yes | Language ID — `4` = English |
| `oemNo` | string | Yes | OEM part number to search |

**Example request (OEM tested):**
```
POST /articles-oem/search-by-oem-no
Body: {"langId": 4, "oemNo": "8F0 513 035 N"}
OEM: Audi shock absorber 8F0 513 035 N
```

---

### Response Structure

**Identical to [#66 GET ** Search Articles by OEM](#66-get--search-articles-by-oem)** — flat JSON array, no `countArticles` wrapper.

```json
[
  {
    "articleId": 976428,
    "articleSearchNo": "8F0 513 035 N",
    "articleNo": "11-0488",
    "articleProductName": "Shock Absorber",
    "manufacturerId": 5,
    "manufacturerName": "AUDI",
    "supplierId": 403,
    "supplierName": "MAXGEAR",
    "articleMediaType": "JPEG",
    "articleMediaFileName": "5275bb6966d882f35bff5ebb9044991a48932406.webp",
    "s3image": "https://fsn1.your-objectstorage.com/tecdoc2025/media_files/images/403/5275bb6966d882f35bff5ebb9044991a48932406.webp"
  }
]
```

The response structure, fields, and behaviour are identical to #66. See [#66 Response Fields](#66-get--search-articles-by-oem) for full field documentation.

### GET (#66) vs POST (#67) Comparison

| Feature | #66 GET | #67 POST |
|---------|---------|---------|
| OEM input | Query param (`?oemNo=`) | Request body JSON (`{"oemNo": "..."}`) |
| Response structure | Flat array | Flat array (identical) |
| Fields returned | All 11 fields | All 11 fields (identical) |
| Use case | Simple OEM lookups | OEM numbers with special characters that break URL encoding |

### Key Notes

- **Same response as #66**: Tested with the same OEM (`8F0 513 035 N`) — identical result set returned. Both endpoints are interchangeable for standard OEM numbers.
- **POST preference**: Use POST when OEM numbers contain characters like `/`, `+`, `#`, or long strings that may cause URL length/encoding issues.
- **URL missing**: Message truncated at 50k chars before metadata was captured. Confirm the exact URL and request body schema from RapidAPI dashboard.
- All notes from #66 apply: flat array, image expansion rows, `articleMediaType` normalization, `manufacturerId`/`manufacturerName` OEM brand fields.

---

## 68. GET ** Search Articles by Article No

**Method:** GET
**Section:** Article Search (`articles/` prefix)
**Date tested:** 2026-04-13
**Response time:** 1014 ms
**Status:** 200 OK

**URL:**
```
https://tecdoc-catalog.p.rapidapi.com/articles/search-by-article-no?langId={langId}&articleNo={articleNo}
```

**Query Params:**

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `langId` | int | Yes | Language ID — `4` = English |
| `articleNo` | string | Yes | Article/part number to search (URL-encode spaces as `+`) |

**Example request:**
```
GET /articles/search-by-article-no?langId=4&articleNo=C+2029
```

---

### Response

```json
{
  "articleNo": "C 2029",
  "countArticles": 1,
  "articles": [
    {
      "articleId": 6159438,
      "articleNo": "C 2029",
      "articleProductName": "Air Filter",
      "supplierName": "MANN-FILTER",
      "supplierId": 4,
      "articleMediaType": "JPG",
      "articleMediaFileName": "5e27f118885fa0253374358b3585240c6c9a53af.webp",
      "s3image": "https://fsn1.your-objectstorage.com/tecdoc2025/media_files/images/4/5e27f118885fa0253374358b3585240c6c9a53af.webp"
    }
  ]
}
```

---

### Response Fields

#### Top Level

| Field | Type | Description |
|-------|------|-------------|
| `articleNo` | string | The queried article number — mirrors the `articleNo` query param |
| `countArticles` | int | Number of articles matched |
| `articles` | array | List of matched article objects |

#### `articles[]`

| Field | Type | Description |
|-------|------|-------------|
| `articleId` | int | TecDoc internal article ID — use for media, detail, OEM, and fitment lookups |
| `articleNo` | string | Article number as stored in TecDoc |
| `articleProductName` | string | Generic product category name (e.g. `"Air Filter"`) |
| `supplierName` | string | Brand/supplier name (e.g. `"MANN-FILTER"`) |
| `supplierId` | int | Supplier ID — use with `articleMediaFileName` to construct S3 URL |
| `articleMediaType` | string | Media type of primary image — `"JPG"` in test (same as #72; other endpoints use `"JPEG"`) |
| `articleMediaFileName` | string | SHA-1 content-addressed filename |
| `s3image` | string | **Direct S3 image URL** — full URL ready to use |

---

### Notes

- **Lightest article-number search endpoint** — returns only identity + image per article. No specs, OEM numbers, compatible vehicles, or article info. Use when you need just the article ID and thumbnail for a search results list
- **`s3image` is a ready-to-use direct URL** — same pattern as #71: `https://fsn1.your-objectstorage.com/tecdoc2025/media_files/images/{supplierId}/{filename}.webp`. No construction needed
- **No path params, no `typeId`, no `countryFilterId`** — simpler URL than #61 and #71. The search is not filtered by vehicle type or country market
- **Top-level `articleNo` field** mirrors the query param — same pattern as #71. Confirms the search term that was used
- **Compared to other article-number search endpoints:**
  - [#19 GET Search Articles by Article No](#19-get-search-articles-by-article-no) — standard tier, returns `articleSearchNo` + `articleId` + supplier + media filename (no `s3image`). Similar scope
  - [#64 GET * Search Articles by Article No ⚠️ DEPRECATED](#64-get--search-articles-by-article-no) — `artlookup/` prefix, deprecated, same basic fields but different URL family
  - [#71 GET * Article Details by Article No](#71-get--article-details-by-article-no) — same `articles/` prefix but much richer: adds specs, EAN, OEM numbers, compatible vehicles. Use #71 for the product detail page; use this (#68) for lightweight search results
- **`articleMediaType: "JPG"`** — normalize with #72's note: both `"JPG"` and `"JPEG"` appear across endpoints for the same underlying JPEG-encoded WebP files
- **Kalaax use case:** Fast article number lookup for search results page — returns enough to display a product card (name, brand, thumbnail). Follow up with [#71](#71-get--article-details-by-article-no) when the user taps a result to get the full product detail
- The "RapidAPI Response Body Size: 2 Bytes" is a known dashboard measurement artefact

---

## 69. GET * OEM Parts by Vehicle ID

**Method:** GET
**Section:** Enhanced Article Search (`*` tier)
**Date tested:** 2026-04-13
**Response time:** TODO — message truncated before metadata was captured
**Status:** 200 OK

**URL:**
```
TODO — URL was not captured (message truncated at 50k chars). Confirm from RapidAPI dashboard.
```

**Path Params:**

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `vehicleId` | int | Yes | TecDoc vehicle ID — obtain from [#14 GET Vehicle IDs by Model ID](#14-get-vehicle-ids-by-model-id) |

**Example request:**
```
GET /artlookup/{vehicleId}/oem-parts   (exact path TBD)
```

---

### Response

```json
[
  {
    "articleOemNo": "00834126",
    "articleProductName": "Air Filter"
  },
  {
    "articleOemNo": "00650652",
    "articleProductName": "Cap"
  },
  {
    "articleOemNo": "1808076",
    "articleProductName": "Engine Oil"
  },
  {
    "articleOemNo": "93165562",
    "articleProductName": "Filter Set"
  },
  {
    "articleOemNo": "13271585",
    "articleProductName": "Filter (Cabin air)"
  },
  {
    "articleOemNo": "55566017",
    "articleProductName": "Fuel Filter"
  },
  {
    "articleOemNo": "55593766",
    "articleProductName": "Housing"
  },
  {
    "articleOemNo": "55597259",
    "articleProductName": "Oil Filter"
  },
  {
    "articleOemNo": "55591218",
    "articleProductName": "Oil filter module"
  },
  {
    "articleOemNo": "55567258",
    "articleProductName": "Oil Separator"
  }
]
```

*(Flat array — no top-level wrapper object. Test vehicle was likely a Vauxhall/Opel based on OEM number patterns. Full response truncated — actual array length unknown.)*

---

### Response Fields

> **Top-level structure is a flat JSON array — no `countArticles`, no `articles` wrapper.** This is structurally unique compared to all other endpoints in this doc which return `{ countArticles, articles: [...] }`.

#### Array item fields

| Field | Type | Description |
|-------|------|-------------|
| `articleOemNo` | string | OEM part number for this vehicle |
| `articleProductName` | string | Generic product/category name (e.g. `"Air Filter"`, `"Oil Filter"`) |

---

### Product Categories Seen in Test Response

| `articleProductName` |
|----------------------|
| Air Filter |
| Cap (oil filter housing) |
| Engine Oil |
| Filter Set |
| Filter (Cabin air) |
| Fuel Filter |
| Holder (air filter housing) |
| Housing (air filter / oil filter) |
| Hydraulic Filter |
| Mounting Kit (soot filter) |
| Oil Filter |
| Oil filter module |
| Oil Separator |
| Soot/Particulate Filter Cleaning |

---

### Notes

- **Flat array response — unique structure:** Every other endpoint returns `{ "countArticles": N, "articles": [...] }`. This endpoint returns a bare `[...]` array with no wrapper object. Do not attempt to access `.countArticles` or `.articles` — iterate the array directly
- **OEM number patterns in test:** `00xxxxxx`, `650xxx`, `834xxx`, `1808xxx`, `13xxxxxx`, `55xxxxxx` series — consistent with Vauxhall/Opel (GM Europe) part number formats. The test vehicle was likely an Opel/Vauxhall model
- **Only two fields per item** — no `articleId`, `supplierId`, `supplierName`, `mediaFileName`, or any other field. This endpoint provides OEM numbers only; use the OEM number with [#63 GET * Analog Spare Parts by OEM](#63-get--analog-spare-parts-by-oem) or [#65 GET * OEM/OEM Cross-Reference through Aftermarket Parts](#65-get--oemoemcross-reference-through-aftermarket-parts) to find aftermarket alternatives or equivalent OEM numbers from other brands
- **`articleProductName` is a generic category label**, not a brand-specific product name — suitable for display as a category grouping in UI (e.g. group all `"Oil Filter"` OEM numbers under one card)
- **Kalaax use case:** After vehicle selection, call this endpoint to get the full list of OEM part numbers for that vehicle. Use those OEM numbers to pre-populate "OEM parts for your vehicle" sections, or cross-reference against the parts catalog for available aftermarket alternatives via #63
- **URL and response time are missing** — the RapidAPI response message was truncated at 50k characters before the metadata section was reached. Confirm the exact URL path from the RapidAPI dashboard and re-test to get response time

---

## 70. GET * List Vehicles by OEM

**Method:** GET
**Section:** OEM Articles (`articles-oem/` prefix)
**Date tested:** 2026-04-13
**Response time:** 1231 ms
**Status:** 200 OK

**URL:**
```
https://tecdoc-catalog.p.rapidapi.com/articles-oem/selecting-a-list-of-cars-for-oem-part-number/type-id/{typeId}/lang-id/{langId}/country-filter-id/{countryId}/manufacturer-id/{manufacturerId}/article-oem-no/{oemNo}
```

**Path Params:**

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `typeId` | int | Yes | Vehicle type ID — `1` = passenger car (same as #5/#6) |
| `langId` | int | Yes | Language ID — `4` = English |
| `countryId` | int | Yes | Country filter ID — narrows results to vehicles sold in that market. `63` = France in test |
| `manufacturerId` | int | Yes | Manufacturer ID — filters results to one brand. `93` = Renault in test |
| `oemNo` | string | Yes | OEM part number to look up (URL-encode special characters) |

**Example request:**
```
GET /articles-oem/selecting-a-list-of-cars-for-oem-part-number/type-id/1/lang-id/4/country-filter-id/63/manufacturer-id/93/article-oem-no/7700115294
```

---

### Response

```json
[
  {
    "manufacturerName": "RENAULT",
    "modelName": "SCÉNIC I MPV (JA0/1_, FA0_)",
    "typeEngineName": "2.0 16V (JA1D, JA17)",
    "bodyType": "MPV",
    "constructionIntervalStart": "1999-09-01",
    "constructionIntervalEnd": "2003-08-01",
    "powerKw": "103.0000",
    "powerPs": "140.0000",
    "capacityTax": "1998.0000"
  },
  {
    "manufacturerName": "RENAULT",
    "modelName": "LAGUNA II (BG0/1_)",
    "typeEngineName": "1.8 16V (BG0B, BG0C, BG0J, BG0M, BG0V)",
    "bodyType": "Hatchback",
    "constructionIntervalStart": "2001-03-01",
    "constructionIntervalEnd": "2005-05-01",
    "powerKw": "89.0000",
    "powerPs": "121.0000",
    "capacityTax": "1783.0000"
  },
  {
    "manufacturerName": "RENAULT",
    "modelName": "TRAFIC II Bus (JL)",
    "typeEngineName": "2.0 (JL0A, JL0G)",
    "bodyType": "Bus",
    "constructionIntervalStart": "2001-03-01",
    "constructionIntervalEnd": null,
    "powerKw": "88.0000",
    "powerPs": "120.0000",
    "capacityTax": "1998.0000"
  },
  {
    "manufacturerName": "RENAULT",
    "modelName": "DUSTER (HS_)",
    "typeEngineName": "2.0 4x4",
    "bodyType": "SUV",
    "constructionIntervalStart": "2011-10-01",
    "constructionIntervalEnd": null,
    "powerKw": "105.0000",
    "powerPs": "142.0000",
    "capacityTax": null
  }
]
```

*(Flat array — ~100+ rows in full response. All RENAULT because `manufacturer-id/93` filtered results. Sample rows above show variety of body types, power outputs, and null values.)*

---

### Response Fields

> **Top-level structure is a flat JSON array — no `countArticles` or `articles` wrapper.** Iterate the array directly.

#### Array item fields

| Field | Type | Nullable | Description |
|-------|------|----------|-------------|
| `manufacturerName` | string | No | Brand name — always matches the `manufacturerId` filter (e.g. `"RENAULT"` for `manufacturer-id/93`) |
| `modelName` | string | No | Model name including body style variant code in parentheses (e.g. `"SCÉNIC I MPV (JA0/1_, FA0_)"`) |
| `typeEngineName` | string | No | Engine/trim variant label including engine codes (e.g. `"2.0 16V (JA1D, JA17)"`) |
| `bodyType` | string | No | Body style category — see values table below |
| `constructionIntervalStart` | string | No | Production start date — ISO `"YYYY-MM-DD"` format |
| `constructionIntervalEnd` | string | Yes | Production end date — ISO `"YYYY-MM-DD"` or `null` if model still in production |
| `powerKw` | string | No | Engine power in kilowatts — decimal string (e.g. `"103.0000"`) — parse with `parseFloat()` and display as integer |
| `powerPs` | string | No | Engine power in metric horsepower (PS) — decimal string (e.g. `"140.0000"`) — parse with `parseFloat()` and display as integer |
| `capacityTax` | string | Yes | Engine displacement in cc — decimal string (e.g. `"1998.0000"`) or `null` when TecDoc has no data for that variant |

#### `bodyType` values seen in test

| Value | Description |
|-------|-------------|
| `"Hatchback"` | 3- or 5-door hatchback |
| `"MPV"` | Multi-purpose vehicle / minivan |
| `"Estate"` | Station wagon |
| `"Saloon"` | 4-door sedan |
| `"Coupe"` | 2-door coupe |
| `"Convertible"` | Cabriolet / open-top |
| `"SUV"` | Sport utility vehicle |
| `"Van"` | Commercial van |
| `"Bus"` | Minibus / passenger bus |
| `"Platform/Chassis"` | Chassis cab without body |
| `"Estate Van"` | Commercial estate van |

---

### Notes

- **Flat array — no wrapper:** Same pattern as #69. Do not attempt `.countArticles`. Iterate directly. Count with `array.length`
- **`manufacturer-id` is required and acts as a mandatory filter** — the response only contains vehicles from the specified manufacturer. To find all compatible vehicles across all brands, you must either: call once per manufacturer, or omit the filter if the API supports it (not tested)
- **`country-filter-id` narrows results to vehicles sold in that market** — set to the country ID of your target market. For Kalaax (Egypt), find the Egypt country ID via [#2 GET Countries](#2-get-countries) and use it here. Test used `63` (France) because the OEM number `7700115294` is a French-market Renault part
- **Power and displacement are decimal strings, not numbers** — `"103.0000"` must be parsed with `parseFloat()`. Round or floor to integer for display: `Math.floor(parseFloat(powerKw))` → `103`
- **`capacityTax: null`** means TecDoc has no engine displacement data for that specific variant. This is common for post-2002 vehicles where the data field was phased out — `powerKw`/`powerPs` are always populated
- **`constructionIntervalEnd: null`** means the model is still in production or the end date is unknown in TecDoc. Treat as "currently available" in UI
- **`modelName` contains TecDoc internal model range codes** in parentheses (e.g. `"JA0/1_, FA0_"`) — these are TecDoc model group identifiers, not user-visible codes. Display only the human-readable prefix before the `(` if needed
- **`typeEngineName` contains TecDoc type codes** in parentheses (e.g. `"JA1D, JA17"`) — same pattern. Display the engine size label only (e.g. `"2.0 16V"`) by trimming the parenthesised codes
- **Special characters in model names** — `SCÉNIC`, `COUPÉ-CABRIOLET` — store as-is (UTF-8). Do not ASCII-encode
- **Different from #43 GET Compatible Vehicles by Article No & Supplier ID** — #43 takes an article number + supplier ID (aftermarket part) and returns TecDoc vehicle IDs. This endpoint (#70) takes an OEM part number and returns human-readable vehicle descriptions with no `vehicleId` field — useful for display only, not for further parts lookup
- **No `vehicleId` in response** — cannot chain this into parts lookup. If `vehicleId` is needed for a matched vehicle, use the `modelName` + `typeEngineName` to search via [#8 GET Models by Type & Manufacturer](#8-get-models-by-type--manufacturer) → [#14 GET Vehicle IDs by Model ID](#14-get-vehicle-ids-by-model-id)
- **URL prefix `articles-oem/`** distinguishes this from the `artlookup/` Enhanced tier — this is a separate API family
- **Kalaax use case:** On the product detail page for an article found via OEM number search, show "Compatible with these vehicles" — call this endpoint with the OEM number and filter by the user's target manufacturer to show a fitment list. Group by `modelName` for a cleaner display
- The "RapidAPI Response Body Size: 2 Bytes" is a known dashboard measurement artefact

---

## 71. GET * Article Details by Article No

**Method:** GET
**Section:** Article Details (`articles/` prefix)
**Date tested:** 2026-04-13
**Response time:** 1129 ms
**Status:** 200 OK

**URL:**
```
https://tecdoc-catalog.p.rapidapi.com/articles/article-number-details/type-id/{typeId}?langId={langId}&countryFilterId={countryId}&articleNo={articleNo}
```

**Path Params:**

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `typeId` | int | Yes | Vehicle type ID — `1` = passenger car |

**Query Params:**

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `langId` | int | Yes | Language ID — `4` = English |
| `countryFilterId` | int | Yes | Country filter ID — filters compatible vehicle list to a market. `63` = France in test |
| `articleNo` | string | Yes | Article/part number — URL-encode special characters |

**Example request:**
```
GET /articles/article-number-details/type-id/1?langId=4&countryFilterId=63&articleNo=002-001-000001R
```

---

### Response

```json
{
  "articleNo": "002-001-000001R",
  "countArticles": 2,
  "articles": [
    {
      "articleId": 131540,
      "articleNo": "002-001-000001R",
      "articleProductName": "Injection Pump",
      "supplierName": "REMANTE",
      "supplierId": 814,
      "articleMediaType": "JPEG",
      "articleMediaFileName": "a87fb8344298bbf9babc7be7c284fef7bd75cac3.webp",
      "articleInfo": {
        "articleId": 131540,
        "articleNo": "002-001-000001R",
        "supplierId": 814,
        "supplierName": "REMANTE",
        "isAccessory": 0,
        "articleProductName": "Injection Pump"
      },
      "allSpecifications": [
        { "criteriaName": "Weight [kg]", "criteriaValue": "9,20" },
        { "criteriaName": "Fuel Type", "criteriaValue": "5" },
        { "criteriaName": "Exchange Part", "criteriaValue": "" },
        { "criteriaName": "Guarantee", "criteriaValue": "2" },
        { "criteriaName": "Generally overhauled", "criteriaValue": "" }
      ],
      "eanNo": {
        "eanNumbers": "08595706500449"
      },
      "oemNo": [
        { "oemBrand": "VW", "oemDisplayNo": "059 130 105 A" },
        { "oemBrand": "VW", "oemDisplayNo": "059 130 106 A" },
        { "oemBrand": "VAG", "oemDisplayNo": "059 130 106 DX" }
      ],
      "compatibleCars": [
        {
          "vehicleId": 7742,
          "modelId": 265,
          "manufacturerName": "AUDI",
          "modelName": "A8 D2 (4D2, 4D8)",
          "typeEngineName": "2.5 TDI",
          "constructionIntervalStart": "1997-01-01",
          "constructionIntervalEnd": "2000-04-01"
        }
      ],
      "s3image": "https://fsn1.your-objectstorage.com/tecdoc2025/media_files/images/814/a87fb8344298bbf9babc7be7c284fef7bd75cac3.webp"
    }
  ]
}
```

*(Test returned `countArticles: 2` — two TecDoc supplier records for the same article number `002-001-000001R`, both REMANTE brand but with different `supplierId` (814 and 4392). Full `compatibleCars` list had 18 vehicles — truncated above to one example.)*

---

### Response Fields

#### Top Level

| Field | Type | Description |
|-------|------|-------------|
| `articleNo` | string | The queried article number — mirrors the `articleNo` query param |
| `countArticles` | int | Number of TecDoc records found for this article number (can be >1 when same part number exists under multiple supplier IDs) |
| `articles` | array | List of matched article records — each is a full article bundle |

#### `articles[]`

| Field | Type | Description |
|-------|------|-------------|
| `articleId` | int | TecDoc internal article ID — use for media, OEM, and fitment lookups |
| `articleNo` | string | Article number as stored in TecDoc |
| `articleProductName` | string | Generic product category name (e.g. `"Injection Pump"`) |
| `supplierName` | string | Brand/supplier name |
| `supplierId` | int | Supplier ID — used in S3 URL construction |
| `articleMediaType` | string | Media type of primary image (`"JPEG"`, `"PNG"`, etc.) |
| `articleMediaFileName` | string | SHA-1 content-addressed filename — use to construct S3 URL or read from `s3image` directly |
| `articleInfo` | object | Nested copy of core article identity fields — see below |
| `allSpecifications` | array | Technical specification key-value pairs — see below |
| `eanNo` | object | EAN barcode number — see below |
| `oemNo` | array | OEM cross-reference numbers by brand — see below |
| `compatibleCars` | array | Compatible vehicle fitment list — same structure as [#61](#61-get--compatible-vehicles-by-article-no) |
| `s3image` | string | **Direct S3 image URL** — full URL ready to use, no construction needed |

#### `articles[].articleInfo`

Nested duplicate of core article identity. Fields are a subset of the parent article object.

| Field | Type | Description |
|-------|------|-------------|
| `articleId` | int | Same as parent `articleId` |
| `articleNo` | string | Same as parent `articleNo` |
| `supplierId` | int | Same as parent `supplierId` |
| `supplierName` | string | Same as parent `supplierName` |
| `isAccessory` | int | `0` = primary part, `1` = accessory/add-on part |
| `articleProductName` | string | Same as parent `articleProductName` |

#### `articles[].allSpecifications[]`

| Field | Type | Description |
|-------|------|-------------|
| `criteriaName` | string | Human-readable spec label (e.g. `"Weight [kg]"`, `"Fuel Type"`, `"Guarantee"`) |
| `criteriaValue` | string | Spec value — may be empty string `""` when TecDoc has no data for that criteria |

> **Note:** `criteriaValue` uses a comma as decimal separator (e.g. `"9,20"` = 9.20 kg) — this is European locale formatting. Parse with `.replace(',', '.')` before converting to float.

> **Note:** `"Fuel Type": "5"` is a TecDoc internal criteria ID, not a human-readable label — would require a criteria value lookup table to decode.

#### `articles[].eanNo`

| Field | Type | Description |
|-------|------|-------------|
| `eanNumbers` | string | EAN barcode — despite the plural name, this is a single string |

> **Data quality:** Two records for the same article returned different EAN strings: `"08595706500449"` (14 chars with leading zero) and `"8595706500449"` (13 chars standard EAN-13). Both represent the same barcode — the leading zero is spurious. Normalize to EAN-13 by trimming leading zeros: `eanNumbers.replace(/^0+/, '')`.

#### `articles[].oemNo[]`

| Field | Type | Description |
|-------|------|-------------|
| `oemBrand` | string | OEM manufacturer brand (e.g. `"VW"`, `"VAG"`) |
| `oemDisplayNo` | string | Human-formatted OEM number with spaces/hyphens for display (e.g. `"059 130 106 A"`) |

> `"VAG"` = Volkswagen AG — the parent company brand used on shared platform parts across VW, Audi, SEAT, Škoda. Both `"VW"` and `"VAG"` may appear for the same physical part.

#### `articles[].compatibleCars[]`

Identical structure to the `compatibleCars` field in [#61 GET * Compatible Vehicles by Article No](#61-get--compatible-vehicles-by-article-no):

| Field | Type | Nullable | Description |
|-------|------|----------|-------------|
| `vehicleId` | int | No | TecDoc vehicle ID — use in vehicle-gated parts lookups |
| `modelId` | int | No | TecDoc model ID |
| `manufacturerName` | string | No | Brand name |
| `modelName` | string | No | Model name with TecDoc range code |
| `typeEngineName` | string | No | Engine/trim variant |
| `constructionIntervalStart` | string | No | Production start — ISO `"YYYY-MM-DD"` |
| `constructionIntervalEnd` | string | Yes | Production end — ISO `"YYYY-MM-DD"` or `null` |

---

### Notes

- **All-in-one article detail bundle** — this is the most comprehensive article-by-number endpoint in the catalog. A single call returns: article identity, media filename + direct S3 URL, full specifications, EAN barcode, OEM cross-references, and complete compatible vehicle fitment list. Compare with [#24 POST Article Details by Article No](#24-post-article-details-by-article-no) which returns lighter data
- **`s3image` is a ready-to-use direct URL** — format: `https://fsn1.your-objectstorage.com/tecdoc2025/media_files/images/{supplierId}/{filename}.webp`. Unlike other endpoints that give `articleMediaFileName` and require you to construct the URL, this gives the full URL. Host `fsn1.your-objectstorage.com/tecdoc2025` is the TecDoc S3-compatible object storage. Treat as the canonical image source for this endpoint
- **`countArticles` can be >1 for the same article number** — the test returned 2 records for `002-001-000001R`: `supplierId` 814 and 4392, both REMANTE. This happens when a supplier has multiple TecDoc registrations (e.g. different regional distributor IDs for the same brand). Both have the same physical part, same specs, same fitment. Deduplicate by `articleNo + supplierName` if you want to show one card per brand
- **`articleInfo` is a redundant nested copy** — all its fields already exist at the parent article level. It appears to be a legacy wrapper; read from the parent fields directly
- **`isAccessory: 0`** is an integer, not a boolean — `0` = primary part, `1` = accessory. Cast to boolean before logic: `isAccessory === 1`
- **`criteriaValue: ""`** means TecDoc has no data for that spec — filter these out before display: `allSpecifications.filter(s => s.criteriaValue !== "")`
- **European decimal comma in `criteriaValue`** — `"9,20"` means 9.20 kg. Always normalize: `value.replace(',', '.')` before `parseFloat()`
- **`oemDisplayNo` is display-formatted** — spaces and hyphens are for human readability. For database storage or search, also store the compact form: `oemDisplayNo.replace(/[\s-]/g, '')` — e.g. `"059 130 106 A"` → `"059130106A"`
- **Same `compatibleCars` in both records** — both supplier registrations have identical fitment because they're the same physical part. When showing fitment, only display once (deduplicate by `vehicleId`)
- **`countryFilterId` affects `compatibleCars`** — changing the country filter narrows which vehicle variants appear. Use Egypt's country ID (find via [#2 GET Countries](#2-get-countries)) for production
- **Kalaax use case:** Primary endpoint for the product detail page when navigating from an article number (e.g. from search results or a barcode scan). One call gives everything needed to render the page: name, image, specs table, OEM cross-refs, and compatible vehicles. No secondary calls needed unless you want richer criteria from [#39 GET Article Criteria](#39-get-article-criteria)
- The "RapidAPI Response Body Size: 2 Bytes" is a known dashboard measurement artefact

---

## 72. GET * Cross-References by Article No

**Method:** GET
**Section:** Enhanced Article Search (`*` tier)
**Date tested:** 2026-04-13
**Response time:** TODO — message truncated before metadata was captured
**Status:** 200 OK

**URL:**
```
TODO — URL was not captured (message truncated at 50k chars). Confirm from RapidAPI dashboard.
```

**Input:** IAM article number (e.g. `"811 357"` from HART)

---

### Response

```json
{
  "countArticles": 413,
  "articles": [
    {
      "articleBrandRoot": "HART",
      "articleNumberRoot": "811 357",
      "crossManufacturerName": "HYUNDAI",
      "crossNumber": "55311-2L000",
      "searchLevel": "IAM -> OEM",
      "articleMediaFileName": "7f7d0e6bb830b100aec03e4b27bf5c3ba99087eb.webp",
      "articleId": 4703802,
      "supplierId": 5251,
      "articleMediaType": "JPG",
      "s3image": "https://fsn1.your-objectstorage.com/tecdoc2025/media_files/images/5251/7f7d0e6bb830b100aec03e4b27bf5c3ba99087eb.webp"
    },
    {
      "articleBrandRoot": "HART",
      "articleNumberRoot": "811 357",
      "crossManufacturerName": "HYUNDAI",
      "crossNumber": "55311-2L500",
      "searchLevel": "IAM -> OEM",
      "articleMediaFileName": "7f7d0e6bb830b100aec03e4b27bf5c3ba99087eb.webp",
      "articleId": 4703802,
      "supplierId": 5251,
      "articleMediaType": "JPG",
      "s3image": "https://fsn1.your-objectstorage.com/tecdoc2025/media_files/images/5251/7f7d0e6bb830b100aec03e4b27bf5c3ba99087eb.webp"
    },
    {
      "articleBrandRoot": "HART",
      "articleNumberRoot": "811 357",
      "crossManufacturerName": "MAXGEAR",
      "crossNumber": "11-0386",
      "searchLevel": "IAM -> OEM -> IAM",
      "articleMediaFileName": "7f7d0e6bb830b100aec03e4b27bf5c3ba99087eb.webp",
      "articleId": 4703802,
      "supplierId": 5251,
      "articleMediaType": "JPG",
      "s3image": "https://fsn1.your-objectstorage.com/tecdoc2025/media_files/images/5251/7f7d0e6bb830b100aec03e4b27bf5c3ba99087eb.webp"
    },
    {
      "articleBrandRoot": "HART",
      "articleNumberRoot": "811 357",
      "crossManufacturerName": "HART",
      "crossNumber": "811 357",
      "searchLevel": "IAM -> OEM -> IAM",
      "articleMediaFileName": "7f7d0e6bb830b100aec03e4b27bf5c3ba99087eb.webp",
      "articleId": 4703802,
      "supplierId": 5251,
      "articleMediaType": "JPG",
      "s3image": "https://fsn1.your-objectstorage.com/tecdoc2025/media_files/images/5251/7f7d0e6bb830b100aec03e4b27bf5c3ba99087eb.webp"
    }
  ]
}
```

*(413 total rows. All share the same `articleId`, `supplierId`, `articleMediaFileName`, and `s3image` — these fields always refer to the **source (root) article**, not the cross-referenced article. Sample rows above show both `searchLevel` variants and the self-reference. Full list truncated.)*

---

### Response Fields

#### Top Level

| Field | Type | Description |
|-------|------|-------------|
| `countArticles` | int | Total number of cross-reference rows found |
| `articles` | array | Flat list of cross-reference rows |

#### `articles[]`

| Field | Type | Description |
|-------|------|-------------|
| `articleBrandRoot` | string | Brand of the **source** article queried (e.g. `"HART"`) |
| `articleNumberRoot` | string | Article number of the **source** article queried (e.g. `"811 357"`) |
| `crossManufacturerName` | string | Brand of the cross-referenced equivalent part |
| `crossNumber` | string | Part number of the cross-referenced equivalent |
| `searchLevel` | string | Path taken to find this cross-reference — see values below |
| `articleId` | int | TecDoc article ID of the **source** (root) article — same on every row |
| `supplierId` | int | Supplier ID of the **source** (root) article — same on every row |
| `articleMediaFileName` | string | Image filename of the **source** (root) article — same on every row |
| `articleMediaType` | string | Media type of the source image — `"JPG"` in test (note: other endpoints use `"JPEG"`) |
| `s3image` | string | Full S3 URL for the **source** (root) article image — same on every row |

#### `searchLevel` values

| Value | Meaning |
|-------|---------|
| `"IAM -> OEM"` | Source IAM article links directly to this OEM number — direct OEM cross-reference |
| `"IAM -> OEM -> IAM"` | Source IAM → OEM pivot → this other IAM brand's equivalent — indirect cross-reference through the OEM number |

> The `->` separator may have trailing spaces (e.g. `"IAM->OEM     "`). Always `.trim()` before comparison. (Same data quality issue documented in #63 and #65.)

---

### Brands Seen in Test Response (413 rows for HART `811 357`)

A partial sample of the cross-referenced brands: HYUNDAI (OEM), MAXGEAR, VITAL SUSPENSIONS, MTR, FEBEST, MASTER-SPORT GERMANY, KAMOKA, PROFIT, AL-KO, Oyodo, SATO tech, METZGER AUTOTEILE, STORM QUALITY PARTS, BOGE, SACHS, STELLOX, KYB, MAGNETI MARELLI, JP GROUP, MEYLE, PRT, MONROE, MONROE-AU, EGT, RED-LINE, VARTEX GERMANY, KRAFT AUTOMOTIVE, MAPCO, ASAM AUTOMOTIVE, DACO Germany, NK, OCAP, GOLD, RIDEX, TRISCAN, DIEDERICHS, OPTIMAL, STATIM, FENOX, MANDO, TRIALLI, EQUAL QUALITY, MGA, APEC, NAPA, BSG, CTR, SIDAT, FISPA, GOOM, FI.BA, ASHIKA, JAPKO, JAPANPARTS, MDR, NIPPARTS, BREMSI, OPEN PARTS, ZEKKERT, KAVO PARTS, SYNCRONIX, AP XENERGY, DAVID VASCO, SpeedMate, Dr!ve+, SRLine, FRECCIA, IBERIS, ZentParts, IOTO, LYNXAUTO, GH, Maysan Mando, QUINTON HAZELL, PEMEBLA, DENCKERMANN, DJ PARTS, 4X4 ESTANFI and more.

---

### Notes

- **`articleId`, `supplierId`, `articleMediaFileName`, `s3image` all belong to the source article** — every row in the response carries the root article's data in these fields. You cannot get the cross-referenced brand's image or articleId from this response. To get a cross-ref article's image, use the `crossNumber` + `crossManufacturerName` to look up that article separately
- **`searchLevel: "IAM -> OEM"`** rows are the direct OEM numbers — in the test these were `HYUNDAI 55311-2L000` and `55311-2L500` (stabilizer link OEM numbers). Only 2 of 413 rows were direct IAM→OEM; all others were the longer IAM→OEM→IAM path
- **`searchLevel: "IAM -> OEM -> IAM"`** rows are equivalent aftermarket parts from other IAM brands that share the same OEM reference. This is the cross-reference network — all 411 aftermarket brands that make an equivalent to HART `811 357`
- **Self-reference present** — `crossManufacturerName: "HART", crossNumber: "811 357"` appears in the list. Filter this out if you want to show "other brands only": `articles.filter(r => !(r.crossManufacturerName === r.articleBrandRoot && r.crossNumber === r.articleNumberRoot))`
- **Duplicate `crossNumber` across brands** — `"F220G1060"` appears under SIDAT, FISPA, and GOOM simultaneously; `"DS3767GT"` appears under both DJ PARTS and Premium Parts. Multiple brands can share the same part number
- **413 cross-references for one part** — this is a popular Hyundai suspension part (stabilizer link) on the Korean platform. High cross-ref count is typical for Korean/Japanese car parts with strong aftermarket coverage
- **`articleMediaType: "JPG"`** — other endpoints return `"JPEG"`. Both mean the same thing; normalize to one value on ingest
- **Different from #50 GET Cross-References by Article ID** — #50 takes an `articleId` and returns cross-refs. This endpoint takes an article number (string) and includes richer source article metadata (`articleBrandRoot`, `articleNumberRoot`, `s3image`) on every row
- **Different from #62 GET * Analog Spare Parts by Article No** — #62 takes an OEM number and returns IAM equivalents with full article detail (articleId, supplierId, image). This endpoint takes an IAM article number and returns the cross-reference graph (OEM numbers + other IAM equivalents) with only the source article's image, not the cross-refs' images
- **Different from #65 GET * OEM/OEM Cross-Reference through Aftermarket Parts** — #65 takes an OEM number and returns OEM-to-OEM cross-references only (no IAM brands). This endpoint takes an IAM number and returns both OEM and IAM equivalents
- **URL and response time are missing** — message truncated at 50k chars before metadata was captured. Confirm the exact URL path from the RapidAPI dashboard
- **Kalaax use case:** "Also available from these brands" section on the product detail page. Use to show a supplier comparison grid: filter `searchLevel` for `"IAM -> OEM -> IAM"` rows to get aftermarket alternatives, or filter for `"IAM -> OEM"` to extract the OEM numbers for display. 413 rows would need pagination or a "show top N brands" limit in the UI
