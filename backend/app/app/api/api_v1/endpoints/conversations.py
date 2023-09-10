from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps
from app.models.chat import ConversationType
from app.schemas.conversation import Conversation, ConversationCreate, ConversationUpdate

# from sqlalchemy.dialects.postgresql import UUID
from uuid import UUID

router = APIRouter()


@router.get("/", response_model=List[Conversation])
def read_conversations(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    # current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve conversations.
    """
    # if crud.user.is_superuser(current_user):
    conversations = crud.conversation.get_multi(db, skip=skip, limit=limit)
  
    return conversations

@router.get("/me", response_model=List[Conversation])
def read_my_conversations(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve conversations.
    """
    # if crud.user.is_superuser(current_user):

    conversations = crud.conversation.get_multi_by_creator(
        db=db, creator_id=current_user.id, skip=skip, limit=limit
    )
    return conversations

@router.post("/", response_model=Conversation)
def create_conversation(
    *,
    db: Session = Depends(deps.get_db),
    conversation_in: ConversationCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new conversation.
    """
    conversation = crud.conversation.create(db, obj_in=conversation_in)
    # conversation = crud.conversation.create_with_creator(db=db, obj_in=conversation_in, creator_id=current_user.id)
    return conversation


@router.put("/{id}", response_model=Conversation)
def update_conversation(
    *,
    db: Session = Depends(deps.get_db),
    id: UUID,
    conversation_in: ConversationUpdate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update a conversation.
    """
    conversation = crud.conversation.get(db=db, id=id)
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    if not crud.user.is_superuser(current_user) and (conversation.creatorId != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    conversation = crud.conversation.update(db=db, db_obj=conversation, obj_in=conversation_in)
    return conversation


@router.get("/{id}", response_model=Conversation)
def read_conversation(
    *,
    db: Session = Depends(deps.get_db),
    id: UUID,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get conversation by ID.
    """
    conversation = crud.conversation.get(db=db, id=id)
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    if not crud.user.is_superuser(current_user) and (conversation.creatorId != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return conversation


@router.delete("/{id}", response_model=Conversation)
def delete_conversation(
    *,
    db: Session = Depends(deps.get_db),
    id: UUID,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete a conversation.
    """
    conversation = crud.conversation.get(db=db, id=id)
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    if not crud.user.is_superuser(current_user) and (conversation.creatorId != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    conversation = crud.conversation.remove(db=db, id=id)
    return conversation
