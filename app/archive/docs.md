  
**KALAAX.COM**

Automotive Spare Parts Marketplace

 

**Backend Development Guide**

Database Schemas, API Specifications, Third-Party Integrations,

Payment Gateway, AI Services & POC Checklist

Prepared by: **Kuberya AI**

Client: **Parts Hub L.L.C (Egypt)**

Date: **April 2026**

*Confidential — Internal Use Only*

# **Table of Contents**

1\. Project Context & Tech Stack

2\. Database Table Schemas

3\. API Specifications

4\. Third-Party Integrations

5\. Payment Gateway (Paymob)

6\. AI Services (OpenAI)

7\. POC Checklist

8\. Developer Quick Reference

# **1\. Project Context & Tech Stack**

Kalaax.com is a drop-shipping marketplace for automotive spare parts in Egypt. Buyers search parts by vehicle, compare prices from multiple sellers, and order. Sellers list inventory against a master TecDoc catalogue. The platform earns commission on each sale.

This document is your single reference for building the backend. Read it fully before writing any code.

## **1.1 Tech Stack**

| Layer | Technology | Notes |
| :---- | :---- | :---- |
| Backend | FastAPI (Python 3.12) | All API endpoints and business logic |
| Frontend | Next.js 14 (React 18\) | SSR for SEO; you only need to return clean JSON |
| Database | PostgreSQL 16 | All structured data; amounts in piastres (integer) |
| Search | Elasticsearch 8 | Part search with Arabic analyser |
| Cache | Redis | Product pages, sessions, rate limiting |
| Task Queue | Celery \+ Redis | Email, SMS, catalogue sync, payouts |
| File Storage | AWS S3 | Product images, KYC documents |
| CDN | Cloudflare | Edge caching, DDoS protection |
| Deployment | Docker on AWS EC2 | Containerised via docker-compose |
| CI/CD | GitHub Actions | Build, test, deploy pipeline |
| AI | OpenAI API | Smart search, Arabic mapping, chat support |

## **1.2 Key Rules (Non-Negotiable)**

All monetary amounts stored as INTEGER in piastres (1 EGP \= 100 piastres). Convert to EGP only in API responses.

All timestamps stored in UTC. Convert to Africa/Cairo only in response.

UUIDs as primary keys for all user-facing entities (orders, users, products, sellers).

No raw SQL. Use SQLAlchemy ORM only.

Every endpoint must have a Pydantic response model. Never return SELECT \*.

All responses use envelope: { data, error, meta }

Commission ledger and payout tables are INSERT-only. No UPDATE or DELETE.

Soft deletes everywhere (deleted\_at timestamp). Hard deletes only for cache/session data.

Secrets loaded from environment variables. Apps must fail fast if required secrets are missing.

# **2\. Database Table Schemas**

Below are all the database tables required. Each table shows column name, data type, constraints, and description. Sample data rows follow each table to show how data looks in practice.

Use Alembic for all migrations. Name format: YYYYMMDD\_short\_description.py. Always test rollback before merging.

## **2.1 users**

Stores all platform users: buyers, sellers, and admins. One table, role-based separation.

| Column | Type | Constraints | Description |
| :---- | :---- | :---- | :---- |
| id | UUID | PK, default uuid4 | Unique user ID |
| email | VARCHAR(255) | UNIQUE, NOT NULL | Login email |
| phone | VARCHAR(20) | UNIQUE, NULLABLE | Egyptian phone (+20...) |
| password\_hash | VARCHAR(255) | NOT NULL | bcrypt hashed password |
| full\_name | VARCHAR(255) | NOT NULL | Display name |
| full\_name\_ar | VARCHAR(255) | NULLABLE | Arabic display name |
| role | VARCHAR(20) | NOT NULL | buyer / seller / admin |
| is\_active | BOOLEAN | DEFAULT true | Account active flag |
| is\_verified | BOOLEAN | DEFAULT false | Email/phone verified |
| google\_id | VARCHAR(255) | NULLABLE | Google OAuth ID |
| locale | VARCHAR(5) | DEFAULT 'ar-EG' | Language preference |
| created\_at | TIMESTAMP | DEFAULT NOW() | UTC creation time |
| updated\_at | TIMESTAMP | ON UPDATE | UTC update time |
| deleted\_at | TIMESTAMP | NULLABLE | Soft delete |

**Sample Data**

id: 550e8400-e29b-41d4-a716-446655440001

email: ahmed.buyer@gmail.com | phone: \+201012345678

role: buyer | full\_name: Ahmed Hassan | locale: ar-EG

## **2.2 buyer\_profiles**

Extended buyer data. One-to-one with users where role \= buyer.

| Column | Type | Constraints | Description |
| :---- | :---- | :---- | :---- |
| id | UUID | PK |  |
| user\_id | UUID | FK users.id, UNIQUE | Link to user |
| default\_address\_id | UUID | FK addresses.id, NULLABLE | Default delivery address |
| created\_at | TIMESTAMP | DEFAULT NOW() |  |

## **2.3 addresses**

Buyer delivery addresses. Egyptian structure: governorate, city, district, street.

| Column | Type | Constraints | Description |
| :---- | :---- | :---- | :---- |
| id | UUID | PK |  |
| user\_id | UUID | FK users.id | Owner |
| label | VARCHAR(50) | NULLABLE | Home / Work / Other |
| full\_name | VARCHAR(255) | NOT NULL | Receiver name |
| phone | VARCHAR(20) | NOT NULL | Receiver phone |
| governorate | VARCHAR(100) | NOT NULL | Egyptian governorate |
| city | VARCHAR(100) | NOT NULL | City name |
| district | VARCHAR(100) | NULLABLE | District/area |
| street | VARCHAR(500) | NOT NULL | Street \+ building |
| postal\_code | VARCHAR(10) | NULLABLE | Postal code |
| is\_default | BOOLEAN | DEFAULT false |  |
| created\_at | TIMESTAMP | DEFAULT NOW() |  |

**Sample Data**

governorate: Cairo | city: Nasr City | district: Zone 8

street: 15 Abbas El Akkad St, Bldg 7, Floor 3, Apt 12

## **2.4 sellers**

Seller business profile. Links to users table. Tracks KYC status.

| Column | Type | Constraints | Description |
| :---- | :---- | :---- | :---- |
| id | UUID | PK |  |
| user\_id | UUID | FK users.id, UNIQUE | Link to user account |
| business\_name | VARCHAR(255) | NOT NULL | Legal business name |
| business\_name\_ar | VARCHAR(255) | NULLABLE | Arabic business name |
| tax\_registration\_no | VARCHAR(50) | UNIQUE | Egyptian tax reg number |
| commercial\_register\_no | VARCHAR(50) | NULLABLE | CR number |
| status | VARCHAR(20) | DEFAULT 'pending' | pending/approved/rejected/suspended |
| tier | VARCHAR(20) | DEFAULT 'new' | new/verified/premium |
| bank\_name | VARCHAR(100) | NULLABLE | Bank for payouts |
| bank\_account\_iban | VARCHAR(34) | NULLABLE | IBAN for payouts |
| show\_name | BOOLEAN | DEFAULT false | Show name or badge only |
| avg\_rating | DECIMAL(3,2) | DEFAULT 0 | Cached average rating |
| total\_orders | INTEGER | DEFAULT 0 | Cached total completed orders |
| avg\_dispatch\_days | DECIMAL(3,1) | DEFAULT 0 | Avg dispatch time |
| return\_rate | DECIMAL(5,2) | DEFAULT 0 | Return percentage |
| rejection\_reason | TEXT | NULLABLE | If rejected/suspended |
| approved\_at | TIMESTAMP | NULLABLE | When approved |
| created\_at | TIMESTAMP | DEFAULT NOW() |  |
| updated\_at | TIMESTAMP | ON UPDATE |  |
| deleted\_at | TIMESTAMP | NULLABLE | Soft delete |

## **2.5 seller\_documents**

KYC document uploads for seller verification. Stored in a private S3 bucket.

| Column | Type | Constraints | Description |
| :---- | :---- | :---- | :---- |
| id | UUID | PK |  |
| seller\_id | UUID | FK sellers.id |  |
| doc\_type | VARCHAR(50) | NOT NULL | commercial\_register / tax\_card / national\_id / iban\_letter |
| s3\_key | VARCHAR(500) | NOT NULL | Private S3 path |
| file\_name | VARCHAR(255) | NOT NULL | Original filename |
| status | VARCHAR(20) | DEFAULT 'pending' | pending / approved / rejected |
| uploaded\_at | TIMESTAMP | DEFAULT NOW() |  |

