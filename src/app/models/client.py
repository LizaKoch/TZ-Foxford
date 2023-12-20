from sqlalchemy import Integer, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.app.core.db import Base


class Client(Base):
    __tablename__ = 'clients'

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
        autoincrement=True,
    )
    telegram_id: Mapped[int] = mapped_column(
        Integer,
        index=True,
        nullable=False,
    )
    tickets: Mapped[list['Ticket']] = relationship(back_populates='client')
    __table_args__ = (UniqueConstraint('telegram_id'),)
