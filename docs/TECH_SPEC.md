# TECH_SPEC.md

## Med Bridge – Technical Specification

---

## 1. Overview

**Med Bridge** is a secure, HIPAA‑compliant pipeline for transferring medical documents between client applications and a central storage service.  
The system guarantees end‑to‑end encryption, multi‑factor authentication (MFA), and real‑time transfer status updates while exposing a simple Python API (`MedBridge`) for developers.

---

## 2. Architecture

```
┌───────────────────────┐
│  Client Application    │
│  (Python SDK / UI)     │
└─────────────┬─────────┘
              │
              │ HTTPS (TLS 1.3)
              ▼
┌───────────────────────┐
│  API Gateway / Auth    │
│  (FastAPI + OAuth2)    │
└───────┬───────────────┘
        │
        │ JWT + MFA
        ▼
┌───────────────────────┐
│  MedBridge Service     │
│  (FastAPI)             │
│  • Upload/Download     │
│  • Status polling      │
│  • File metadata store │
└───────┬───────────────┘
        │
        │ S3‑compatible (MinIO) + KMS
        ▼
┌───────────────────────┐
│  Object Storage        │
│  (MinIO)               │
└───────┬───────────────┘
        │
        │ KMS‑encrypted
        ▼
┌───────────────────────┐
│  Audit & Logging       │
│  (ElasticSearch + Loki)│
└───────────────────────┘
```

* **Client** – Python SDK or web UI.  
* **API Gateway** – Handles TLS termination, rate limiting, and OAuth2 token issuance.  
* **MedBridge Service** – Core business logic, file chunking, encryption, and status tracking.  
* **Object Storage** – MinIO (S3‑compatible) with server‑side encryption via AWS KMS‑compatible key.  
* **Audit & Logging** – All events are logged to Elasticsearch; logs are streamed to Loki for Grafana dashboards.

---

## 3. Components

| Component | Responsibility | Key Libraries |
|-----------|----------------|---------------|
| **MedBridge SDK** | Provides `MedBridge.upload(file_path)` & `MedBridge.download(record_id)` | `requests`, `pyjwt`, `cryptography`, `boto3` |
| **FastAPI Service** | REST endpoints: `/upload`, `/download`, `/status` | `fastapi`, `uvicorn`, `pydantic`, `sqlalchemy` |
| **Auth Service** | OAuth2 + MFA (TOTP) | `fastapi-users`, `pyotp`, `passlib` |
| **Object Store** | Persistent, encrypted storage | `minio` SDK |
| **Audit Service** | Event ingestion & search | `elasticsearch`, `loki` |
| **CI/CD** | Automated tests & deployment | `pytest`, `docker-compose`, `GitHub Actions` |

---

## 4. Data Model

```sql
-- PostgreSQL (used for metadata)
CREATE TABLE medical_records (
    id UUID PRIMARY KEY,
    patient_id UUID NOT NULL,
    uploader_id UUID NOT NULL,
    file_name TEXT NOT NULL,
    file_size BIGINT NOT NULL,
    upload_ts TIMESTAMP WITH TIME ZONE DEFAULT now(),
    status VARCHAR(20) NOT NULL,          -- PENDING, IN_PROGRESS, COMPLETED, FAILED
    storage_key TEXT NOT NULL,            -- MinIO key
    encryption_key_id TEXT NOT NULL,      -- KMS key ID
    checksum BYTEA NOT NULL
);

CREATE TABLE audit_events (
    event_id BIGSERIAL PRIMARY KEY,
    record_id UUID,
    user_id UUID,
    event_type VARCHAR(50),
    event_ts TIMESTAMP WITH TIME ZONE DEFAULT now(),
    details JSONB
);
```

* **Encryption** – Files are encrypted client‑side with AES‑256‑GCM. The symmetric key is wrapped with a KMS‑managed key and stored in the `encryption_key_id` field.  
* **Checksum** – SHA‑256 of the plaintext file to detect corruption.

---

## 5. Key APIs / Interfaces

| Endpoint | Method | Request | Response | Notes |
|----------|--------|---------|----------|-------|
| `/auth/token` | POST | `{ "username": "", "password": "" }` | `{ "access_token": "", "token_type": "bearer" }` | OAuth2 password grant |
| `/auth/mfa` | POST | `{ "token": "", "totp": "123456" }` | `{ "access_token": "", "token_type": "bearer" }` | MFA step |
| `/upload` | POST | `multipart/form-data` (`file`, `patient_id`) | `{ "record_id": "", "status": "PENDING" }` | Streams file, returns record ID |
| `/download/{record_id}` | GET | `Authorization: Bearer <token>` | `application/octet-stream` | Decrypts on the fly |
| `/status/{record_id}` | GET | `Authorization: Bearer <token>` | `{ "status": "", "progress": 0-100 }` | Polling endpoint |

All endpoints require a valid JWT. The SDK wraps these calls and handles retries, back‑off, and decryption.

---

## 6. Tech Stack

