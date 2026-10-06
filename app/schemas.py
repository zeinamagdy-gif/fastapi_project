from pydantic import BaseModel, ConfigDict
from fastapi_users import schemas
import uuid
from datetime import datetime

class Postcreate(BaseModel):
    text:str
    content:str


class PostResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    user_id: uuid.UUID
    caption: str | None
    URL: str
    filename: str
    file_type: str
    create_at: datetime

class UserRead(schemas.BaseUser[uuid.UUID]):
    pass
class UserCreate(schemas.BaseUserCreate):
    pass
class UserUpdate(schemas.BaseUserUpdate):
    pass