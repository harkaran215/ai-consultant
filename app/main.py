from fastapi import FastAPI
from app.routes import contract, approval

app = FastAPI()

app.include_router(contract.router)
app.include_router(approval.router)
