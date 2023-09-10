from pydantic import BaseModel
from typing import Optional

# from sqlalchemy.dialects.postgresql import UUID
from uuid import UUID
from .model import ConversationType

from datetime import datetime

# Shared properties
class ConversationBase(BaseModel):
    name: Optional[str] = None
    isGroup: Optional[bool]

# Properties to receive on conversation creation
class ConversationCreate(ConversationBase):
    name: str
    isGroup: bool
    serverId: UUID
    creatorId: UUID
    type: ConversationType
    # members: list[UUID]

# Properties to receive on conversation update
class ConversationUpdate(ConversationBase):
    pass

# Properties shared by models stored in DB
class ConversationInDBBase(ConversationBase):
    id: UUID
    createdAt: datetime
    lastMessageAt: datetime
    serverId: UUID
    creatorId: UUID
    type: ConversationType

    class Config:
        orm_mode = True

# Properties to return to client
class Conversation(ConversationInDBBase):
    serverId: UUID
    creatorId: UUID
    type: ConversationType
    pass

# Properties properties stored in DB
class ConversationInDB(ConversationInDBBase):
    pass