| Layer | Technology | Rationale |
|-------|------------|-----------|
| **API** | FastAPI | Modern async framework, automatic OpenAPI docs |
| **Auth** | fastapi-users + pyotp | Built‑in MFA support, OAuth2 |
| **Storage** | MinIO (S3‑compatible) | Open‑source, self‑hosted, KMS integration |
| **Encryption** | cryptography (AES‑GCM) | Proven library, strong defaults |
| **Database** | PostgreSQL | ACID, JSONB for audit |
| **Audit** | Elasticsearch + Loki | Full‑text search, log aggregation |
| **CI** | pytest, GitHub Actions | Test coverage, Docker builds |
| **Deployment** | Docker Compose (dev), Helm (prod) | Consistent environments |

---

## 7. Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| fastapi | ^0.110.0 | API framework |
| uvicorn | ^0.27.0 | ASGI server |
| pydantic | ^2.6.0 | Data validation |
| fastapi-users | ^12.0.0 | Auth & MFA |
| pyotp | ^2.9.0 | TOTP generation |
| cryptography | ^41.0.0 | AES‑GCM encryption |
| boto3 | ^1.34.0 | MinIO SDK |
| sqlalchemy | ^2.0.0 | ORM |
| psycopg2-binary | ^2.9.0 | PostgreSQL driver |
| elasticsearch | ^8.10.0 | Audit logs |
| loki | ^2.8.0 | Log aggregation |
| pytest | ^8.0.0 | Unit tests |
| docker-compose | ^2.20.0 | Local dev stack |

All dependencies are pinned in `requirements.txt` and `pyproject.toml`.

---

## 8. Deployment

### 8.1 Local Development

```bash
# Spin up services
docker compose up -d

# Run tests
pytest
```

### 8.2 Production

1. **Infrastructure** – Kubernetes cluster (EKS/GKE/Azure AKS).  
2. **Helm Chart** – `med-bridge/helm/med-bridge` contains deployments for:
   * FastAPI service
   * MinIO (statefulset)
   * PostgreSQL (statefulset)
   * Elasticsearch + Loki (statefulsets)
   * Ingress with TLS termination (cert-manager)
3. **Secrets** – Stored in Kubernetes Secrets:
   * `MEDBRIDGE_DB_URL`
   * `MEDBRIDGE_MINIO_ENDPOINT`
   * `MEDBRIDGE_MINIO_ACCESS_KEY`
   * `MEDBRIDGE_MINIO_SECRET_KEY`
   * `MEDBRIDGE_KMS_KEY_ID`
4. **CI/CD** – GitHub Actions pipeline:
   * Lint (`ruff`, `black`)
   * Unit tests (`pytest`)
   * Build Docker image
   * Push to registry (DockerHub/GCR)
   * Helm upgrade via `helm upgrade --install`

### 8.3 Scaling

* **Stateless API** – Horizontal pod autoscaler based on CPU/Memory.  
* **MinIO** – Distributed mode with erasure coding.  
* **PostgreSQL** – Patroni for HA, read replicas for audit queries.  
* **Audit** – Elasticsearch cluster with shard replication.

---

## 9. Security & Compliance

| Requirement | Implementation |
|-------------|----------------|
| **HIPAA** | All data at rest encrypted (AES‑256), encryption keys managed by KMS, audit logs immutable. |
| **End‑to‑End Encryption** | Client encrypts file before upload; server stores ciphertext only. |
| **MFA** | TOTP via `pyotp`; enforced on token issuance. |
| **Transport Security** | TLS 1.3 enforced on all endpoints. |
| **Access Control** | Role‑based access via OAuth2 scopes (`upload`, `download`, `audit`). |
| **Audit Trail** | Every upload/download/status change logged to Elasticsearch. |
| **Data Retention** | Configurable retention policy in PostgreSQL and MinIO; automatic purge via cron job. |

---

## 10. Testing Strategy

| Layer | Tests |
|-------|-------|
| **Unit** | `pytest` for SDK, encryption helpers, auth handlers. |
| **Integration** | FastAPI test client for `/upload`, `/download`, `/status`. |
| **E2E** | Docker Compose stack; simulate client uploads, verify storage, audit logs. |
| **Security** | OWASP ZAP scan, static analysis (`bandit`). |
| **Performance** | Locust load tests on `/upload` and `/download`. |

All tests must pass before merging to `main`. Coverage target: ≥90%.

---

## 11. Roadmap (Next 3 Months)

1. **Feature** – Support chunked uploads for >1 GB files.  
2. **Feature** – Implement WebSocket status updates.  
3. **Feature** – Add role‑based UI for auditors.  
4. **Ops** – Move to serverless MinIO on AWS S3 for cost savings.  
5. **Ops** – Implement automated key rotation for KMS keys.

---

## 12. Glossary

| Term | Definition |
|------|------------|
| **KMS** | Key Management Service – used to wrap/unwrap encryption keys. |
| **S3‑compatible** | API compatible with Amazon S3; allows using MinIO. |
| **JWT** | JSON Web Token – bearer token for API auth. |
| **MFA** | Multi‑Factor Authentication – TOTP in this project. |
| **HIPAA** | Health Insurance Portability and Accountability Act – U.S. privacy law. |

---
