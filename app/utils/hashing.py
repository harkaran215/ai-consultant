import hashlib
import json

def generate_hash(record: dict) -> str:
    safe_record = {
        "contract_id": record.get("contract_id"),
        "vendor": record.get("vendor"),
        "value": record.get("value"),
        "risk_level": record.get("risk_level"),
        "status": record.get("status"),
        "summary": record.get("summary", "")  # 👈 FIX
    }

    record_str = json.dumps(safe_record, sort_keys=True)
    return hashlib.md5(record_str.encode()).hexdigest()