## **2.6 vehicles (Master Data)**

Master vehicle data synced from TecDoc. Make \> Model \> Year \> Engine.

| Column | Type | Constraints | Description |
| :---- | :---- | :---- | :---- |
| id | UUID | PK |  |
| tecdoc\_id | INTEGER | UNIQUE, NOT NULL | TecDoc vehicle ID |
| make | VARCHAR(100) | NOT NULL, INDEX | Toyota, Hyundai, etc. |
| make\_ar | VARCHAR(100) | NULLABLE | Arabic make name |
| model | VARCHAR(100) | NOT NULL, INDEX | Corolla, Accent, etc. |
| model\_ar | VARCHAR(100) | NULLABLE | Arabic model name |
| year\_from | INTEGER | NOT NULL | Start production year |
| year\_to | INTEGER | NULLABLE | End production year (null=current) |
| engine | VARCHAR(100) | NULLABLE | 1.6L Petrol, 2.0L Diesel |
| engine\_code | VARCHAR(50) | NULLABLE | Technical engine code |
| body\_type | VARCHAR(50) | NULLABLE | sedan/hatchback/suv |
| synced\_at | TIMESTAMP | NOT NULL | Last TecDoc sync time |

## **2.7 buyer\_vehicles (My Garage)**

Saved vehicles per buyer. One is marked active per session.

| Column | Type | Constraints | Description |
| :---- | :---- | :---- | :---- |
| id | UUID | PK |  |
| user\_id | UUID | FK users.id | Buyer who saved this |
| vehicle\_id | UUID | FK vehicles.id | Selected vehicle |
| vin | VARCHAR(17) | NULLABLE | If buyer entered VIN |
| nickname | VARCHAR(100) | NULLABLE | My Corolla, etc. |
| is\_active | BOOLEAN | DEFAULT false | Currently active vehicle |
| created\_at | TIMESTAMP | DEFAULT NOW() |  |

## **2.8 categories**

Part categories synced from TecDoc. Hierarchical tree (parent\_id).

| Column | Type | Constraints | Description |
| :---- | :---- | :---- | :---- |
| id | UUID | PK |  |
| tecdoc\_id | INTEGER | UNIQUE | TecDoc category ID |
| name | VARCHAR(255) | NOT NULL | English name |
| name\_ar | VARCHAR(255) | NOT NULL | Arabic name |
| slug | VARCHAR(255) | UNIQUE | URL slug |
| parent\_id | UUID | FK categories.id, NULLABLE | Parent for tree |
| icon\_url | VARCHAR(500) | NULLABLE | Category icon S3 URL |
| commission\_rate | DECIMAL(5,2) | DEFAULT 8.00 | Commission % for this category |
| is\_active | BOOLEAN | DEFAULT true |  |
| sort\_order | INTEGER | DEFAULT 0 | Display order |

## **2.9 products (articles)**

Master parts catalogue. Each row is one unique part. Synced nightly from TecDoc via RapidAPI.

| Column | Type | Constraints | Description |
| :---- | :---- | :---- | :---- |
| id | UUID | PK |  |
| tecdoc\_article\_id | INTEGER | UNIQUE | TecDoc article number |
| article\_number | VARCHAR(100) | INDEX | Part number (e.g. 1K0615301M) |
| name | VARCHAR(500) | NOT NULL | English part name |
| name\_ar | VARCHAR(500) | NULLABLE | Arabic part name |
| colloquial\_name\_ar | VARCHAR(500) | NULLABLE | Egyptian street name |
| brand | VARCHAR(200) | INDEX | Bosch, Brembo, etc. |
| category\_id | UUID | FK categories.id | Part category |
| description | TEXT | NULLABLE | English description |
| description\_ar | TEXT | NULLABLE | Arabic description |
| oem\_numbers | JSONB | DEFAULT '\[\]' | Array of OEM reference numbers |
| specifications | JSONB | DEFAULT '{}' | Dimensions, weight, etc. |
| images | JSONB | DEFAULT '\[\]' | Array of S3 image URLs |
| warranty\_months | INTEGER | NULLABLE | Warranty period |
| origin | VARCHAR(20) | NULLABLE | oem / aftermarket |
| is\_active | BOOLEAN | DEFAULT true |  |
| synced\_at | TIMESTAMP | NOT NULL | Last TecDoc sync |
| created\_at | TIMESTAMP | DEFAULT NOW() |  |

**Sample Data**

article\_number: 1K0615301M | name: Brake Disc Front

name\_ar: قرص فرامل أمامي | colloquial\_name\_ar: دسك فرامل قدام

brand: Brembo | oem\_numbers: \["1K0615301M", "1K0615301AC"\]

## **2.10 product\_vehicle\_fitment**

Many-to-many between products and vehicles. Which part fits which vehicle.

| Column | Type | Constraints | Description |
| :---- | :---- | :---- | :---- |
| id | UUID | PK |  |
| product\_id | UUID | FK products.id, INDEX | The part |
| vehicle\_id | UUID | FK vehicles.id, INDEX | The vehicle it fits |
| tecdoc\_link\_id | INTEGER | NULLABLE | TecDoc linkage ID |
| synced\_at | TIMESTAMP | NOT NULL |  |

Unique constraint on (product\_id, vehicle\_id) to prevent duplicates.

## **2.11 colloquial\_names**

Egyptian vernacular part names mapped to formal catalogue entries. Admin-managed.

| Column | Type | Constraints | Description |
| :---- | :---- | :---- | :---- |
| id | UUID | PK |  |
| formal\_name | VARCHAR(255) | NOT NULL | Standard Arabic name |
| colloquial\_name | VARCHAR(255) | NOT NULL, INDEX | Street/slang name |
| product\_id | UUID | FK products.id, NULLABLE | Direct link if applicable |
| category\_id | UUID | FK categories.id, NULLABLE | Category level mapping |
| created\_by | UUID | FK users.id | Admin who added |
| created\_at | TIMESTAMP | DEFAULT NOW() |  |

**Sample Data**

formal\_name: مضخة المياه | colloquial\_name: طرمبة المية

(water pump mapped to its Egyptian slang equivalent)

## **2.12 seller\_offers**

Core marketplace table. One seller, one product, one offer. Multiple sellers compete on same product.

| Column | Type | Constraints | Description |
| :---- | :---- | :---- | :---- |
| id | UUID | PK |  |
| seller\_id | UUID | FK sellers.id, INDEX | Which seller |
| product\_id | UUID | FK products.id, INDEX | Which part |
| price | INTEGER | NOT NULL | Price in piastres (e.g. 45000 \= 450 EGP) |
| quantity | INTEGER | NOT NULL, DEFAULT 0 | Available stock |
| dispatch\_days | INTEGER | DEFAULT 1 | Days to dispatch after order |
| status | VARCHAR(20) | DEFAULT 'draft' | draft / published / suspended |
| is\_buy\_box | BOOLEAN | DEFAULT false | Top ranked offer flag |
| rank\_score | DECIMAL(8,4) | DEFAULT 0 | Computed ranking score |
| created\_at | TIMESTAMP | DEFAULT NOW() |  |
| updated\_at | TIMESTAMP | ON UPDATE |  |

Auto-suspend: trigger or application logic sets status \= suspended when quantity reaches 0\.

**Sample Data**

seller\_id: (Seller A) | product\_id: (Brake Disc Front)

price: 45000 (=450 EGP) | quantity: 25 | dispatch\_days: 1

status: published | is\_buy\_box: true

## **2.13 orders**

Buyer order. Contains one or more sub\_orders (one per seller).

| Column | Type | Constraints | Description |
| :---- | :---- | :---- | :---- |
| id | UUID | PK |  |
| order\_number | VARCHAR(20) | UNIQUE, NOT NULL | Human-readable (KLX-20260411-001) |
| buyer\_id | UUID | FK users.id | Who placed the order |
| address\_id | UUID | FK addresses.id | Delivery address snapshot |
| address\_snapshot | JSONB | NOT NULL | Frozen address at order time |
| subtotal | INTEGER | NOT NULL | Sum of items in piastres |
| discount\_amount | INTEGER | DEFAULT 0 | Promo discount in piastres |
| shipping\_total | INTEGER | DEFAULT 0 | Total shipping cost |
| total | INTEGER | NOT NULL | Final amount buyer pays |
| currency | VARCHAR(3) | DEFAULT 'EGP' | Always EGP |
| payment\_method | VARCHAR(20) | NOT NULL | card / cod |
| payment\_status | VARCHAR(20) | DEFAULT 'pending' | pending/paid/failed/refunded |
| payment\_ref | VARCHAR(255) | NULLABLE | Paymob transaction ID |
| promo\_code\_id | UUID | FK promo\_codes.id, NULLABLE | Applied promo |
| status | VARCHAR(20) | DEFAULT 'pending' | pending/confirmed/completed/cancelled |
| created\_at | TIMESTAMP | DEFAULT NOW() |  |
| updated\_at | TIMESTAMP | ON UPDATE |  |

