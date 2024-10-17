from contextlib import asynccontextmanager

from fastapi import FastAPI, status
from fastapi.responses import JSONResponse

from database.database import engine, Base, session, Wallet
from database.models import test, get_wallet_balance, update_wallet_balance, BalanceException
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
async def operation_amount(wallet_uuid: str, operation: OperationRequest):
    """Изменение баланса кошелка"""

    # Если данного типо оперции не существует
    if operation.operationType not in ("DEPOSIT", "WITHDRAW"):
        # Возвращаем ошибку
        return JSONResponse(
            content={"error": "Invalid operation type."},
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    try:
        # Обновляем кошелёк
        wallet = await update_wallet_balance(wallet_uuid=wallet_uuid,
                                             operation_type=operation.operationType,
                                             amount=operation.amount,
                                             )
        # Если кошелёк найден
        if wallet:
            # Возвращаем информацию о новом балансе
            return JSONResponse(wallet, status.HTTP_200_OK)

        # В случае, если кошелёк не найден, возвращаем ошибку
        return JSONResponse(
            content={"error": f"wallet {wallet_uuid} not found."},
            status_code=status.HTTP_404_NOT_FOUND,
        )

    # Ошибка, недостаточно средств
    except BalanceException:
        # Возвращаем ошибку
        return JSONResponse(
            content={"error": "Insufficient funds."},
            status_code=status.HTTP_400_BAD_REQUEST,
        )


@app.get("/api/v1/wallets/{wallet_uuid}", response_model=WalletResponse)
async def get_wallets(wallet_uuid: str):
    """Возвращает информацию о балансе кошелька"""

    # Получаем кошелёк
    wallet: Wallet | None = await get_wallet_balance(wallet_uuid=wallet_uuid)

    # Есои кошелёк найден
    if wallet:
        # Возвращаем инфомацию о балансе
        return JSONResponse(wallet, status.HTTP_200_OK)

    # Если кошеёлк не найден, возращаем ошибку
    return JSONResponse(
        content={"error": f"wallet {wallet_uuid} not found."},
        status_code=status.HTTP_404_NOT_FOUND,
    )
