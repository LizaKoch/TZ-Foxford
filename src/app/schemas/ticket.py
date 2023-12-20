from datetime import date, datetime
from typing import Optional

from fastapi_filter.contrib.sqlalchemy import Filter
from pydantic import BaseModel

from src.app.models.ticket import Ticket, TicketStatus


class TicketFilter(Filter):
    status: Optional[TicketStatus] = None
    employee_id: Optional[int] = None
    created_at: Optional[date] = None
    updated_at: Optional[date] = None

    class Constants(Filter.Constants):
        """Filter constants."""

        model = Ticket


class Ticket(BaseModel):
    status: Optional[TicketStatus] = TicketStatus.OPEN


class TicketCreate(BaseModel):
    telegram_id: int
    message: str

class TicketUpdate(BaseModel):
    status: TicketStatus = TicketStatus.OPEN


class TicketDB(BaseModel):
    id: int
    status: Optional[TicketStatus] = TicketStatus.OPEN
    client_id: int
    employee_id: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        """ORM config."""

        from_attributes = True