## **2.14 sub\_orders**

One sub\_order per seller within a parent order. Tracks fulfilment separately.

| Column | Type | Constraints | Description |
| :---- | :---- | :---- | :---- |
| id | UUID | PK |  |
| order\_id | UUID | FK orders.id | Parent order |
| seller\_id | UUID | FK sellers.id | Which seller fulfils this |
| subtotal | INTEGER | NOT NULL | Sum of this seller items |
| shipping\_cost | INTEGER | DEFAULT 0 | Shipping for this sub\_order |
| status | VARCHAR(20) | DEFAULT 'pending' | pending/accepted/dispatched/delivered/returned |
| tracking\_number | VARCHAR(100) | NULLABLE | Bosta tracking number |
| dispatched\_at | TIMESTAMP | NULLABLE | When seller dispatched |
| delivered\_at | TIMESTAMP | NULLABLE | When buyer received |
| created\_at | TIMESTAMP | DEFAULT NOW() |  |

## **2.15 order\_items**

| Column | Type | Constraints | Description |
| :---- | :---- | :---- | :---- |
| id | UUID | PK |  |
| sub\_order\_id | UUID | FK sub\_orders.id | Which sub\_order |
| offer\_id | UUID | FK seller\_offers.id | Which offer was purchased |
| product\_id | UUID | FK products.id | Which product |
| seller\_id | UUID | FK sellers.id | Redundant for query speed |
| quantity | INTEGER | NOT NULL | How many |
| unit\_price | INTEGER | NOT NULL | Price per unit at purchase time (piastres) |
| total\_price | INTEGER | NOT NULL | quantity \* unit\_price |
| vehicle\_id | UUID | FK vehicles.id, NULLABLE | Buyer vehicle at time of purchase |

## **2.16 commission\_ledger**

APPEND-ONLY. No UPDATE or DELETE. Protect with DB trigger. This is the financial audit trail.

| Column | Type | Constraints | Description |
| :---- | :---- | :---- | :---- |
| id | UUID | PK |  |
| sub\_order\_id | UUID | FK sub\_orders.id | Which sub\_order |
| seller\_id | UUID | FK sellers.id | Which seller |
| order\_item\_id | UUID | FK order\_items.id | Which item |
| sale\_amount | INTEGER | NOT NULL | Total sale in piastres |
| commission\_rate | DECIMAL(5,2) | NOT NULL | Rate applied (e.g. 8.00) |
| commission\_amount | INTEGER | NOT NULL | Commission in piastres |
| platform\_fee | INTEGER | DEFAULT 0 | Fixed per-txn fee in piastres |
| created\_at | TIMESTAMP | DEFAULT NOW() |  |

**Sample Calculation**

sale\_amount: 45000 (450 EGP) | commission\_rate: 8.00%

commission\_amount: 3600 (36 EGP) | platform\_fee: 300 (3 EGP)

## **2.17 payout\_batches**

Weekly payout batch. Admin creates, reviews, and marks as paid.

| Column | Type | Constraints | Description |
| :---- | :---- | :---- | :---- |
| id | UUID | PK |  |
| batch\_number | VARCHAR(20) | UNIQUE | PAY-20260411-001 |
| period\_start | DATE | NOT NULL | Start of payout period |
| period\_end | DATE | NOT NULL | End of payout period |
| total\_amount | INTEGER | NOT NULL | Total payout in piastres |
| status | VARCHAR(20) | DEFAULT 'pending' | pending/approved/paid |
| bank\_ref | VARCHAR(255) | NULLABLE | Manual bank transfer ref |
| paid\_at | TIMESTAMP | NULLABLE |  |
| created\_by | UUID | FK users.id | Admin who created |
| created\_at | TIMESTAMP | DEFAULT NOW() |  |

## **2.18 payout\_items**

| Column | Type | Constraints | Description |
| :---- | :---- | :---- | :---- |
| id | UUID | PK |  |
| batch\_id | UUID | FK payout\_batches.id | Which batch |
| seller\_id | UUID | FK sellers.id | Which seller gets paid |
| gross\_amount | INTEGER | NOT NULL | Total sales in piastres |
| commission\_total | INTEGER | NOT NULL | Total commission deducted |
| net\_amount | INTEGER | NOT NULL | Amount to pay seller |
| sub\_order\_ids | JSONB | NOT NULL | Array of sub\_order IDs included |

## **2.19 promo\_codes**

| Column | Type | Constraints | Description |
| :---- | :---- | :---- | :---- |
| id | UUID | PK |  |
| code | VARCHAR(50) | UNIQUE, NOT NULL | KALAAX20 etc. |
| type | VARCHAR(20) | NOT NULL | percentage / fixed / free\_shipping |
| value | INTEGER | NOT NULL | Percentage (e.g. 10\) or fixed amount in piastres |
| min\_order\_amount | INTEGER | DEFAULT 0 | Minimum order to apply |
| max\_discount | INTEGER | NULLABLE | Cap on discount amount |
| usage\_limit | INTEGER | NULLABLE | Total uses allowed |
| used\_count | INTEGER | DEFAULT 0 | Times used so far |
| starts\_at | TIMESTAMP | NULLABLE | Active from |
| expires\_at | TIMESTAMP | NULLABLE | Active until |
| is\_active | BOOLEAN | DEFAULT true |  |
| created\_by | UUID | FK users.id | Admin who created |

## **2.20 reviews**

| Column | Type | Constraints | Description |
| :---- | :---- | :---- | :---- |
| id | UUID | PK |  |
| order\_item\_id | UUID | FK order\_items.id, UNIQUE | One review per purchase |
| buyer\_id | UUID | FK users.id | Reviewer |
| product\_id | UUID | FK products.id | Reviewed product |
| seller\_id | UUID | FK sellers.id | Reviewed seller |
| rating | SMALLINT | NOT NULL, CHECK 1-5 | Star rating |
| comment | TEXT | NULLABLE | Review text |
| status | VARCHAR(20) | DEFAULT 'pending' | pending/approved/rejected |
| created\_at | TIMESTAMP | DEFAULT NOW() |  |

## **2.21 return\_requests**

| Column | Type | Constraints | Description |
| :---- | :---- | :---- | :---- |
| id | UUID | PK |  |
| sub\_order\_id | UUID | FK sub\_orders.id |  |
| buyer\_id | UUID | FK users.id |  |
| seller\_id | UUID | FK sellers.id |  |
| reason | VARCHAR(50) | NOT NULL | defective/wrong\_part/not\_needed/other |
| description | TEXT | NULLABLE | Buyer explanation |
| photo\_urls | JSONB | DEFAULT '\[\]' | Evidence photos on S3 |
| status | VARCHAR(20) | DEFAULT 'pending' | pending/accepted/rejected/escalated/refunded |
| seller\_response | TEXT | NULLABLE | Seller reply |
| admin\_resolution | TEXT | NULLABLE | If escalated |
| refund\_amount | INTEGER | NULLABLE | Refund in piastres |
| created\_at | TIMESTAMP | DEFAULT NOW() |  |
| resolved\_at | TIMESTAMP | NULLABLE |  |

## **2.22 wishlists**

| Column | Type | Constraints | Description |
| :---- | :---- | :---- | :---- |
| id | UUID | PK |  |
| user\_id | UUID | FK users.id | Buyer |
| product\_id | UUID | FK products.id | Saved product |
| created\_at | TIMESTAMP | DEFAULT NOW() |  |

Unique constraint on (user\_id, product\_id).

## **2.23 catalogue\_gap\_requests**

When a seller cannot find a part in the catalogue, they submit a gap request for admin review.

| Column | Type | Constraints | Description |
| :---- | :---- | :---- | :---- |
| id | UUID | PK |  |
| seller\_id | UUID | FK sellers.id | Requesting seller |
| part\_name | VARCHAR(255) | NOT NULL | Name of missing part |
| brand | VARCHAR(100) | NULLABLE |  |
| oem\_number | VARCHAR(100) | NULLABLE |  |
| vehicle\_info | TEXT | NULLABLE | What vehicle it fits |
| status | VARCHAR(20) | DEFAULT 'pending' | pending/added/rejected |
| admin\_notes | TEXT | NULLABLE |  |
| created\_at | TIMESTAMP | DEFAULT NOW() |  |

