from typing import List
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
# from app.models.conversation import Conversation
from app.models.chat import ConversationType, Conversation 
from app.schemas.conversation import ConversationCreate, ConversationUpdate
from app.crud.base import CRUDBase
from uuid import UUID
# import UUID
# from sqlalchemy.dialects.postgresql import UUID


class CRUDConversation(CRUDBase[Conversation, ConversationCreate, ConversationUpdate]):
    def create_with_creator(
        self, db: Session, *, obj_in: ConversationCreate, creator_id: UUID
    ) -> Conversation:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data, creatorId=creator_id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_multi_by_creator(
        self, db: Session, *, creator_id: UUID, skip: int = 0, limit: int = 100
    ) -> List[Conversation]:
        return (
            db.query(self.model)
            .filter(Conversation.creatorId == creator_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

conversation = CRUDConversation(Conversation)
