
from src.app.crud.base import CRUDBase
from src.app.models.client import Client
from src.app.schemas.client import ClientCreate


class ClientCRUD(CRUDBase[Client, ClientCreate, None]):
    pass

client_crud = ClientCRUD(Client)