## **2.24 refresh\_tokens**

When a user logs in, they get two tokens: an access token (expires in 15 minutes) and a refresh token (expires in 30 days). The access token is what the frontend sends with every API call to prove "I'm logged in." But since it dies in 15 minutes, the user would have to log in again every 15 minutes — terrible experience.

So instead, when the access token expires, the frontend silently sends the refresh token to `/auth/refresh` and gets a brand new access token — no login screen, the user doesn't even notice. The `refresh_tokens` table stores these refresh tokens (hashed) so we can verify them, track which device they belong to, and revoke them if someone logs out or if we detect suspicious activity (like the same token being used twice, which means it was stolen).

Short version: it keeps users logged in for 30 days without asking them to re-enter their password, while still being secure.

| Column | Type | Constraints | Description |
| :---- | :---- | :---- | :---- |
| id | UUID | PK |  |
| user\_id | UUID | FK users.id |  |
| token\_hash | VARCHAR(255) | UNIQUE, NOT NULL | SHA256 of token |
| device\_fingerprint | VARCHAR(255) | NULLABLE |  |
| expires\_at | TIMESTAMP | NOT NULL | 30 days from creation |
| is\_revoked | BOOLEAN | DEFAULT false |  |
| created\_at | TIMESTAMP | DEFAULT NOW() |  |

## **2.25 notifications**

| Column | Type | Constraints | Description |
| :---- | :---- | :---- | :---- |
| id | UUID | PK |  |
| user\_id | UUID | FK users.id | Recipient |
| type | VARCHAR(50) | NOT NULL | order\_confirmed/shipped/price\_drop etc. |
| title | VARCHAR(255) | NOT NULL | Notification title |
| title\_ar | VARCHAR(255) | NOT NULL | Arabic title |
| body | TEXT | NOT NULL | Notification body |
| body\_ar | TEXT | NOT NULL | Arabic body |
| data | JSONB | DEFAULT '{}' | Payload: order\_id, product\_id, etc. |
| is\_read | BOOLEAN | DEFAULT false |  |
| channel | VARCHAR(20) | NOT NULL | push/email/sms |
| sent\_at | TIMESTAMP | DEFAULT NOW() |  |

## **2.26 flash\_sales**

| Column | Type | Constraints | Description |
| :---- | :---- | :---- | :---- |
| id | UUID | PK |  |
| offer\_id | UUID | FK seller\_offers.id | Which offer |
| original\_price | INTEGER | NOT NULL | Regular price in piastres |
| flash\_price | INTEGER | NOT NULL | Discounted price |
| starts\_at | TIMESTAMP | NOT NULL |  |
| ends\_at | TIMESTAMP | NOT NULL |  |
| is\_active | BOOLEAN | DEFAULT true |  |

# **3\. API Specifications**

All endpoints follow REST conventions. Base URL: /api/v1. All responses use the envelope format: { data: ..., error: null, meta: { total, limit, offset, has\_more } }. On error: { data: null, error: { code: "...", message: "..." }, meta: null }

Authentication: JWT Bearer token in Authorization header. Access token \= 15 min. Refresh token \= 30 days, stored hashed in DB.

## **3.1 Authentication APIs**

Frontend integrates these on: Login page, Register page, Forgot password flow.

| Endpoint | Purpose | Payload | Response |
| :---- | :---- | :---- | :---- |
| POST /auth/register | Register buyer/seller | { email, password, full\_name, full\_name\_ar, phone, role } | { data: { user\_id, access\_token, refresh\_token } } |
| POST /auth/login | Email+password login | { email, password } | { data: { user\_id, role, access\_token, refresh\_token } } |
| POST /auth/google | Google OAuth login | { google\_token } | { data: { user\_id, role, access\_token, refresh\_token } } |
| POST /auth/refresh | Get new tokens | { refresh\_token } | { data: { access\_token, refresh\_token } } |
| POST /auth/logout | Revoke refresh token | { refresh\_token } | { data: { success: true } } |
| POST /auth/otp/send | Send OTP to phone | { phone } | { data: { message: 'sent' } } |
| POST /auth/otp/verify | Verify OTP | { phone, otp\_code } | { data: { verified: true } } |
| POST /auth/password/reset | Request password reset | { email } | { data: { message: 'email sent' } } |
| POST /auth/password/change | Change password (auth) | { old\_password, new\_password } | { data: { success: true } } |

Rate limits: Login \= 10 attempts/IP/15 min. OTP \= 5 attempts/phone/hour. Return 429 with Retry-After header.

## **3.2 Vehicle & Garage APIs**

Frontend: Vehicle selector dropdowns (cascading), My Garage page, VIN lookup.

| Endpoint | Purpose | Payload/Params | Response |
| :---- | :---- | :---- | :---- |
| GET /vehicles/makes | List all makes | ?lang=ar | { data: \[{ id, name, name\_ar, logo\_url }\] } |
| GET /vehicles/models | Models for a make | ?make\_id=...\&lang=ar | { data: \[{ id, name, name\_ar }\] } |
| GET /vehicles/years | Years for a model | ?model\_id=... | { data: \[2024, 2023, ...\] } |
| GET /vehicles/engines | Engines for model+year | ?model\_id=...\&year=2020 | { data: \[{ id, engine, engine\_code }\] } |
| POST /vehicles/vin-lookup | Decode VIN | { vin: '...' } | { data: { vehicle\_id, make, model, year, engine } } |
| GET /me/garage | Buyer saved vehicles | Auth required | { data: \[{ id, vehicle, nickname, is\_active }\] } |
| POST /me/garage | Save vehicle to garage | { vehicle\_id, nickname } | { data: { id, vehicle, is\_active } } |
| PATCH /me/garage/{id}/activate | Set active vehicle | Auth required | { data: { success: true } } |
| DELETE /me/garage/{id} | Remove from garage | Auth required | { data: { success: true } } |

## **3.3 Search & Catalogue APIs**

Frontend: Homepage, Search bar (autocomplete), Search results page, Category pages.

| Endpoint | Purpose | Payload/Params | Response |
| :---- | :---- | :---- | :---- |
| GET /search | Full text search | ?q=...\&vehicle\_id=...\&category\_id=...\&brand=...\&min\_price=...\&max\_price=...\&origin=...\&sort=price\_asc\&limit=20\&offset=0 | { data: \[ProductListItem\], meta: { total, ... } } |
| GET /search/autocomplete | Suggestions as user types | ?q=...\&vehicle\_id=...\&limit=8 | { data: \[{ text, type: 'product'|'category', id }\] } |
| GET /categories | All root categories | ?lang=ar | { data: \[{ id, name, name\_ar, slug, icon\_url, children }\] } |
| GET /categories/{slug}/products | Products in category | ?vehicle\_id=...\&sort=...\&limit=20\&offset=0 | { data: \[ProductListItem\], meta } |
| GET /products/{id} | Product detail page | ?vehicle\_id=... | { data: ProductDetail } |
| GET /products/{id}/offers | All seller offers for product | ?sort=price\_asc | { data: \[OfferItem\] } |
| GET /products/{id}/reviews | Product reviews | ?limit=10\&offset=0 | { data: \[ReviewItem\], meta } |
| GET /products/{id}/fitment | Check vehicle fitment | ?vehicle\_id=... | { data: { fits: true/false, status: 'confirmed'|'unconfirmed' } } |
| GET /products/trending | Homepage trending parts | ?limit=10 | { data: \[ProductListItem\] } |
| GET /products/oem-crossref | OEM cross reference | ?oem\_number=... | { data: \[ProductListItem\] } |

**ProductListItem Shape**

{ id, article\_number, name, name\_ar, brand, category, images\[0\],

  lowest\_price, offer\_count, avg\_rating, review\_count, fits\_vehicle }

**ProductDetail Shape**

{ id, article\_number, name, name\_ar, brand, category,

  description, description\_ar, images\[\], oem\_numbers\[\],

  specifications{}, warranty\_months, origin,

  buy\_box\_offer: OfferItem, offer\_count, avg\_rating, review\_count }

**OfferItem Shape**

{ offer\_id, seller\_label: 'Seller A', seller\_tier, seller\_rating,

  price (EGP), dispatch\_days, quantity, is\_buy\_box }

Note: seller\_label is anonymised. Never expose actual seller name to buyer.

## **3.4 Cart & Checkout APIs**

Frontend: Cart page, Checkout page, Order confirmation page.

