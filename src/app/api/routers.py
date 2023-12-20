from fastapi import APIRouter

from src.app.api.endpoints import (
    client_router,
    message_router,
    ticket_router,
    user_router,
)

main_router = APIRouter()
main_router.include_router(client_router)
main_router.include_router(ticket_router)
main_router.include_router(message_router)
main_router.include_router(user_router)
