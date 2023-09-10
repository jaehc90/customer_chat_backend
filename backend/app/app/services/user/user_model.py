from datetime import datetime
from sqlmodel import BigInteger, Field, SQLModel, Relationship, Column, DateTime
from app.models.links_model import LinkGroupUser, LinkLikePost
from app.models.media_model import ImageMedia

from typing import List, Optional
from pydantic import EmailStr
from app.models.base_uuid_model import BaseUUIDModel
from uuid import UUID


class UserSimpleBase(BaseUUIDModel, SQLModel):
    username: str = Field(nullable=True, index=True, sa_column_kwargs={"unique": True})
    photo_url: Optional[str] = Field(nullable=True)
    is_active: bool = Field(default=True)
    is_superuser: bool = Field(default=False)
    

class UserBase(SQLModel):
    first_name: Optional[str] = Field(nullable=True) 
    last_name: Optional[str] = Field(nullable=True)
    email: EmailStr = Field(
        nullable=True, index=True, sa_column_kwargs={"unique": True}
    )
    username: str = Field(nullable=True, index=True, sa_column_kwargs={"unique": True})
    photo_url: Optional[str] = Field(nullable=True)

    is_active: bool = Field(default=True)
    is_superuser: bool = Field(default=False)
    role_id: Optional[UUID] = Field(default=None, foreign_key="Role.id")

    firebase_uid: Optional[str] = Field(nullable=True, default=None, index=True)
    
    bio: str = Field(nullable=True)
    birthdate: Optional[datetime] = Field(
        sa_column=Column(DateTime(timezone=True), nullable=True)
    )  # birthday with timezone
    phone: Optional[str]
    state: Optional[str]
    country: Optional[str]
    address: Optional[str]
    followers: Optional[str]
    following: Optional[str]


class User(BaseUUIDModel, UserBase, table=True):
    hashed_password: Optional[str] = Field(nullable=False, index=True)
    role: Optional["Role"] = Relationship(  # noqa: F821
        back_populates="users", sa_relationship_kwargs={"lazy": "selectin"}
    )
    groups: List["Group"] = Relationship(  # noqa: F821
        back_populates="users",
        link_model=LinkGroupUser,
        sa_relationship_kwargs={"lazy": "selectin"},
    )
    image_id: Optional[UUID] = Field(default=None, foreign_key="ImageMedia.id")
    image: ImageMedia = Relationship(
        sa_relationship_kwargs={
            "lazy": "selectin",
            "primaryjoin": "User.image_id==ImageMedia.id",
        }
    )
    follower_count: Optional[int] = Field(
        sa_column=Column(BigInteger(), server_default="0")
    )
    following_count: Optional[int] = Field(
        sa_column=Column(BigInteger(), server_default="0")
    )
    
    liked_posts: List["Post"] = Relationship(
        back_populates="likes",
        link_model=LinkLikePost,
        sa_relationship_kwargs={"lazy": "selectin"}
    )

    
class UserDetailed(User):
    pass
    # liked_posts: List["Post"] = Relationship(
    #     back_populates="likes",
    #     link_model=LinkLikePost,
    #     sa_relationship_kwargs={"lazy": "selectin"}
    # )
