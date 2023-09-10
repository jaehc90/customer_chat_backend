from sqlmodel import Field, Relationship, SQLModel
from typing import List, Optional
from .links_model import LinkTagPost
from app.models.base_uuid_model import BaseUUIDModel
from app.models.user_model import User
from uuid import UUID


class TagBase(SQLModel):
    name: str
    description: str


class Tag(BaseUUIDModel, TagBase, table=True):
    created_by_id: Optional[UUID] = Field(default=None, foreign_key="User.id")
    created_by: "User" = Relationship(
        sa_relationship_kwargs={
            "lazy": "selectin",
            "primaryjoin": "Tag.created_by_id==User.id",
        }
    )
    posts: List["Post"] = Relationship(
        back_populates="tags",
        link_model=LinkTagPost,
        sa_relationship_kwargs={"lazy": "selectin"},
    )
