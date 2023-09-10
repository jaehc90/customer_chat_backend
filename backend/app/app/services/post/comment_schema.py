from app.models.comment_model import CommentBase
from app.models.user_model import UserBase
from app.utils.partial import optional
from uuid import UUID


class ICommentCreate(CommentBase):
    pass


# All these fields are optional
@optional
class ICommentUpdate(CommentBase):
    pass


class ICommentRead(CommentBase):
    id: UUID


class ICommentReadWithUser(ICommentRead):
    user: UserBase