| Endpoint | Purpose | Payload/Params | Response |
| :---- | :---- | :---- | :---- |
| GET /cart | Get current cart | Auth required | { data: { items\[\], vehicle\_id, subtotal, shipping, total } } |
| POST /cart/items | Add to cart | { offer\_id, quantity, vehicle\_id } | { data: CartItem } |
| PATCH /cart/items/{id} | Update quantity | { quantity } | { data: CartItem } |
| DELETE /cart/items/{id} | Remove item |  | { data: { success: true } } |
| POST /cart/promo | Apply promo code | { code: 'KALAAX20' } | { data: { discount\_amount, new\_total } } |
| DELETE /cart/promo | Remove promo |  | { data: { success: true } } |
| POST /checkout | Place order | { address\_id, payment\_method: 'card'|'cod' } | { data: { order\_id, order\_number, payment\_url (if card) } } |
| POST /checkout/payment/callback | Paymob webhook | Paymob posts here | 200 OK |
| GET /checkout/payment/status/{order\_id} | Check payment status |  | { data: { status: 'paid'|'pending'|'failed' } } |

Vehicle-gated cart: Backend MUST reject add-to-cart if vehicle\_id is missing. Also validate fitment on server side.

## **3.5 Buyer Account APIs**

Frontend: My Orders page, Order detail, Returns, Wishlist, Profile settings.

| Endpoint | Purpose | Payload/Params | Response |
| :---- | :---- | :---- | :---- |
| GET /me/orders | Order history | ?status=...\&limit=20\&offset=0 | { data: \[OrderListItem\], meta } |
| GET /me/orders/{id} | Order detail |  | { data: OrderDetail with sub\_orders and tracking } |
| POST /me/orders/{sub\_order\_id}/return | Request return | { reason, description, photos\[\] } | { data: ReturnRequest } |
| GET /me/wishlist | Wishlist | ?limit=20\&offset=0 | { data: \[WishlistItem with current price/stock\] } |
| POST /me/wishlist | Add to wishlist | { product\_id } | { data: { id } } |
| DELETE /me/wishlist/{id} | Remove |  | { data: { success: true } } |
| GET /me/profile | Get profile |  | { data: UserProfile } |
| PATCH /me/profile | Update profile | { full\_name, phone, locale } | { data: UserProfile } |
| POST /me/reviews | Submit review | { order\_item\_id, rating, comment } | { data: Review } |

## **3.6 Seller Portal APIs**

Frontend: Seller registration, Seller dashboard, Inventory management, Order fulfilment.

| Endpoint | Purpose | Payload/Params | Response |
| :---- | :---- | :---- | :---- |
| POST /seller/register | Submit registration | { business\_name, tax\_reg\_no, bank\_name, iban, documents\[\] } | { data: { seller\_id, status: 'pending' } } |
| GET /seller/status | Check KYC status | Auth required | { data: { status, rejection\_reason } } |
| GET /seller/dashboard | Dashboard metrics | ?period=day|week|month | { data: { total\_orders, gmv, top\_parts\[\], avg\_dispatch } } |
| GET /seller/inventory | My offers | ?status=...\&q=...\&limit=20\&offset=0 | { data: \[SellerOfferItem\], meta } |
| POST /seller/inventory | Create offer | { product\_id, price, quantity, dispatch\_days } | { data: SellerOffer } |
| PATCH /seller/inventory/{id} | Update offer | { price, quantity, dispatch\_days } | { data: SellerOffer } |
| DELETE /seller/inventory/{id} | Unpublish offer |  | { data: { success: true } } |
| POST /seller/inventory/bulk-upload | CSV upload | multipart/form-data { file } | { data: { imported: 45, errors: 3, error\_rows: \[...\] } } |
| GET /seller/catalogue/search | Search master catalogue | ?q=...\&vehicle\_id=... | { data: \[ProductListItem\] } |
| POST /seller/catalogue/gap-request | Report missing part | { part\_name, brand, oem\_number, vehicle\_info } | { data: { id, status: 'pending' } } |
| GET /seller/orders | Orders to fulfil | ?status=...\&limit=20\&offset=0 | { data: \[SellerOrderItem\], meta } |
| PATCH /seller/orders/{sub\_order\_id}/accept | Accept order |  | { data: { status: 'accepted' } } |
| PATCH /seller/orders/{sub\_order\_id}/dispatch | Mark dispatched |  | { data: { tracking\_number, status: 'dispatched' } } |
| GET /seller/returns | Return requests | ?status=...\&limit=20 | { data: \[ReturnItem\], meta } |
| PATCH /seller/returns/{id} | Respond to return | { action: 'accept'|'reject', response } | { data: ReturnRequest } |
| GET /seller/payouts | Payout history | ?limit=20\&offset=0 | { data: \[PayoutItem\], meta } |
| GET /seller/commission-statements | Commission detail | ?period\_start=...\&period\_end=... | { data: \[CommissionEntry\] } |

## **3.7 Admin APIs**

Frontend: Admin dashboard, Seller KYC queue, Catalogue editor, Order management, Payouts.

| Endpoint | Purpose | Payload/Params | Response |
| :---- | :---- | :---- | :---- |
| GET /admin/dashboard | KPI dashboard |  | { data: { gmv\_today, orders\_today, active\_buyers, active\_sellers, pending\_kyc\_count } } |
| GET /admin/sellers | Seller directory | ?status=...\&q=...\&limit=20 | { data: \[SellerListItem\], meta } |
| GET /admin/sellers/{id} | Seller detail \+ docs |  | { data: SellerDetail with documents\[\] } |
| PATCH /admin/sellers/{id}/approve | Approve seller |  | { data: { status: 'approved' } } \+ triggers email |
| PATCH /admin/sellers/{id}/reject | Reject seller | { reason } | { data: { status: 'rejected' } } |
| PATCH /admin/sellers/{id}/suspend | Suspend seller | { reason } | { data: { status: 'suspended' } } |
| PATCH /admin/sellers/{id}/reinstate | Reinstate |  | { data: { status: 'approved' } } |
| GET /admin/orders | All orders | ?status=...\&seller\_id=...\&date\_from=...\&limit=20 | { data: \[OrderListItem\], meta } |
| GET /admin/catalogue/gap-requests | Pending gap requests | ?status=pending | { data: \[GapRequest\], meta } |
| PATCH /admin/catalogue/gap-requests/{id} | Resolve gap request | { status, admin\_notes } | { data: GapRequest } |
| POST /admin/products | Add product manually | { full product payload } | { data: Product } |
| PATCH /admin/products/{id} | Edit product | { fields to update } | { data: Product } |
| GET /admin/reviews | Review moderation | ?status=pending | { data: \[Review\], meta } |
| PATCH /admin/reviews/{id} | Approve/reject review | { status: 'approved'|'rejected' } | { data: Review } |
| POST /admin/promo-codes | Create promo | { code, type, value, ... } | { data: PromoCode } |
| GET /admin/payouts/batches | Payout batches | ?status=...\&limit=20 | { data: \[PayoutBatch\], meta } |
| POST /admin/payouts/batches | Create payout batch | { period\_start, period\_end } | { data: PayoutBatch with items\[\] } |
| PATCH /admin/payouts/batches/{id}/pay | Mark batch paid | { bank\_ref } | { data: PayoutBatch } |
| GET /admin/returns | All return requests | ?status=...\&limit=20 | { data: \[ReturnRequest\], meta } |
| PATCH /admin/returns/{id}/resolve | Admin resolve dispute | { resolution, refund\_amount } | { data: ReturnRequest } |
| POST /admin/colloquial-names | Add colloquial name | { formal\_name, colloquial\_name, product\_id } | { data: ColloquialName } |
| GET /admin/reports/revenue | Revenue report | ?date\_from=...\&date\_to=... | { data: { gmv, net\_revenue, refunds, commission\_total } } |
| GET /admin/reports/vat-summary | VAT for ETA filing | ?month=2026-04 | { data: { total\_sales, vat\_amount, invoice\_count } } |

## **3.8 Notification APIs**

| Endpoint | Purpose | Payload/Params | Response |
| :---- | :---- | :---- | :---- |
| GET /me/notifications | User notifications | ?is\_read=false\&limit=20 | { data: \[Notification\], meta } |
| PATCH /me/notifications/{id}/read | Mark as read |  | { data: { success: true } } |
| POST /me/notifications/push-token | the buyer's browser gives us its "notification address" and we save it so we can send them updates later through their browser. | { token, platform } | { data: { success: true } } |

# **4\. Third-Party Integrations**

## **4.1 TecDoc / RapidAPI (Parts Catalogue)**

**Purpose:** Master parts catalogue data. Vehicle data, part identification, cross-referencing, fitment data.

**Where it integrates:** Nightly Celery sync task populates products, vehicles, categories, and product\_vehicle\_fitment tables. Also used for VIN lookup.

