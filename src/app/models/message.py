from datetime import datetime

from sqlalchemy import ForeignKey, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.app.core.db import Base
from src.app.models.user import User


class Message(Base):
    __tablename__ = 'messages'
    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True,
        autoincrement=True,
    )
    ticket_id: Mapped[int] = mapped_column(
        ForeignKey('tickets.id'),
        nullable=False,
    )
    ticket: Mapped['Ticket'] = relationship(back_populates='messages')
    text: Mapped[str] = mapped_column(Text)
    employee_id: Mapped[int | None] = mapped_column(ForeignKey(User.id))
    created_at: Mapped[datetime] = mapped_column(
        nullable=False,
        default=func.now(),
    )
