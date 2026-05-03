from fastapi import APIRouter
from fastapi.responses import JSONResponse

# Internal
from app.db.postgres import upsert_contract_scd2

router = APIRouter()


@router.post("/approve-contract")
def approve_contract(data: dict):
    try:
        contract_id = data.get("contract_id")
        status = data.get("status")

        if not contract_id or not status:
            return JSONResponse(
                {"error": "Missing contract_id or status"},
                status_code=400
            )

        # 🔥 SCD2 update (single function)
        upsert_contract_scd2(
            {
                "contract_id": contract_id,
                "status": status
            },
            operation="update"
        )

        return {
            "message": f"Contract {contract_id} updated to {status}"
        }

    except Exception as e:
        return JSONResponse(
            {"error": str(e)},
            status_code=500
        )