import pytest
from app.database.database import Wallet
from httpx import AsyncClient
from sqlalchemy.future import select

from conftest import ac, async_session_maker_test


async def test_add_user_to_db():
    """Тест на работу БД, добавляем кошельки и проверяем"""
    async with async_session_maker_test() as session:
        wallet_1 = Wallet(wallet_uuid="111")
        wallet_2 = Wallet(wallet_uuid="222")
        wallet_3 = Wallet(wallet_uuid="333")
        wallet_4 = Wallet(wallet_uuid="444")
        wallet_5 = Wallet(wallet_uuid="555")

        session.add(wallet_1)
        session.add(wallet_2)
        session.add(wallet_3)
        session.add(wallet_4)
        session.add(wallet_5)

        await session.commit()

        query = select(Wallet)
        result = await session.execute(query)
        results = result.scalars().all()
        result_json = [i.to_json() for i in results]

        wallet_json = [
            {'id': 1, 'wallet_uuid': '111', 'balance': 0},
            {'id': 2, 'wallet_uuid': '222', 'balance': 0},
            {'id': 3, 'wallet_uuid': '333', 'balance': 0},
            {'id': 4, 'wallet_uuid': '444', 'balance': 0},
            {'id': 5, 'wallet_uuid': '555', 'balance': 0}
        ]

        assert result_json == wallet_json, "no users added"
