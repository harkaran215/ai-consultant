from fastapi import APIRouter, UploadFile, File, Form
from fastapi.responses import JSONResponse
import uuid
from datetime import datetime
import io

import pdfplumber

# Internal
from app.ai.analyzer import analyze_contract
from app.db.postgres import upsert_contract_scd2
from app.utils.hashing import generate_hash

from app.integration.n8n_client import send_to_n8n

router = APIRouter()


# 🔍 Extract text
async def extract_text(file: UploadFile) -> str:
    content = await file.read()

    if file.filename.endswith(".pdf"):
        text = ""
        with pdfplumber.open(io.BytesIO(content)) as pdf:
            for page in pdf.pages:
                text += page.extract_text() or ""
        return text

    return content.decode("utf-8", errors="ignore")


@router.post("/upload-contract/")
async def upload_contract(
    file: UploadFile = File(...),
    vendor: str = Form(...),
    value: float = Form(...)
):
    try:
        # 1. Extract text
        text = await extract_text(file)

        if not text.strip():
            return JSONResponse(
                {"error": "Could not extract text"},
                status_code=400
            )

        # 2. Generate ID
        contract_id = str(uuid.uuid4())

        # 3. AI analysis
        analysis = analyze_contract(text)

        # 4. Build record
        record = {
        "contract_id": contract_id,
        "vendor": vendor,
        "value": value,
        "risk_level": analysis.get("risk_level", "Unknown"),
        "summary": analysis.get("summary", ""),   # 🔥 ADD THIS LINE
        "status": "pending",
        "created_at": datetime.utcnow().isoformat()
    }

        # 5. Hash (optional but good)
        record["record_hash"] = generate_hash(record)

        # 6. Insert (SCD2 - insert mode)
        upsert_contract_scd2(record, operation="insert")

        
        # 7. Trigger n8n
        send_to_n8n({
        "contract_id": contract_id,
        "vendor": vendor,
        "value": value,
        "risk_level": record["risk_level"],
        "summary": analysis.get("summary", "")
    })



        # 7. Return response
        return {
            "contract_id": contract_id,
            "analysis": analysis
        }

    except Exception as e:
        return JSONResponse(
            {"error": str(e)},
            status_code=500
        )