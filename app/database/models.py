from typing import Dict

from sqlalchemy.engine.result import ChunkedIteratorResult
from sqlalchemy.future import select
from sqlalchemy.sql.selectable import Select

from database.database import Wallet, async_session

async def get_wallet_balance(wallet_uuid: str) -> Dict[str: str, str: int] | None:
    """
    Корутин возвращающий информацию о балансе счёта по wallet_uuid
    :param wallet_uuid: wallet_uuid
    :type wallet_uuid: str
    :return: Словарь с информацией о номере счёта и балансе
    :rtype: Dict[str: str, str: int] | None
    """
    async with async_session() as session:
        async with session.begin():
            # Запрос на получение данных
            wallet_query: Select = (
                select(Wallet)
                .filter(wallet_uuid == Wallet.wallet_uuid)
            )
            wallet_result: ChunkedIteratorResult = await session.execute(wallet_query)
            wallet: Wallet | None = wallet_result.scalars().one_or_none()

            # Если кошелёк найден
            if wallet:
                # Создаём словарь для ответа
                wallet_data: Dict[str: str, str: int] = {
                    "wallet_uuid": wallet.wallet_uuid,
                    "balance": wallet.balance,
                }

                return wallet_data

            return None

async def test():
    """Корутина которая заполняет данными БД для демонстрации"""
    async with async_session() as session:
        async with session.begin():
            wallet_query = select(Wallet)
            wallet_result = await session.execute(wallet_query)
            wallet = wallet_result.scalars().all()

            if len(wallet) == 0:
                wallet_1 = Wallet(wallet_uuid="111")
                wallet_2 = Wallet(wallet_uuid="222")
                wallet_3 = Wallet(wallet_uuid="333")
                wallet_4 = Wallet(wallet_uuid="444")
                wallet_5 = Wallet(wallet_uuid="555")

                session.add_all([wallet_1, wallet_2, wallet_3, wallet_4, wallet_5])
                await session.commit()
