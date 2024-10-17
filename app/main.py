from contextlib import asynccontextmanager

from fastapi import FastAPI, status
from fastapi.responses import JSONResponse

from database.database import engine, Base, session, Wallet
from database.models import test, get_wallet_balance
from shemas import OperationRequest, WalletResponse

# Контекстный менеджер для выполнения действий
# до запуска приложения и после завершения работы
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Создаём таблицы в БД, если они не созданы
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    await test()
    yield

    # Завершаем сессию
    await session.close()
    await engine.dispose()


app = FastAPI(lifespan=lifespan)


@app.post("/api/v1/wallets/{wallet_uuid}/operation")
async def operation_amount():
    pass


@app.get("/api/v1/wallets/{wallet_uuid}", response_model=WalletResponse)
async def get_wallets(wallet_uuid: str):
    """Возвращает информацию о балансе кошелька"""

    wallet: Wallet | None  = await get_wallet_balance(wallet_uuid=wallet_uuid)

    if wallet:
        return wallet

    return JSONResponse(
        content={"error": f"wallet {wallet_uuid} not found."},
        status_code=status.HTTP_404_NOT_FOUND,
    )
