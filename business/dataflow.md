# dataflow.md  

## System Dataflow Architecture for **med‑bridge**

```
+-------------------+        +-------------------+        +-------------------+
|  External Data    |        |   Ingestion Layer |        |  Processing /    |
|  Sources          |        |   (API / Streams) |        |  Transform Tier  |
|-------------------|        |-------------------|        |-------------------|
| • EHR/EMR APIs    |  -->   | • API Gateway     |  -->   | • Validation      |
|   (FHIR, HL7)     |        |   (AuthN/Z)       |        |   Service         |
| • PACS (DICOM)    |        | • Message Queue   |        | • De‑identif.     |
| • Patient Apps    |        |   (Kafka/Rabbit)  |        |   Service         |
| • Wearables / IoT |        | • Secure FTP/S3   |        | • Encryption /   |
|   (BLE, MQTT)     |        |   (TLS)           |        |   Signing Service |
| • Lab Results API |        | • Webhooks        |        | • Format Conv.    |
| • Billing Systems |        |   (Signed JWT)    |        |   (FHIR ↔ HL7)    |
+-------------------+        +-------------------+        +-------------------+

        |                                 |                                 |
        v                                 v                                 v

+-------------------+        +-------------------+        +-------------------+
|   Storage Tier    |        |  Query / Serving  |        |   Egress to User  |
|-------------------|        |      Layer        |        |-------------------|
| • Encrypted Object|  <--   | • GraphQL / REST  |  -->   | • Web UI (React)  |
|   Store (S3)      |        |   API (AuthZ)     |        |   (TLS)           |
| • Relational DB   |        | • Search Engine   |        | • Mobile SDKs     |
|   (PostgreSQL)    |        |   (Elastic)       |        |   (iOS/Android)   |
| • Audit Log DB    |        | • Reporting /     |        | • Secure Email /  |
|   (Append‑only)   |        |   Analytics (BI)  |        |   Fax (HIPAA)     |
| • Cache (Redis)   |        |   (RBAC)          |        | • API Gateway     |
+-------------------+        +-------------------+        +-------------------+
```

### 1. External Data Sources
- **EHR/EMR Systems** – FHIR/HL7 endpoints (Epic, Cerner, etc.)  
- **PACS** – DICOM image repositories for radiology  
- **Patient Mobile Apps** – Secure WebSocket/MQTT streams from smartphones & tablets  
- **Wearables / IoT** – BLE or MQTT telemetry (heart rate, glucose)  
- **Lab Results APIs** – HL7 v2 over MLLP or FHIR LabResult resources  
- **Billing & Claims Systems** – ISO‑20022 or custom REST APIs  

All external connections require **mutual TLS** and **OAuth 2.0** client‑credential flow; scopes are limited to `read:clinical` or `write:clinical` as appropriate.

### 2. Ingestion Layer
| Component | Role | Auth / Security |
|-----------|------|-----------------|
| **API Gateway** (Kong/Envoy) | Central entry point, rate‑limit, request routing | JWT access tokens, mTLS, IP allow‑list |
| **Message Queue** (Apache Kafka) | Decouples high‑volume streams (e.g., telemetry) | SASL/SCRAM, ACLs per topic |
| **Secure File Transfer** (S3‑compatible bucket with VPC endpoint) | Bulk uploads (imaging, lab CSV) | IAM policies, bucket‑level encryption (SSE‑KMS) |
| **Webhooks Receiver** | Event callbacks from third‑party services | Signed JWT payload, replay‑nonce validation |
| **Adapter Services** (FHIR‑Adapter, DICOM‑Adapter) | Translate proprietary formats to internal canonical schema | Service‑to‑service mTLS, scoped API keys |

### 3. Processing / Transform Layer
| Service | Function | Tech |
|---------|----------|------|
| **Validation Service** | Schema & business rule checks (FHIR profiles, DICOM tags) | JSON‑Schema, custom rule engine (OPA) |
| **De‑identification Service** | PHI removal / pseudonymisation per HIPAA Safe Harbor | Python + Presidio, audit‑log of transformations |
| **Encryption / Signing Service** | End‑to‑end encryption of payloads, digital signatures for audit | AWS KMS, RSA‑PSS |
| **Format Conversion Service** | FHIR ↔ HL7 v2 ↔ DICOM encapsulation | Apache Camel routes |
| **Orchestration** (Temporal / Airflow) | Workflow management for multi‑step pipelines (e.g., ingest → validate → store) | Temporal workers with JWT auth |

All services run in **Kubernetes** pods behind a **service mesh** (Istio) enforcing **Zero‑Trust** (mTLS, RBAC).

### 4. Storage Tier
- **Encrypted Object Store** (AWS S3 + KMS) – raw files, DICOM images, large PDFs.  
- **Relational DB** (Amazon Aurora PostgreSQL) – structured clinical records, user metadata.  
- **Audit Log DB** (Append‑only PostgreSQL with pg\_audit) – immutable trail of all reads/writes.  
- **Cache** (Redis Cluster, TLS‑enabled) – session tokens, recent query results.  

All storage volumes are **encrypted at rest** (AES‑256) and **access‑controlled** via IAM roles and fine‑grained DB privileges.

### 5. Query / Serving Layer
| Component | Purpose | Auth |
|-----------|---------|------|
| **GraphQL / REST API** (Apollo Server) | Unified data access for UI & external partners | OAuth2 scopes, RBAC (role: clinician, admin, researcher) |
| **Search Engine** (ElasticSearch) | Full‑text and vector search on notes, imaging metadata | API keys + TLS |
| **Reporting / Analytics** (Metabase / Superset) | Dashboarding for usage, outcomes, compliance | SSO (SAML) with MFA |
| **Rate Limiter & Throttling** | Prevent abuse, ensure QoS | Integrated in API Gateway |

### 6. Egress to User
- **Web UI** (React + Material‑UI) – accessed over HTTPS, session managed via HttpOnly Secure cookies.  
- **Mobile SDKs** (iOS Swift, Android Kotlin) – communicate through the same GraphQL endpoint, certificate‑pinning enabled.  
- **Secure Email / Fax** – encrypted MIME for email, HIPAA‑compliant fax gateway for legacy workflows.  
- **Partner API Gateway** – external systems (e.g., referral networks) receive data via signed JWT‑protected REST endpoints.  

All egress paths enforce **least‑privilege** token scopes and **audit logging** of every data export.

---

### Auth Boundaries Overview
1. **External → Ingestion** – Mutual TLS + OAuth2 client‑credentials.  
2. **Ingestion → Processing** – Service‑mesh mTLS, OPA policies per service.  
3. **Processing → Storage** – IAM roles with least‑privilege KMS keys.  
4. **Storage → Query Layer** – DB role‑based access, token‑based API auth.  
5. **Query → User/Egress** – OAuth2 access tokens, RBAC, session cookies, MFA for privileged actions.  

---  

*End of dataflow.md*