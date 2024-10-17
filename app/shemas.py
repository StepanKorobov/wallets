from pydantic import BaseModel


class OperationRequest(BaseModel):
    operationType: str
    amount: int | float


class WalletResponse(BaseModel):
    wallet_uuid: str
    balance: int | float
