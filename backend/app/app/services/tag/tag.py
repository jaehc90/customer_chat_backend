from typing import Optional
from uuid import UUID
from app.utils.exceptions import IdNotFoundException
from fastapi import APIRouter, Depends, Query
from fastapi_pagination import Params
from app import crud
from sqlmodel import and_, select
from app.api import deps
from app.models.tag_model import Tag
from app.models.user_model import User
from app.models.post_model import Post
from app.models.links_model import LinkTagPost
from app.schemas.common_schema import IOrderEnum
from app.schemas.tag_schema import (
    ITagCreate,
    ITagRead,
    ITagReadWithPosts,
    ITagUpdate,
)
from app.schemas.base_response_schema import (
    IDeleteResponseBase,
    IGetResponseBase,
    IGetResponsePaginated,
    IPostResponseBase,
    IPutResponseBase,
    create_response,
)
from app.schemas.role_schema import IRoleEnum

router = APIRouter()


@router.get("")
async def get_tag_list(
    params: Params = Depends(),
    # current_user: User = Depends(deps.get_current_user()),
) -> IGetResponsePaginated[ITagReadWithPosts]:
    """
    Gets a paginated list of tages
    """
    tages = await crud.tag.get_multi_paginated(params=params)
    return create_response(data=tages)


@router.get("/by_created_at")
async def get_tag_list_order_by_created_at(
    order: Optional[IOrderEnum] = Query(
        default=IOrderEnum.ascendent, description="It is optional. Default is ascendent"
    ),
    params: Params = Depends(),
    # current_user: User = Depends(deps.get_current_user()),
) -> IGetResponsePaginated[ITagReadWithPosts]:
    """
    Gets a paginated list of tages ordered by created at datetime
    """
    tages = await crud.tag.get_multi_paginated_ordered(
        params=params, order_by="created_at", order=order
    )
    return create_response(data=tages)


@router.get("/{tag_id}")
async def get_tag_by_id(
    tag_id: UUID,
    # current_user: User = Depends(deps.get_current_user()),
) -> IGetResponseBase[ITagReadWithPosts]:
    """
    Gets a tag by its id
    """
    tag = await crud.tag.get(id=tag_id)
    if not tag:
        raise IdNotFoundException(Tag, tag_id)
    return create_response(data=tag)


@router.post("")
async def create_tag(
    tag: ITagCreate,
    current_user: User = Depends(
        deps.get_current_user(required_roles=[IRoleEnum.admin, IRoleEnum.manager])
    ),
) -> IPostResponseBase[ITagRead]:
    """
    Creates a new tag
    """
    tage = await crud.tag.create(obj_in=tag, created_by_id=current_user.id)
    return create_response(data=tage)


@router.put("/{tag_id}")
async def update_tag(
    tag_id: UUID,
    tag: ITagUpdate,
    current_user: User = Depends(
        deps.get_current_user(required_roles=[IRoleEnum.admin, IRoleEnum.manager])
    ),
) -> IPutResponseBase[ITagRead]:
    """
    Updates a tag by its id
    """
    current_tag = await crud.tag.get(id=tag_id)
    if not current_tag:
        raise IdNotFoundException(Tag, tag_id)
    tage_updated = await crud.tag.update(obj_new=tag, obj_current=current_tag)
    return create_response(data=tage_updated)


@router.delete("/{tag_id}")
async def remove_tag(
    tag_id: UUID,
    current_user: User = Depends(
        deps.get_current_user(required_roles=[IRoleEnum.admin, IRoleEnum.manager])
    ),
) -> IDeleteResponseBase[ITagRead]:
    """
    Deletes a tag by its id
    """
    current_tag = await crud.tag.get(id=tag_id)
    if not current_tag:
        raise IdNotFoundException(Tag, tag_id)
    tage = await crud.tag.remove(id=tag_id)
    return create_response(data=tage)


@router.get("/{tag_name}/posts")
async def get_post_list(
    tag_name: str, 
    params: Params = Depends(),
    # current_user: User = Depends(deps.get_current_user()),
) -> IGetResponsePaginated[ITagReadWithPosts]:
    """
    Lists the people who the authenticated user follows.
    """
    query = (
        select(
            Post.id,
            Post.like_count,
            Post.description,
            Post.post_url,
            Post.prof_image,
            Post.tags 
        )
        .join(LinkTagPost, Post.id == LinkTagPost.post_id)
        .join(Tag, LinkTagPost.tag_id == Tag.id)
        .where(Tag.name == tag_name)        
    )
    
    # Post.tags.any(tag_name=tag_name)    
    users = await crud.user.get_multi_paginated(query=query, params=params)
    return create_response(data=users)