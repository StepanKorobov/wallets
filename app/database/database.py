import os

from dotenv import load_dotenv
from sqlalchemy import Integer, String, Float
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine
from sqlalchemy.orm import (
    Mapped,
    declarative_base,
    mapped_column,
    sessionmaker,
)
from sqlalchemy.orm.decl_api import DeclarativeMeta

# загружаем переменные окружения
load_dotenv()


def get_database_url() -> str:
    """
    Функция создающая url адрес БД из переменных окружения
    :return: URL БД
    :rtype: str
    """

    db_user: str = os.getenv("TEST_DB_USER")
    db_password: str = os.getenv("TEST_DB_PASSWORD")
    db_host: str = os.getenv("TEST_DB_HOST")
    db_port: str = os.getenv("TEST_DB_PORT")
    db_name: str = os.getenv("TEST_DB_NAME")

    database_url: str = (
        f"postgresql+asyncpg://{db_user}:{db_password}@"
        f"{db_host}:{db_port}/{db_name}"
    )

    return database_url


# Получаем URL БД
DATABASE_URL: str = get_database_url()

# Создаём асинхронный движок
engine: AsyncEngine = create_async_engine(DATABASE_URL)

# Создаём генератор асинхронной сессии
async_session = sessionmaker(
    bind=engine,
    expire_on_commit=False,
    class_=AsyncSession,
)

# Создаём базу
Base: DeclarativeMeta = declarative_base()

# Создаём асинхронную сессию
session: AsyncSession = async_session()


class Wallet(Base):
    """Таблица кошёльков, содержит UUID и баланс"""

    __tablename__ = "wallets"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    wallet_uuid: Mapped[int] = mapped_column(String, unique=True)
    balance: Mapped[float] = mapped_column(Float, default=0)
