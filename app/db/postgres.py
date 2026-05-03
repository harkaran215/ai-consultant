import psycopg2
import os

def load_sql(file_path: str) -> str:
    with open(file_path, "r") as f:
        return f.read()


def upsert_contract_scd2(record: dict, operation: str = "insert"):

    conn = psycopg2.connect(
    dbname=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT")
)

    cursor = conn.cursor()

    try:
        with open("app\db\queries\TableRefresh.sql", "r") as f:
            query = f.read()

        params = {
            "contract_id": record.get("contract_id"),
            "vendor": record.get("vendor"),
            "value": record.get("value"),
            "risk_level": record.get("risk_level"),
            "status": record.get("status", "pending"),
            "operation": operation
        }

        cursor.execute(query, params)
        conn.commit()

    except Exception as e:
        conn.rollback()   # 🔥 THIS FIXES YOUR ERROR
        raise e           # rethrow so FastAPI shows real issue

    finally:
        cursor.close()
        conn.close()