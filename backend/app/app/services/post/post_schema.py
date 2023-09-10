from app.models.post_model import PostBase
from app.models.user_model import UserBase, UserSimpleBase
from app.models.comment_model import CommentBase
from app.models.tag_model import TagBase
from app.models.style_model import StyleBase
# from app.schemas.user_schema import IUserSimpleRead
from app.utils.partial import optional
from typing import List, Optional
from uuid import UUID
from sqlmodel import SQLModel


class IPostCreate(PostBase):
    pass

class IPostCreateWithUser(PostBase):
    created_by_id: UUID
 

# All these fields are optional
@optional
class IPostUpdate(PostBase):
    pass


class IPostRead(PostBase):
    id: UUID
    styles: Optional[List[StyleBase]]
    tags: Optional[List[TagBase]]
    # tags: Optional[List[TagBase]]


class IPostReadWithUser(IPostRead):
    created_by: UserBase


class IUserSimpleRead(SQLModel):
    id: UUID


class IPostReadWithUserSimple(IPostRead):
    # id: Optional[UUID]
    created_by: UserSimpleBase
    # likes: Optional[List[IUserSimpleRead]]
    likes: Optional[List[IUserSimpleRead]]
    
    
class IPostReadWithUserComments(IPostRead):
    created_by: UserSimpleBase
    comments: Optional[List[CommentBase]]
    # comments: List[CommentBase]
    
    
class IPostReadWithComments(IPostRead):
    comments: Optional[List[CommentBase]]
    # comments: List[CommentBase]
    
class IPostReadwithUserCommentsLikes(IPostRead):
    created_by: UserSimpleBase
    comments: Optional[List[CommentBase]]
    likes: List[IUserSimpleRead]

    
class IPostReadWithUserTags(IPostRead):
    created_by: UserSimpleBase
    
