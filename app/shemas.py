from pydantic import BaseModel


class OperationRequest(BaseModel):
    operationType: str
    amount: int


class WalletResponse(BaseModel):
    wallet_uuid: str
    balance: int