**Paid/Free:** Paid. RapidAPI subscription. Multiple tiers available. Client already has an account.

**Who provides:** CLIENT already has RapidAPI account with TecDoc Catalog API subscription.

**What we need from client:**

1\. RapidAPI account credentials (email/password for dashboard access)

2\. Current API key (or generate new one after rotating old exposed key)

3\. Subscription plan details (request quota per month)

4\. Generate SEPARATE API keys: one for staging, one for production

**Setup steps:**

1\. Client logs into RapidAPI dashboard and rotates the old key (was hardcoded and exposed)

2\. Client generates 2 new API keys under the same subscription

3\. We store keys as environment variables: TECDOC\_RAPIDAPI\_KEY\_STAGING and TECDOC\_RAPIDAPI\_KEY\_PROD

4\. Never hardcode keys. Load via config.py from env vars.

**Key endpoints we use:**

GET /manufacturers \- List all vehicle makes

GET /models \- Models for a manufacturer

GET /vehicles \- Vehicle variants (year, engine)

GET /articles \- Parts by category \+ vehicle

GET /article-details \- Full part details, OEM numbers, specs

GET /article-oemNumbers \- Cross-reference OEM codes

GET /vehicle-by-vin \- VIN decode to vehicle

**Sync strategy:**

Nightly Celery task (2 AM Cairo time). Sync runs in background. If sync fails, email admin but do NOT cause downtime. Use pagination. Process in batches of 100\. Upsert records (insert or update on tecdoc\_id).

## **4.2 NHTSA VIN Decode API**

**Purpose:** Free VIN decoding as fallback/supplement to TecDoc VIN lookup.

**Where it integrates:** VIN lookup endpoint (/vehicles/vin-lookup). Try TecDoc first, fallback to NHTSA.

**Paid/Free:** FREE. No API key required. US government service.

**Who provides:** Public API. No client action needed.

**Endpoint:**

GET https://vpic.nhtsa.dot.gov/api/vehicles/decodevin/{VIN}?format=json

## **4.3 Vonage (SMS / OTP)**

**Purpose:** SMS OTPs for login verification. Arabic order status SMS to buyers and sellers.

**Where it integrates:** Auth OTP endpoints, order notification Celery tasks.

**Paid/Free:** Paid. Pay per SMS. Vonage offers Egypt-specific rates.

**Who provides:** WE sign up. Client provides Egyptian business details for sender ID registration.

**Setup steps:**

1\. Sign up at vonage.com/communications-apis

2\. Get API Key \+ API Secret from dashboard

3\. Register an Egyptian Sender ID (requires Egyptian business documents from client)

4\. Required from client: Commercial Register copy, letter authorising sender ID name

5\. Test with sandbox first, then go live after sender ID approval (takes 3-5 business days)

6\. Store VONAGE\_API\_KEY, VONAGE\_API\_SECRET, VONAGE\_SENDER\_ID in env vars

**OTP format:**

Arabic: رمز التحقق الخاص بك هو: 123456

English fallback: Your verification code is: 123456

## **4.4 AWS SES (Email)**

**Purpose:** Transactional emails: order confirmation, seller approval, payout notification, password reset.

**Where it integrates:** Celery email tasks. All emails sent in Arabic and English.

**Paid/Free:** Paid. Very cheap ($0.10 per 1000 emails). Part of AWS.

**Who provides:** WE set up using our/client AWS account.

**Setup steps:**

1\. Enable SES in AWS Console (same account as EC2/S3)

2\. Verify sending domain (kalaax.com) by adding DNS records

3\. Request production access (move out of SES sandbox) \- takes 1-2 days

4\. Required from client: DNS access to kalaax.com to add DKIM/SPF records

5\. Store AWS\_SES\_REGION, AWS\_ACCESS\_KEY\_ID, AWS\_SECRET\_ACCESS\_KEY in env vars

## **4.5 Firebase Cloud Messaging (Push Notifications)**

**Purpose:** Push notifications to buyer’s browser. Order updates, price drops, flash sales.

**Where it integrates:** Notification service in backend. Frontend registers FCM token, backend sends via FCM.

**Paid/Free:** FREE (part of Firebase free tier).

**Who provides:** WE create Firebase project under client Google account, OR client creates and shares credentials.

**Setup steps:**

1\. Create Firebase project at console.firebase.google.com

2\. Enable Cloud Messaging

3\. Generate VAPID keys for web push

4\. Download service account JSON key file

5\. Store FIREBASE\_SERVICE\_ACCOUNT\_JSON path in env vars

6\. Required from client: Google account (or we create under their organisation)

## **4.6 Google OAuth**

**Purpose:** Sign in with Google for buyers.

**Paid/Free:** FREE.

**Who provides:** WE set up in Google Cloud Console.

**Setup:**

1\. Create OAuth 2.0 Client ID in Google Cloud Console

2\. Set redirect URIs for staging and production

3\. Store GOOGLE\_CLIENT\_ID, GOOGLE\_CLIENT\_SECRET in env vars

## **4.7 AWS S3 (File Storage)**

**Purpose:** Product images, KYC documents, invoice PDFs.

**Paid/Free:** Paid. Very cheap ($0.023/GB/month).

**Bucket structure:**

kalaax-public: product images, category icons (served via Cloudflare CDN)

kalaax-private: KYC docs, invoices (pre-signed URLs with 1-hour expiry)

## **4.8 Bosta (Logistics & Courier)**

**Purpose:** Courier pickup booking, shipping labels, delivery tracking for Egyptian market.

**Where it integrates:** Seller dispatch flow. When seller clicks Dispatch, backend calls Bosta to create shipment and get tracking number.

**Paid/Free:** Paid per shipment. Bosta charges per delivery. No monthly fee.

**Who provides:** CLIENT must sign up with Bosta directly and get API key.

**What we need from client:**

1\. Register at business.bosta.co/signup

2\. Wait for Bosta account approval

3\. Get API key from Bosta dashboard \> Settings \> API Integration

4\. Share API key with us for staging integration

5\. Bosta provides separate sandbox environment for testing

**Key API calls we make:**

POST /deliveries \- Create a delivery (pickup from seller, deliver to buyer)

GET /deliveries/{id} \- Track delivery status

GET /deliveries/{id}/airwaybill \- Download shipping label PDF

POST /deliveries/{id}/cancel \- Cancel a delivery

**Webhook:**

Bosta sends status updates to our webhook URL. We update sub\_order status when delivery status changes.

POST /webhooks/bosta \- Bosta calls this when delivery status changes

Python SDK available: pip install bosta

API docs: docs.bosta.co

## **4.9 Google Analytics 4**

**Purpose:** Page views, buyer funnel, conversions.

**Where:** Frontend only (Next.js). No backend work needed.

**Paid/Free:** FREE.

Required from client: Google account. We create GA4 property.

## **4.10 Egyptian Tax Authority (ETA) E-Invoice API**

**ETA E-Invoice API — What it does in our flow**

In Egypt, there's a law that says every time a business sells something online, it must report that sale to the Egyptian Tax Authority (ETA) electronically — in real time. This is not optional. If Kalaax doesn't do this, the client can face fines between 20,000 to 100,000 EGP.

**Here's how it fits in our flow:**

A buyer places an order on Kalaax and pays. The moment that order is confirmed, our backend automatically sends an electronic invoice to the ETA government system in the background. This invoice contains: who sold (Kalaax/Parts Hub L.L.C), who bought, what part, how much, and how much VAT was charged.

The ETA system receives it, validates it, and gives back a unique government invoice ID. We store that ID in our database. That's it — the sale is now legally reported.

**Why it matters for the client:**

The client (Parts Hub L.L.C) is an Egyptian registered company. Every sale on the platform is a taxable transaction. Without this integration, the client would have to manually report every single sale to the tax authority — which is impossible at scale. This automates the entire thing.

**What happens if ETA is down?**

Our system queues the invoice and retries later. We never block the buyer's order just because the tax system is temporarily unavailable. The buyer gets their confirmation instantly, and the invoice gets submitted in the background whenever ETA comes back online.

Short version: it's the legal tax reporting system for Egypt. Every sale must be reported to the government automatically. Our backend does this silently in the background after each order.

**Purpose:** Real-time e-invoice submission for all taxable sales. Legal requirement in Egypt.

**Where it integrates:** Celery background task triggered on order confirmation. If ETA is down, queue for retry.

**Paid/Free:** FREE API from government. But requires USB security token (costs \~2000-3000 EGP) for digital signing.

**Who provides:** CLIENT handles registration. This is a legal/tax matter for their Egyptian company.

