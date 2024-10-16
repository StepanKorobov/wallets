from fastapi import FastAPI

app = FastAPI()

@app.post("/api/v1/wallets/{wallet_uuid}/operation")
async def operation_amount():
    pass

@app.get("/api/v1/wallets/{wallet_uuid}")
async def get_wallets():
    pass