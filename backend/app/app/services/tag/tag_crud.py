from typing import Optional
from app.schemas.tag_schema import ITagCreate, ITagUpdate
from datetime import datetime
from app.crud.base_crud import CRUDBase
from app.models.tag_model import Tag
from app.models.post_model import Post

from fastapi_async_sqlalchemy import db
from sqlmodel import select, func, and_
from sqlmodel.ext.asyncio.session import AsyncSession


class CRUDTag(CRUDBase[Tag, ITagCreate, ITagUpdate]):
    async def get_tags_by_name(
        self, *, name: str, db_session: Optional[AsyncSession] = None
    ) -> Tag:
        db_session = db_session or db.session
        tags = await db_session.execute(select(Tag).where(Tag.name == name))
        return tags.scalar_one_or_none()

    async def get_count_of_tags(
        self,
        *,
        start_time: datetime,
        end_time: datetime,
        db_session: Optional[AsyncSession] = None,
    ) -> int:
        db_session = db_session or db.session
        subquery = (
            select(Tag)
            .where(
                and_(
                    Tag.created_at > start_time,
                    Tag.created_at < end_time,
                )
            )
            .subquery()
        )
        query = select(func.count()).select_from(subquery)
        count = await db_session.execute(query)
        value = count.scalar_one_or_none()
        return value


    async def get_count_of_posts_per_tags(
        self,
        *,
        name: str, 
        # start_time: datetime,
        # end_time: datetime,
        db_session: Optional[AsyncSession] = None,
    ) -> int:
        db_session = db_session or db.session
        # subquery = (
        #     select(Tag)
        #     .where(
        #         Tag.name == name
        #         # and_(
        #         #     Tag.created_at > start_time,
        #         #     Tag.created_at < end_time,
        #         # )
        #     )
        #     .subquery()
        # )
        # query = select(func.count()).select_from(subquery)
        
        subquery = (
            select(Tag)
            .join(Post, Tag.id == Post.tag_id)
            .where(Tag.name == name)
            .subquery()
        )
        query = select(func.count()).select_from(subquery)
        count = await db_session.execute(query)
        value = count.scalar_one_or_none()
        return value

tag = CRUDTag(Tag)
