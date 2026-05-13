# Egyptian Tax Authority (ETA) E-Commerce API Documentation

## What is this Service?

This is the **Egyptian Tax Authority (ETA) E-Commerce API** — pre-production environment. Egypt made it mandatory for e-commerce platforms to validate sellers/taxpayers through their **TRN (Tax Registration Number)** before they can legally sell online.

Your API has to verify that the merchant is a registered Egyptian taxpayer via OTP. Super common for any platform operating in Egypt (think Amazon.eg, Noon, Jumia, etc).

**Base URL:** `https://api-ecommercetest.eta.gov.eg`

---

## Table of Contents

1. [API 1: RequestAccessToken (OAuth2 Login)](#1-requestaccesstoken-oauth2-login)
2. [API 2: ValidateTaxPayerAndSendOTP](#2-validatetaxpayerandsendotp)
3. [API 3: ValidateTaxPayerOTP](#3-validatetaxpayerotp)
4. [Integration Flow](#integration-flow)
5. [FastAPI Integration Plan](#fastapi-integration-plan)
6. [Key Points to Remember](#key-points-to-remember)

---

## The 3 APIs — Full Flow

### 1. RequestAccessToken (OAuth2 Login)

**Endpoint:** `POST /asg/tax/ecom/RequestAccessToken`

**Full URL:** `https://api-ecommercetest.eta.gov.eg/asg/tax/ecom/RequestAccessToken`

**Purpose:** Auth handshake. You send client credentials, get back a bearer token (valid **300s / 5 min**).

**Authentication:** None (this IS the auth endpoint)

**Request Body:**
```json
{
  "client_id": "200020298-649049fd0396c8-35269236",
  "client_secret": "y4A0H1GjO4C1ivYZsVV50SyE5VgHa5dTWADi0UCs/vFBk50sDbe8xiAMOmHCAEJ3m4Y=",
  "grant_type": "password",
  "CorrelationId": "111122223333545"
}
```

**Request Fields:**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `client_id` | string | Yes | Your ETA-issued client ID |
| `client_secret` | string | Yes | Your ETA-issued client secret |
| `grant_type` | string | Yes | Always `"password"` |
| `CorrelationId` | string | Yes | Unique ID for request tracing |

**Success Response (200 OK):**
```json
{
  "access_token": "eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIi...",
  "expires_in": 300,
  "refresh_expires_in": 1800,
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCIgOiAiSldUI...",
  "token_type": "bearer",
  "not-before-policy": 0,
  "session_state": "54c3dbb8-8c4e-4f3c-b434-32dc90c77b43",
  "scope": "email profile"
}
```

**Response Fields:**
| Field | Type | Description |
|-------|------|-------------|
| `access_token` | string | JWT bearer token for subsequent API calls |
| `expires_in` | integer | Access token lifetime in seconds (300s / 5 min) |
| `refresh_expires_in` | integer | Refresh token lifetime in seconds (1800s / 30 min) |
| `refresh_token` | string | Token to refresh access without re-auth |
| `token_type` | string | Always `"bearer"` |
| `session_state` | string | Session identifier |
| `scope` | string | Granted scopes |

---

### 2. ValidateTaxPayerAndSendOTP

**Endpoint:** `POST /asg/tax/validateTaxPayerAndsendOTP`

**Full URL:** `https://api-ecommercetest.eta.gov.eg/asg/tax/validateTaxPayerAndsendOTP`

**Purpose:** Send taxpayer's **TRN** → ETA validates it exists + sends OTP to their registered phone/email.

**Authentication:** Bearer token (from API 1)

**Headers:**
```
Authorization: Bearer <access_token>
Content-Type: application/json
```

**Request Body:**
```json
{
  "validateTaxPayerAndsendOTPRequest": {
    "correlationId": "aa702c17-a342-42b4-b87d-624c0a654c8c",
    "trn": "200020298"
  }
}
```

**Request Fields:**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `validateTaxPayerAndsendOTPRequest.correlationId` | string (UUID) | Yes | Unique ID for request tracing |
| `validateTaxPayerAndsendOTPRequest.trn` | string | Yes | Taxpayer's Tax Registration Number |

**Success Response:**
Returns an `identifier` (UUID) — you need this for step 3 (OTP verification).

---

### 3. ValidateTaxPayerOTP

**Endpoint:** `POST /asg/tax/validateTaxPayerOTP`

**Full URL:** `https://api-ecommercetest.eta.gov.eg/asg/tax/validateTaxPayerOTP`

**Purpose:** User enters OTP → you verify it with the `identifier` from step 2.

**Authentication:** Bearer token (from API 1)

**Headers:**
```
Authorization: Bearer <access_token>
Content-Type: application/json
```

**Request Body:**
```json
{
  "validateTaxPayerOTPRequest": {
    "correlationId": "0483f175-f8c9-409a-b504-1d3d49751ddf",
    "identifier": "4b39792f-6c19-4389-85d5-084809915d01",
    "otp": 666666
  }
}
```

**Request Fields:**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `validateTaxPayerOTPRequest.correlationId` | string (UUID) | Yes | Unique ID for request tracing |
| `validateTaxPayerOTPRequest.identifier` | string (UUID) | Yes | The identifier returned from API 2 |
| `validateTaxPayerOTPRequest.otp` | integer | Yes | The 6-digit OTP entered by the user |

**Success Response:**
Taxpayer verified — you can onboard them into your platform.

---

## Integration Flow

```
┌──────────────┐                ┌──────────────┐                ┌──────────────┐
│   Frontend   │                │ Your Backend │                │   ETA API    │
└──────┬───────┘                └──────┬───────┘                └──────┬───────┘
       │                               │                               │
       │  1. User enters TRN           │                               │
       │──────────────────────────────>│                               │
       │                               │  2. Get/Refresh Access Token  │
       │                               │──────────────────────────────>│
       │                               │<──────────────────────────────│
       │                               │                               │
       │                               │  3. validateTaxPayerAndSendOTP│
       │                               │──────────────────────────────>│
       │                               │<──────────────────────────────│
       │                               │    (returns identifier)       │
       │  4. Return verification UUID  │                               │
       │<──────────────────────────────│                               │
       │                               │                               │
       │  5. User enters OTP           │                               │
       │──────────────────────────────>│                               │
       │                               │  6. validateTaxPayerOTP       │
       │                               │──────────────────────────────>│
       │                               │<──────────────────────────────│
       │                               │    (verified!)                │
       │  7. Success / onboarded       │                               │
       │<──────────────────────────────│                               │
```

### Step-by-Step Breakdown

1. **Frontend** → calls your `POST /api/eta/send-otp` with `trn`
2. **Your Backend** → grabs cached access token (or refreshes if expired), calls ETA's `validateTaxPayerAndsendOTP`, stores `identifier` in DB, returns verification UUID to frontend
3. **Frontend** → user enters OTP → calls your `POST /api/eta/verify-otp` with OTP + verification UUID
4. **Your Backend** → fetches `identifier` from DB, calls ETA's `validateTaxPayerOTP`, marks user as verified

---

## FastAPI Integration Plan

### Project Structure

```
routers/eta_tax.py          # 2 endpoints: send-otp, verify-otp
models/eta_verification.py  # DB model to track verifications
services/eta_service.py     # Token caching + all 3 ETA API calls
schema/schemas.py           # Request/response schemas + enums
config.py                   # ETA_BASE_URL, ETA_CLIENT_ID, ETA_CLIENT_SECRET
```

### Config (config.py)

```python
# ==================== EGYPTIAN TAX AUTHORITY (ETA) CONFIGURATION ====================
ETA_BASE_URL: str = Field(default="https://api-ecommercetest.eta.gov.eg", description="ETA API base URL")
ETA_CLIENT_ID: str = Field(default="", description="ETA OAuth client ID")
ETA_CLIENT_SECRET: str = Field(default="", description="ETA OAuth client secret")
ETA_GRANT_TYPE: str = Field(default="password", description="ETA OAuth grant type")
```

### Your Backend Endpoints (routers/eta_tax.py)

| Method | Endpoint | Purpose |
|--------|----------|---------|
| `POST` | `/api/eta/send-otp` | Initiates TRN validation, sends OTP to taxpayer |
| `POST` | `/api/eta/verify-otp` | Verifies the OTP entered by the user |

### Database Table

```sql
CREATE TABLE eta_verifications (
    eta_verification_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(user_id),
    trn VARCHAR(50) NOT NULL,
    identifier UUID,
    correlation_id UUID NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'pending', -- pending, verified, failed, expired
    verified_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_eta_verifications_trn ON eta_verifications(trn);
CREATE INDEX idx_eta_verifications_user_id ON eta_verifications(user_id);
```

### Service Layer Responsibilities (services/eta_service.py)

- **Token caching**: Store access token in memory (or Redis) with expiry tracking. Only refresh when expired.
- **`get_access_token()`**: Returns cached token or fetches new one
- **`send_otp(trn, correlation_id)`**: Calls ETA API 2, returns identifier
- **`verify_otp(identifier, otp, correlation_id)`**: Calls ETA API 3, returns verification result
- Use **httpx** async client for all HTTP calls

---

## Key Points to Remember

### Must-Do's

- **Token caching** — token only lasts 5 min. Cache in memory (or Redis) and refresh when needed. Don't hit `RequestAccessToken` on every call
- **CorrelationId** — generate a fresh UUID per request using `uuid.uuid4()` for tracing
- **Never hardcode `client_secret`** — put it in `.env` → `config.py`
- **Store verifications** — table with `trn`, `identifier`, `status` (pending/verified/failed), `correlation_id`, `created_at`
- **Handle OTP expiry** — gracefully with proper error codes
- **Use httpx async client** — not `requests` (sync blocks the event loop)
- **Abstract behind a service class** — e.g., `ETAService`. Don't let raw httpx calls leak into routers

### Security Considerations

- Client credentials MUST be in `.env` file (never commit)
- Rotate tokens securely — don't log access tokens
- Validate TRN format on the frontend AND backend before calling ETA
- Rate limit your own endpoints (`@limiter.limit("5/minute")` for OTP endpoints to prevent abuse)
- Log failed attempts for audit trail but never log the OTP or token values

### Token Lifecycle

| Token | Lifetime | Use |
|-------|----------|-----|
| `access_token` | 300s (5 min) | Used in `Authorization: Bearer` header |
| `refresh_token` | 1800s (30 min) | Use to get new access token without re-auth |

### Error Handling

Map ETA error responses to your app's error codes:
- Invalid TRN → `400 BAD_REQUEST`
- Taxpayer not found → `404 NOT_FOUND`
- Expired/invalid OTP → `400 BAD_REQUEST` with `OTP_INVALID` code
- ETA service down → `502 BAD_GATEWAY` with `EXTERNAL_SERVICE_ERROR` code
- Rate limit on ETA side → `429 TOO_MANY_REQUESTS`

---

## API Summary Table

| # | API Name | Method | Endpoint | Auth Required | Purpose |
|---|----------|--------|----------|---------------|---------|
| 1 | RequestAccessToken | POST | `/asg/tax/ecom/RequestAccessToken` | No | Get OAuth bearer token |
| 2 | ValidateTaxPayerAndSendOTP | POST | `/asg/tax/validateTaxPayerAndsendOTP` | Bearer | Send OTP to taxpayer |
| 3 | ValidateTaxPayerOTP | POST | `/asg/tax/validateTaxPayerOTP` | Bearer | Verify the OTP |

---

## Source

Based on the Postman collection: **ECommerce ETA PreProd** (`tex-service.json`)
