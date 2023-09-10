from typing import Optional
from app.schemas.post_schema import IPostCreate, IPostUpdate
from datetime import datetime
from app.crud.base_crud import CRUDBase
from app.models.post_model import Post
from app.models.user_model import User
from app.models.links_model import LinkLikePost
from app.models.comment_model import Comment
from fastapi_async_sqlalchemy import db
from sqlmodel import select, func, and_
from sqlmodel.ext.asyncio.session import AsyncSession


class CRUDPost(CRUDBase[Post, IPostCreate, IPostUpdate]):
    pass
    # async def get_post_by_name(
    #     self, *, name: str, db_session: Optional[AsyncSession] = None
    # ) -> Post:
    #     db_session = db_session or db.session
    #     post = await db_session.execute(select(Post).where(Post.name == name))
    #     return post.scalar_one_or_none()

    async def get_count_of_comments(
        self,
        *,
        id, # id of the post
        start_time: datetime,
        end_time: datetime,
        db_session: Optional[AsyncSession] = None,
    ) -> int:
        db_session = db_session or db.session
        subquery = (
            select(Post)
            .join(Comment)
            .where(Post.id==id)
            .subquery()
        )
        query = select(func.count()).select_from(subquery)
        
        # query = db_session.query(func.count(Comment.id)).\
        #     join(Post, Comment.id == Post.id).\
        #     filter(Post.id == 1)
        
        count = await db_session.execute(query)
        value = count.scalar_one_or_none()
        return value
    
    async def like(
        self,
        *,
        id, # id of the post
        current_user: User,
        # user_id,
        db_session: Optional[AsyncSession] = None,
    ) -> int:

        db_session = db_session or db.session
        response = await db_session.execute(
            select(Post).where(Post.id == id)
        )
        post = response.scalar_one()
        
        # if user_id in post.likes:
        #     post.likes.remove(user_id)
        # else:   
        #     post.likes.append(user_id)

        # check if current_user exists in post.likes            
        if current_user in post.likes:
            post.likes.remove(current_user)
        else:   
            post.likes.append(current_user)
        
        post.like_count = len(post.likes)
        
        db_session.add(post)
        await db_session.commit()
        
        return post        
    
        
    async def like_by_user_id(
        self,
        *,
        id, # id of the post
        # current_user: User,
        user_id,
        db_session: Optional[AsyncSession] = None,
    ) -> int:
            
        db_session = db_session or db.session
        response = await db_session.execute(
            select(Post).where(Post.id == id)
        )
        post = response.scalar_one()
        
        response = await db_session.execute(
            select(LinkLikePost).where(LinkLikePost.post_id == id).where(LinkLikePost.user_id == user_id)   
        )
        
        likedPost = response.one_or_none()
            
        if likedPost is not None: 
            db_session.delete(likedPost)
        else:
            likedPost = LinkLikePost(post_id=id, user_id=user_id)
            db_session.add(likedPost)   
        
        post.like_count = len(post.likes)
        
        db_session.add(post)
        await db_session.commit()
        
        return post

post = CRUDPost(Post)