**What client must do:**

1\. Register on ETA portal (invoicing.eta.gov.eg)

2\. Get taxpayer digital profile set up

3\. Register the ERP system (our platform) on ETA portal to get Client ID and Secret

4\. Obtain electronic seal USB token from Egypt Trust or authorised provider

5\. Get ETA pre-production (sandbox) access for testing

6\. Generate EGS (Egyptian Goods & Services) codes for all product categories OR use GS1 barcodes

**What we need from client:**

ETA Client ID, ETA Client Secret, USB Token access (or cloud HSM), Pre-production credentials, Tax registration number, Branch codes

**API integration approach:**

Use ETA SDK documentation at sdk.invoicing.eta.gov.eg. Submit invoices as JSON with CADES-BES digital signature. We build this as a Celery task that runs after order confirmation. If ETA rejects, log error and queue for admin review.

*IMPORTANT: This is the most complex integration. We recommend the client engages an Egyptian tax consultant to handle the registration side. Our job is only the API integration after credentials are received.*

# **5\. Payment Gateway (Paymob)**

## **5.1 Why Paymob**

Paymob is the leading payment gateway in Egypt. It supports Visa/Mastercard in EGP, is PCI-DSS certified, has developer-friendly APIs, and the SOW explicitly names it as the payment provider.

## **5.2 Pricing**

Transaction fee: 2.75% \+ 3 EGP per transaction. No monthly fee. No setup fee. Weekly settlement to client bank account.

## **5.3 Supported Payment Methods**

Visa and Mastercard (online card payments), Cash on Delivery (COD handled by our platform logic, not Paymob). Meeza (Egyptian local card network) available if client requests.

## **5.4 Registration (Client Must Do This)**

**Step-by-step:**

1\. Go to accept.paymob.com/portal2/en/register

2\. Fill in business details: business name, business type, email, phone

3\. Upload required documents:

   a. Valid Commercial Register (Egyptian سجل تجاري)

   b. Tax Card copy (بطاقة ضريبية)

   c. Owner/Director National ID copy

   d. Bank account details for settlement

4\. Choose payment methods to activate (Card payments at minimum)

5\. Wait for document verification (up to 3 business days)

6\. Once approved, client gets access to Paymob dashboard

## **5.5 What We Need from Client After Approval**

From Paymob dashboard \> Settings:

1\. API Key (Settings \> Account Info \> View API Key)

2\. Secret Key

3\. Public Key

4\. HMAC Secret (for webhook verification)

5\. Integration ID for Card payments (Developers \> Payment Integrations)

6\. iFrame ID (Developers \> iFrames)

Client should set up Test Mode first. We integrate with sandbox, then switch to Live.

## **5.6 Integration Flow**

**Step 1: Create Payment Intention**

POST https://accept.paymob.com/v1/intention/

Headers: Authorization: Token {SECRET\_KEY}

Body: { amount: 45000, currency: 'EGP',

  payment\_methods: \[INTEGRATION\_ID\],

  billing\_data: { first\_name, last\_name, email, phone,

    city, country: 'EG', state: 'Cairo' },

  items: \[{ name, amount, quantity }\] }

**Step 2: Redirect Buyer**

Paymob returns a client\_secret. Frontend redirects buyer to Paymob hosted checkout page using the client\_secret. Buyer enters card details on Paymob page (PCI compliant, no card data touches our servers).

**Step 3: Webhook Callback**

Paymob sends POST to our callback URL with transaction result. We verify HMAC signature and update order payment\_status.

POST /webhooks/paymob

Verify HMAC: compute HMAC-SHA512 of sorted response fields using HMAC Secret. Compare with Paymob header.

**Step 4: Handle COD**

For Cash on Delivery: no Paymob call. Set payment\_method \= 'cod', payment\_status \= 'pending'. Seller collects cash. After delivery confirmed, admin or system marks payment as collected.

## **5.7 Refunds**

POST https://accept.paymob.com/api/acceptance/void\_refund/refund

Body: { transaction\_id, amount\_cents }

Used when admin approves a return request with refund.

## **5.8 Environment Variables**

PAYMOB\_API\_KEY=...

PAYMOB\_SECRET\_KEY=...

PAYMOB\_PUBLIC\_KEY=...

PAYMOB\_HMAC\_SECRET=...

PAYMOB\_CARD\_INTEGRATION\_ID=...

PAYMOB\_IFRAME\_ID=...

# **6\. AI Services (OpenAI)**

We use OpenAI for three specific features. All are powered by GPT-4o-mini for cost efficiency.

## **6.1 AI-Powered Search**

**What:** When Elasticsearch returns poor results (\< 3 matches or low relevance score), use OpenAI to understand buyer intent and rewrite the query.

**Where:** Search service, called as fallback after Elasticsearch.

**How it works:**

1\. Buyer searches: القطعة اللي بتوقف العربية (the thing that stops the car)

2\. Elasticsearch returns 0 results

3\. Call OpenAI: given this Egyptian Arabic query, what auto part is the buyer looking for?

4\. OpenAI returns: brake pad (فحة فرامل / تيل فرامل)

5\. Re-run Elasticsearch with translated terms

**Implementation:**

System prompt: You are an Egyptian automotive parts expert.

Given a search query in Egyptian Arabic, return the formal

Arabic and English part name. Reply in JSON only:

{ "formal\_ar": "...", "english": "...", "category": "..." }

## **6.2 Arabic Colloquial Name Generation**

**What:** Help admin populate the colloquial\_names table by suggesting Egyptian slang names for formal part names.

**Where:** Admin panel, bulk tool for generating colloquial mappings.

**Implementation:**

System prompt: You are an Egyptian mechanic who knows

all the street/slang names for car parts in Egyptian Arabic.

Given a formal part name, return the common Egyptian names.

Reply in JSON: { "suggestions": \["name1", "name2"\] }

## **6.3 Buyer Support Chatbot (Phase 2 / Optional)**

**What:** FAQ chatbot on buyer side. Answers common questions about orders, returns, vehicle compatibility.

**Where:** Chat widget on buyer pages. Backend endpoint /chat.

This is optional for launch. Build only if time permits.

## **6.4 OpenAI Setup**

**Paid/Free:** Paid. GPT-4o-mini costs $0.15 per 1M input tokens, $0.60 per 1M output tokens. Very cheap.

**Who provides:** WE sign up at platform.openai.com and get API key.

**Steps:**

1\. Create account at platform.openai.com

2\. Add billing (credit card)

3\. Generate API key

4\. Set usage limits ($50/month cap to start)

5\. Store OPENAI\_API\_KEY in env vars

**Python usage:**

pip install openai

from openai import OpenAI

client \= OpenAI(api\_key=settings.OPENAI\_API\_KEY)

response \= client.chat.completions.create(

  model='gpt-4o-mini',

  messages=\[{'role':'system','content':'...'},

            {'role':'user','content': query}\],

  response\_format={'type':'json\_object'})

# **7\. POC (Proof of Concept) Checklist**

Before building any feature, complete these POCs to validate integrations work. Each POC should take 2-4 hours max. Document results in a shared folder.

| \# | POC Name | What to Prove | Priority | Est. Hours |
| :---- | :---- | :---- | :---- | :---- |
| 1 | TecDoc API Sync | Fetch 10 manufacturers, 50 models, 100 articles. Parse response. Store in PostgreSQL. Verify data structure. | P0 \- Day 1 | 4 |
| 2 | TecDoc VIN Decode | Decode 3 known VINs. Verify vehicle identification accuracy. Test NHTSA fallback. | P0 \- Day 1 | 2 |
| 3 | Paymob Card Payment | Create intention, redirect to hosted checkout, complete test payment (sandbox), receive webhook, verify HMAC. | P0 \- Day 2 | 4 |
| 4 | Paymob Refund | Refund a test transaction. Verify refund status callback. | P1 \- Day 3 | 2 |
| 5 | Bosta Create Delivery | Create a test delivery with pickup \+ delivery addresses in Cairo. Get tracking number. Check status. | P1 \- Day 3 | 3 |
| 6 | Bosta Webhook | Receive delivery status update via webhook. Parse and log. | P1 \- Day 3 | 2 |
| 7 | Elasticsearch Arabic Search | Index 100 products with Arabic names. Search with colloquial terms. Verify Arabic analyser works. | P0 \- Day 2 | 4 |
| 8 | OpenAI Search Fallback | Send 5 Egyptian slang queries. Verify JSON response with correct part identification. | P1 \- Day 4 | 2 |
| 9 | Vonage SMS OTP | Send OTP to Egyptian phone number. Verify delivery and Arabic content. | P1 \- Day 4 | 2 |
| 10 | AWS SES Email | Send test order confirmation email in Arabic \+ English from kalaax.com domain. | P1 \- Day 4 | 2 |
| 11 | Firebase FCM Push | Send test push notification to a Chrome browser. Verify lock screen delivery. | P2 \- Day 5 | 2 |
| 12 | ETA E-Invoice (Sandbox) | Submit a test invoice to ETA pre-production. Verify acceptance. (Depends on client providing credentials) | P2 \- Week 2 | 8 |
| 13 | Google OAuth | Complete Google sign-in flow. Extract email and name. Create user. | P1 \- Day 5 | 2 |
| 14 | S3 Upload \+ Pre-signed URL | Upload a test KYC document. Generate pre-signed URL. Verify 1-hour expiry. | P0 \- Day 2 | 1 |
| 15 | Redis Caching | Cache a product page response. Verify cache hit. Verify invalidation on offer update. | P1 \- Day 3 | 2 |
| 16 | OpenAI Colloquial Names | Feed 20 formal part names. Verify quality of Egyptian slang suggestions. | P2 \- Day 5 | 2 |

