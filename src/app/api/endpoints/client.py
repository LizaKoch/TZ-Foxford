from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.core.db import get_async_session
from src.app.crud.client import client_crud
from src.app.schemas.client import ClientCreate, ClientDB

router = APIRouter(
    prefix='/clients',
    tags=['Clients'],
)

@router.post(
    '/',
    response_model=ClientDB,
    response_model_exclude_none=True,
)
async def create_client(
    client: ClientCreate,
    session: AsyncSession = Depends(get_async_session),
):
    """Create a new client."""
    return await client_crud.create(client, session)
