## partner‑targets.md  

**Product:** **med‑bridge** – Secure, HIPAA‑grade platform for remote collaboration & medical‑data transfer between clinicians, clinics & patients.  

**Goal of Partnerships**  
| Goal | Why it matters for med‑bridge |
|------|------------------------------|
| **Compliance‑boost** | Leverage partners with built‑in PHI encryption, audit logs, and e‑signature compliance to reduce our own dev effort and increase trust. |
| **Network effects** | Embed med‑bridge in existing clinician workflows (EHR, tele‑health, imaging) so adoption is “plug‑and‑play”. |
| **Revenue‑share / Affiliate** | Capture a % of partner‑generated usage (e.g., per‑record storage, per‑API call) to accelerate topline while keeping our cost base low. |
| **Data enrichment** | Pull patient‑generated health data (wearables, labs) to make the collaboration richer and justify premium tiers. |
| **Go‑to‑market acceleration** | Partner‑led co‑marketing & joint‑sales with established SaaS vendors gives us immediate access to their sales pipelines. |

---

### 1️⃣ Integration Roadmap (12‑month horizon)

| Quarter | Milestone | Partner(s) | Integration Effort* | Primary Value‑Add (User Job) |
|---------|-----------|------------|----------------------|------------------------------|
| **Q1** | Core “Secure File Exchange” API | **Box (Enterprise)**, **Dropbox Business** | **M** (OAuth + S3‑compatible upload) | *Clinician uploads imaging, labs → patient receives secure link* |
| **Q1** | E‑Signature for consent forms | **DocuSign** | **M** (REST SDK, webhook) | *Obtain legally‑binding consent quickly* |
| **Q2** | Tele‑consultation video embed | **Twilio Video** (or **Vonage Video API**) | **L** (WebRTC, TURN/STUN, token service) | *Live video consult directly inside med‑bridge* |
| **Q2** | EMR/EHR data pull (patient summary) | **Redox** (health‑data integration platform) | **L** (FHIR mapping, HL7 bridge) | *Pull latest meds, allergies → avoid duplicate entry* |
| **Q3** | Wearable & remote monitoring data | **Apple HealthKit** / **Google Fit** (via **Human API**) | **M** (OAuth + data normalisation) | *Add vitals (HR, SpO2) to patient record* |
| **Q3** | AI‑assisted triage / note summarisation | **OpenAI GPT‑4o** (via Azure OpenAI) | **M** (prompt engineering, rate‑limit handling) | *Generate concise visit summaries for clinicians* |
| **Q4** | Billing & claims automation | **Stripe Connect** (for marketplace) + **Change Healthcare** API | **L** (PCI‑DSS compliance, claim submission) | *Close the loop – bill insurers/patients directly* |
| **Q4** | Marketplace / Affiliate program | **PartnerStack** (partner‑management SaaS) | **S** (embed referral links, track revenue share) | *Scale partner‑driven acquisition* |

\*Effort rating (relative to our internal dev capacity):  
- **S** – < 2 weeks (simple webhook/OAuth)  
- **M** – 2‑6 weeks (API SDK, data mapping, UI glue)  
- **L** – > 6 weeks (complex compliance, real‑time media, multi‑step workflows)

---

### 2️⃣ Detailed Partner List (5‑8 targets)

| # | SaaS / API | Free‑Tier / Limits (as of 2026‑06) | Integration Effort | Revenue‑Share / Affiliate | Primary User Job Solved |
|---|------------|-----------------------------------|--------------------|---------------------------|--------------------------|
| **1** | **Box (Enterprise)** | 10 GB storage, 1 TB for paid plans; API calls unlimited on free dev tier | **M** – OAuth, file‑upload SDK, webhooks | 15 % of storage fees on referral (Box Partner Program) | Secure file exchange (imaging, PDFs) |
| **2** | **DocuSign** | 100 envelopes/mo free for dev; paid plans start $25/mo | **M** – REST SDK, event webhook | 10 % of envelope revenue (DocuSign Partner) | Electronic consent & signatures |
| **3** | **Twilio Video** | 40 min video per month free; $0.0015/min thereafter | **L** – token service, TURN/STUN, UI embed | 20 % of usage revenue (Twilio RevShare) | Real‑time video consults |
| **4** | **Redox** (FHIR/HL7 integration hub) | Free sandbox with 5,000 messages/mo | **L** – mapping to multiple EHRs, compliance testing | 12 % of transaction fees (Redox Partner) | Pull patient summary from EMR |
| **5** | **Human API** (aggregates Apple HealthKit, Google Fit, wearables) | 500 API calls/mo free | **M** – OAuth, data normalisation layer | 10 % of premium data plan revenue | Add vitals & activity data to records |
| **6** | **OpenAI (Azure) – GPT‑4o** | $18 free credit (≈ 300k tokens) | **M** – prompt design, rate‑limit handling | 5 % of usage credit via Azure Marketplace | Auto‑summarise notes, triage suggestions |
| **7** | **Stripe Connect** | No fee on test mode; live fees standard (2.9 % + $0.30) | **L** – PCI‑DSS compliance, payout flows | 10 % of processing fees on referred merchants | Billing, revenue split with clinicians |
| **8** | **PartnerStack** | Free tier: up to 5 partners, 1 k clicks/mo | **S** – embed referral widget, track clicks | 20 % of partner‑generated revenue (PartnerStack) | Affiliate program to drive new clinics |

---

### 3️⃣ Prioritisation Rationale  

1. **Compliance‑first integrations** (Box, DocuSign, Redox) – they give us immediate HIPAA‑grade storage, consent, and EMR connectivity, lowering our own compliance burden.  
2. **Revenue‑share heavy** (Twilio Video, PartnerStack) – high % rev‑share and strong network effects; we can monetize per‑consultation and per‑referral.  
3. **Data enrichment** (Human API, OpenAI) – modest free tiers, but unlock premium clinical insights that justify higher subscription tiers.  
4. **Monetisation backbone** (Stripe Connect) – essential for closing the billing loop; partner‑share aligns incentives with clinicians who become “marketplaces” for their services.  

---

### 4️⃣ Next Steps for Business Development  

1. **Outreach Cadence** – Assign BD lead to contact each partner’s alliance team (Box, DocuSign, Twilio) within 2 weeks.  
2. **MVP Integration Sprint** – Parallel dev squads:  
   - Squad A: File storage + e‑signature (Q1)  
   - Squad B: Video + Redox (Q2)  
3. **Legal Review** – Draft Data‑Processing Addendum (DPA) templates for each partner; aim for sign‑off before code freeze.  
4. **Affiliate Program Launch** – Configure PartnerStack by end of Q4; create co‑branded landing pages for each partner channel.  

---  

*Prepared by Business‑Synthesis (med‑bridge)*  



---  