**POC Output Template:**

For each POC, create a file in /docs/pocs/ with: POC name, date, status (pass/fail), code snippet used, response sample, any issues found, decision made.

# **8\. Developer Quick Reference**

## **8.1 Environment Variables (.env)**

Create .env from .env.example. Never commit .env to git.

DATABASE\_URL=postgresql://user:pass@localhost:5432/kalaax

REDIS\_URL=redis://localhost:6379/0

ELASTICSEARCH\_URL=http://localhost:9200

JWT\_SECRET=\<generate-random-64-char-string\>

JWT\_ALGORITHM=HS256

TECDOC\_RAPIDAPI\_KEY=\<from-client\>

PAYMOB\_SECRET\_KEY=\<from-client-dashboard\>

PAYMOB\_HMAC\_SECRET=\<from-client-dashboard\>

PAYMOB\_CARD\_INTEGRATION\_ID=\<from-client-dashboard\>

VONAGE\_API\_KEY=\<from-vonage\>

VONAGE\_API\_SECRET=\<from-vonage\>

VONAGE\_SENDER\_ID=Kalaax

AWS\_ACCESS\_KEY\_ID=\<aws\>

AWS\_SECRET\_ACCESS\_KEY=\<aws\>

AWS\_REGION=me-south-1

AWS\_S3\_BUCKET\_PUBLIC=kalaax-public

AWS\_S3\_BUCKET\_PRIVATE=kalaax-private

OPENAI\_API\_KEY=\<from-openai\>

FIREBASE\_SERVICE\_ACCOUNT\_JSON=/path/to/firebase.json

BOSTA\_API\_KEY=\<from-client-bosta-dashboard\>

ETA\_CLIENT\_ID=\<from-client-eta-portal\>

ETA\_CLIENT\_SECRET=\<from-client-eta-portal\>

GOOGLE\_CLIENT\_ID=\<from-google-cloud-console\>

GOOGLE\_CLIENT\_SECRET=\<from-google-cloud-console\>

## **8.2 Build Order (What to Build First)**

Follow this exact order. Each step depends on the previous one.

| Week | Build | Depends On |
| :---- | :---- | :---- |
| W1 D1-3 | Project setup: Docker, FastAPI scaffold, DB models, Alembic migrations, Auth (register/login/JWT) | Nothing |
| W1 D4-5 | TecDoc sync task \+ vehicle endpoints \+ Elasticsearch setup | DB models |
| W2 D1-3 | Search API \+ product endpoints \+ Arabic search | TecDoc sync \+ ES |
| W2 D4-5 | Cart \+ Checkout \+ Paymob integration | Products \+ Auth |
| W3 D1-3 | Order management \+ sub-order split \+ commission ledger | Checkout |
| W3 D4-5 | Seller registration \+ KYC \+ document upload | Auth \+ S3 |
| W4 D1-3 | Seller inventory portal \+ offer CRUD \+ CSV upload | Seller \+ Products |
| W4 D4-5 | Multi-seller product pages \+ Buy Box ranking | Offers |
| W5 D1-3 | Bosta logistics integration \+ order dispatch \+ tracking | Orders \+ Bosta API |
| W5 D4-5 | Notification service (email \+ SMS \+ push) | Vonage \+ SES \+ FCM |
| W6 D1-2 | Returns \+ refunds (Paymob refund API) | Orders \+ Paymob |
| W6 D3-5 | Admin panel APIs \+ dashboard \+ payout batch | Everything above |
| W7 D1-3 | AI search fallback \+ colloquial name tool | Search \+ OpenAI |
| W7 D4-5 | Promo codes \+ flash sales \+ reviews \+ wishlist | Products \+ Orders |
| W8 | ETA e-invoice integration (if credentials received) | Client ETA registration |
| W8 | Testing, bug fixes, performance tuning | All features |

## **8.3 Response Envelope Standard**

**Success:**

{ "data": { ... }, "error": null, "meta": { "total": 340, "limit": 20, "offset": 0, "has\_more": true } }

**Error:**

{ "data": null, "error": { "code": "VEHICLE\_REQUIRED", "message": "Select a vehicle before adding to cart" }, "meta": null }

**Common error codes:**

| Code | HTTP Status | When |
| :---- | :---- | :---- |
| VALIDATION\_ERROR | 422 | Pydantic validation failed |
| UNAUTHORIZED | 401 | Missing or expired token |
| FORBIDDEN | 403 | Wrong role for this endpoint |
| NOT\_FOUND | 404 | Resource does not exist |
| VEHICLE\_REQUIRED | 400 | Cart action without vehicle |
| FITMENT\_MISMATCH | 400 | Part does not fit selected vehicle |
| OUT\_OF\_STOCK | 400 | Offer quantity \= 0 |
| RATE\_LIMITED | 429 | Too many requests |
| PAYMENT\_FAILED | 400 | Paymob transaction failed |
| SERVER\_ERROR | 500 | Unexpected error |

## **8.4 Elasticsearch Index Configuration**

**Index: products**

name: { type: text, analyzer: standard }

name\_ar: { type: text, analyzer: arabic }

colloquial\_name\_ar: { type: text, analyzer: arabic }

article\_number: { type: keyword }

brand: { type: keyword }

oem\_numbers: { type: keyword } (array)

category\_id: { type: keyword }

vehicle\_ids: { type: keyword } (array from fitment table)

lowest\_price: { type: integer }

offer\_count: { type: integer }

avg\_rating: { type: float }

Re-index when: TecDoc sync completes, offer created/updated/deleted, review approved.

## **8.5 Celery Task Registry**

| Task | Schedule | Queue |
| :---- | :---- | :---- |
| sync\_tecdoc\_catalogue | Daily 2:00 AM Cairo | sync |
| send\_email | On demand | notifications |
| send\_sms | On demand | notifications |
| send\_push\_notification | On demand | notifications |
| process\_payout\_batch | Weekly Sunday 6:00 AM | finance |
| submit\_eta\_invoice | On order confirmation | finance |
| check\_price\_drops\_wishlist | Daily 8:00 AM Cairo | notifications |
| update\_buy\_box\_rankings | Every 30 minutes | default |
| cleanup\_expired\_sessions | Daily midnight | default |

## **8.6 Buy Box Ranking Formula**

rank\_score \= (price\_weight \* price\_score)

           \+ (rating\_weight \* seller\_rating)

           \+ (dispatch\_weight \* dispatch\_score)

           \+ (stock\_weight \* stock\_reliability)

Default weights: price=0.5, rating=0.2, dispatch=0.2, stock=0.1

price\_score \= 1 \- (this\_price / max\_price\_in\_offers)

dispatch\_score \= 1 \- (this\_days / max\_days\_in\_offers)

Offer with highest rank\_score gets is\_buy\_box \= true.

Recalculate every 30 minutes via Celery task.

# **Final Notes**

This document covers everything you need to start building. The most important things to remember:

1\. Follow the build order in Section 8.2. Do not jump ahead.

2\. Complete POCs from Section 7 before building the actual feature.

3\. Every API endpoint must have a Pydantic model for request and response.

4\. Test in Arabic and English for every user-facing feature.

5\. All money is in piastres (integer). All timestamps in UTC.

6\. Commission ledger and payout tables are APPEND-ONLY.

7\. Never expose seller real name to buyers. Use anonymised labels.

8\. Vehicle-gated cart enforced at BOTH frontend and backend.

9\. If stuck, ask. A 5-minute question saves a rejected PR.

*End of Document*  
