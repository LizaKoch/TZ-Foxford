from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy.orm import Mapped, relationship

from src.app.core.db import Base


class User(SQLAlchemyBaseUserTable[int], Base):
    tickets: Mapped[list['Ticket']] = relationship(back_populates='employee')
