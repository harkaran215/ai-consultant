# 📄 AI Legal Ops Automation System

An end-to-end **AI-powered contract processing and approval system** built using **FastAPI, n8n, Slack, and PostgreSQL (SCD Type 2)**.

This project automates contract ingestion, risk analysis, and human approval workflows with full audit history.

---

## 🚀 Features

* 📥 Upload contracts (PDF / text)
* 🤖 AI-powered contract analysis (risk + summary)
* 🧠 Structured data extraction
* 🗃️ PostgreSQL storage with **SCD Type 2 (history tracking)**
* 🔄 Workflow automation using n8n
* 💬 Slack notifications for approvals
* ✅ Human-in-the-loop approval system
* 📊 Audit trail of all contract changes

---

## 🏗️ Architecture

```
FastAPI → AI Analyzer → PostgreSQL (SCD2)
        ↓
       n8n → Slack Notification
        ↓
User Approval (Slack)
        ↓
       n8n → FastAPI
        ↓
PostgreSQL (Update with SCD2)
```

---

## 🧰 Tech Stack

* **Backend:** FastAPI (Python)
* **AI Model:** Ollama (Mistral)
* **Workflow Automation:** n8n
* **Database:** PostgreSQL
* **Integration:** Slack Webhooks
* **PDF Processing:** pdfplumber

---

## ⚙️ Setup Instructions

### 1. Clone the repo

```
git clone <your-repo-url>
cd project
```

---

### 2. Install dependencies

```
pip install -r requirements.txt
```

---

### 3. Start PostgreSQL

Create database:

```
CREATE DATABASE legalops;
```

---

### 4. Create `contracts` table

```
CREATE TABLE contracts (
    id SERIAL PRIMARY KEY,
    contract_id UUID NOT NULL,
    vendor TEXT NOT NULL,
    value NUMERIC,
    risk_level TEXT,
    summary TEXT,
    status TEXT,
    record_hash TEXT,
    is_current BOOLEAN DEFAULT TRUE,
    start_date TIMESTAMP DEFAULT NOW(),
    end_date TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW()
);
```

---

### 5. Run FastAPI

```
uvicorn main:app --reload
```

---

### 6. Start n8n

```
n8n
```

---

### 7. Configure Slack

* Create Slack App
* Add bot to workspace
* Use Slack node in n8n
* (Optional) Configure interactivity or use URL buttons

---

## 🔁 Workflow Setup (n8n)

### Workflow 1: Contract Processing

* Webhook `/contract`
* Send Slack message with contract details

### Workflow 2: Approval

* Webhook `/approve` or `/reject`
* Call FastAPI `/approve-contract`

### Workflow 3 (Optional): Post-Approval Notification

* Send confirmation message to Slack

---

## 📡 API Endpoints

### Upload Contract

```
POST /upload-contract/
```

**Form Data:**

* `file`: contract file
* `vendor`: vendor name
* `value`: contract value

---

### Approve / Reject Contract

```
POST /approve-contract
```

**JSON Body:**

```
{
  "contract_id": "uuid",
  "status": "approved" | "rejected"
}
```

---

## 🧠 SCD Type 2 Logic

Every update creates a **new version** of the contract:

| contract_id | status   | is_current | start_date | end_date |
| ----------- | -------- | ---------- | ---------- | -------- |
| 123         | pending  | FALSE      | t1         | t2       |
| 123         | approved | TRUE       | t2         | NULL     |

---

## ⚠️ Known Limitations

* Slack buttons require public URL (ngrok recommended)
* Localhost webhooks won’t work directly with Slack
* AI output depends on prompt quality

---

## 🚀 Future Improvements

* Capture Slack user (approved_by)
* Add approval timestamps
* Build dashboard (React / Power BI)
* Improve AI clause detection
* Deploy using Docker

---

## 🎯 Use Cases

* Legal contract review automation
* Procurement approvals
* Vendor risk assessment
* Compliance tracking systems

---

## 🏁 Status

✅ Core system functional
⚠️ Slack interactive approval requires public endpoint

---

## 🤝 Contributing

Pull requests are welcome!

---

## 📜 License

MIT License
