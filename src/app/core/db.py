from sqlalchemy import Column, Integer
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import (
    declared_attr,
    sessionmaker,
)

from src.app.core.config import settings


class PreBase:
    @declared_attr
    def __tablename__(cls):  # noqa
        """Return the lowercase name of the class as the table name."""
        return cls.__name__.lower()

    id = Column(Integer, primary_key=True)  # noqa: A003


Base = declarative_base(cls=PreBase)

engine = create_async_engine(settings.database_url)

AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession)


async def get_async_session():
    async with AsyncSessionLocal() as async_session:
        yield async_session
