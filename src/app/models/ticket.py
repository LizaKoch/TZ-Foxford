from datetime import datetime
from enum import Enum as PythonEnum
from typing import Optional

from sqlalchemy import (
    Enum,
    ForeignKey,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.app.core.db import Base
from src.app.models.client import Client
from src.app.models.user import User
from src.app.models.message import Message

class TicketStatus(PythonEnum):
    OPEN = 'Открыт'
    IN_PROGRESS = 'В работе'
    CLOSED = 'Закрыт'

class Ticket(Base):
    __tablename__ = 'tickets'
    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True,
        autoincrement=True,
    )
    status: Mapped[Enum] = mapped_column(
        Enum(TicketStatus), nullable=False, default=TicketStatus.OPEN,
    )

    client_id: Mapped[int] = mapped_column(ForeignKey('clients.id'))
    client: Mapped['Client'] = relationship(back_populates='tickets')

    employee_id: Mapped[int | None] = mapped_column(ForeignKey('user.id'))
    employee: Mapped[Optional['User']] = relationship(back_populates='tickets')

    messages: Mapped[list['Message']] = relationship(back_populates='ticket')

    created_at: Mapped[datetime] = mapped_column(
        nullable=False,
        default=func.now(),
    )
    updated_at: Mapped[datetime] = mapped_column(
        nullable=False,
        default=func.now(),
        onupdate=func.now(),
    )
    completed_at: Mapped[datetime | None] = mapped_column(nullable=True)
