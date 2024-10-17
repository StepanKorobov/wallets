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


async def test_get_wallet_response(ac: AsyncClient):
    """Тест отдачи баланса кошелька"""
    response = await ac.get("/api/v1/wallets/111")
    expected_response = {
        "wallet_uuid": "111",
        "balance": 0,
    }

    assert response.status_code == 200
    assert response.json() == expected_response


async def test_get_wallet_not_found(ac: AsyncClient):
    """Тест отдачи, если кошелёк не найден"""
    response = await ac.get("/api/v1/wallets/666")
    expected_response = {
        "error": "wallet 666 not found."
    }

    assert response.status_code == 404
    assert response.json() == expected_response


async def test_post_wallet_deposit_response(ac: AsyncClient):
    """Тест пополнения баланса кошелька"""
    response = await ac.post("/api/v1/wallets/111/operation",
                             json={"operationType": "DEPOSIT", "amount": 1000})
    expected_response = {
        "wallet_uuid": "111",
        "balance": 1000,
    }

    assert response.status_code == 200
    assert response.json() == expected_response


async def test_post_wallet_withdraw_response(ac: AsyncClient):
    """Тест снятия с баланса кошелька"""
    response = await ac.post("/api/v1/wallets/111/operation",
                             json={"operationType": "WITHDRAW", "amount": 1000})
    expected_response = {
        "wallet_uuid": "111",
        "balance": 0,
    }

    assert response.status_code == 200
    assert response.json() == expected_response


async def test_post_wallet_operation_not_exist(ac: AsyncClient):
    """Тест на несуществующие операции с кошельком"""
    response = await ac.post("/api/v1/wallets/111/operation",
                             json={"operationType": "UPDATING", "amount": 1000})
    expected_response = {
        'error': 'Invalid operation type.'
    }

    assert response.status_code == 400
    assert response.json() == expected_response


async def test_post_wallet_not_found(ac: AsyncClient):
    """Тест отдачи, если кошелёк не найден"""
    response = await ac.post("/api/v1/wallets/666/operation",
                             json={"operationType": "DEPOSIT", "amount": 1000})
    expected_response = {
        "error": "wallet 666 not found."
    }

    assert response.status_code == 404
    assert response.json() == expected_response


async def test_post_wallet_insufficient_funds(ac: AsyncClient):
    """Тест отдачи, если на кошелёке отрицательный баланс"""
    response = await ac.post("/api/v1/wallets/111/operation",
                             json={"operationType": "WITHDRAW", "amount": 1000})
    expected_response = {
        "error": "Insufficient funds."
    }

    assert response.status_code == 400
    assert response.json() == expected_response


async def test_post_wallet_incorrect_amount(ac: AsyncClient):
    """Тест отдачи (валидатора), при некоректном типе данных amount"""
    response = await ac.post("/api/v1/wallets/111/operation",
                             json={"operationType": "DEPOSIT", "amount": 'abc'})
    expected_response = {'detail': [{'type': 'int_parsing', 'loc': ['body', 'amount', 'int'],
                                     'msg': 'Input should be a valid integer, unable to parse string as an integer',
                                     'input': 'abc', 'url': 'https://errors.pydantic.dev/2.9/v/int_parsing'},
                                    {'type': 'float_parsing', 'loc': ['body', 'amount', 'float'],
                                     'msg': 'Input should be a valid number, unable to parse string as a number',
                                     'input': 'abc', 'url': 'https://errors.pydantic.dev/2.9/v/float_parsing'}],
                         'body': {'operationType': 'DEPOSIT', 'amount': 'abc'}}

    assert response.status_code == 422
    assert response.json() == expected_response
