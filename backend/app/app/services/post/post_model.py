from sqlmodel import Field, Relationship, SQLModel
from typing import Optional, Dict
from app.models.base_uuid_model import BaseUUIDModel
from app.models.links_model import LinkTagPost, LinkLikePost, LinkStylePost
# from app.models.like_model import LikePostLink
from app.models.comment_model import Comment
from app.models.user_model import UserSimpleBase, UserDetailed
from uuid import UUID
from typing import List



class PostBase(SQLModel):
    description: str = Field(default=None, index=False)
    post_url: str = Field(default=None, index=False)
    username: str = Field(default=None, index=False)
    prof_image: str = Field(default=None, index=False)
    like_count: Optional[int] = Field(default=0)
    


class Post(BaseUUIDModel, PostBase, table=True):
    created_by_id: Optional[UUID] = Field(default=None, foreign_key="User.id", index=True)
    created_by: "User" = Relationship(  # noqa: F821
        sa_relationship_kwargs={
            "lazy": "selectin",
            "primaryjoin": "Post.created_by_id==User.id"
        }
    )
    
    comments: List[Comment] = Relationship(  # noqa: F821
        back_populates="post", 
        sa_relationship_kwargs={"lazy": "selectin"}
    )
        
    tags: List["Tag"] = Relationship(
        back_populates="posts",
        link_model=LinkTagPost,
        sa_relationship_kwargs={"lazy": "selectin"},
    )
    
    styles: List["Style"] = Relationship(
        back_populates="posts",
        link_model=LinkStylePost,
        sa_relationship_kwargs={"lazy": "selectin"},
    )
    
    like_users: Optional[str] = Field(default="[]")
    
    likes: List["User"] = Relationship(
        back_populates="liked_posts",
        link_model=LinkLikePost,
        sa_relationship_kwargs={"lazy": "selectin"}
    )
