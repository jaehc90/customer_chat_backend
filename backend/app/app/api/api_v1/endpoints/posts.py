from typing import Optional
from uuid import UUID
from app.utils.exceptions import IdNotFoundException
from fastapi import APIRouter, Depends, Query
from fastapi_pagination import Params
from app import crud
from app.api import deps
from app.models.post_model import Post
from app.models.user_model import User
from app.schemas.common_schema import IOrderEnum
from app.schemas.post_schema import (
    IPostCreate,
    IPostRead,
    IPostReadWithUser,
    IPostUpdate,
    IPostReadWithComments,
    IPostReadWithUserComments,
    IPostReadWithUserSimple, 
    IPostCreateWithUser
)
from app.schemas.base_response_schema import (
    IDeleteResponseBase,
    IGetResponseBase,
    IGetResponsePaginated,
    IPostResponseBase,
    IPutResponseBase,
    create_response,
)
from app.schemas.user_schema import IUserRead
from app.schemas.role_schema import IRoleEnum

router = APIRouter()


@router.get("")
async def get_post_list(
    order: Optional[IOrderEnum] = Query(
        default=IOrderEnum.descendent, description="It is optional. Default is descendent"
    ),
    params: Params = Depends(),
    # current_user: User = Depends(deps.get_current_user()),
) -> IGetResponsePaginated[IPostReadWithUserSimple]:
    """
    Gets a paginated list of posts
    """
    posts = await crud.post.get_multi_paginated_ordered(
        params=params, 
        order_by="created_at", 
        order=order
    )
    
    print(posts)

    return create_response(data=posts)


@router.get("/by_created_at")
async def get_post_list_order_by_created_at(
    order: Optional[IOrderEnum] = Query(
        default=IOrderEnum.ascendent, description="It is optional. Default is ascendent"
    ),
    params: Params = Depends(),
    # current_user: User = Depends(deps.get_current_user()),
) -> IGetResponsePaginated[IPostReadWithUser]:
    """
    Gets a paginated list of posts ordered by created at datetime
    """
    posts = await crud.post.get_multi_paginated_ordered(
        params=params, order_by="created_at", order=order
    )
    return create_response(data=posts)


@router.get("/like/{post_id}/user/{user_id}")
async def like_post_by_user_id(
    post_id: UUID,
    user_id: UUID,
    params: Params = Depends(),
    # current_user: User = Depends(deps.get_current_user()),
) -> IGetResponseBase[IPostReadWithUser]:
    """
    Gets a post by its id
    """
    post = await crud.post.like_by_user_id(
        id=post_id, 
        user_id=user_id
        # user_id=current_user.id
    )
    
    if not post:
        raise IdNotFoundException(Post, post_id)
    return create_response(data=post)

@router.get("/{post_id}")
async def get_post_by_id(
    post_id: UUID,
    current_user: User = Depends(deps.get_current_user()),
) -> IGetResponseBase[IPostReadWithUser]:
    """
    Gets a post by its id
    """
    post = await crud.post.get(id=post_id)
    if not post:
        raise IdNotFoundException(Post, post_id)
    return create_response(data=post)


@router.post("")
async def create_post(
    post: IPostCreate,
    current_user: User = Depends(
        deps.get_current_user()
    ),
) -> IPostResponseBase[IPostRead]:
    """
    Creates a new post
    """
    post = await crud.post.create(obj_in=post, created_by_id=current_user.id)
    return create_response(data=post)


@router.post("/admin")
async def create_post_admin(
    post: IPostCreateWithUser,
) -> IPostResponseBase[IPostRead]:
    """
    Creates a new post
    """
    print("post", post)
    post = await crud.post.create(obj_in=post)
    return create_response(data=post)


@router.put("/{post_id}")
async def update_post(
    post_id: UUID,
    post: IPostUpdate,
    current_user: User = Depends(
        deps.get_current_user(required_roles=[IRoleEnum.admin, IRoleEnum.manager])
    ),
) -> IPutResponseBase[IPostRead]:
    """
    Updates a post by its id
    """
    current_post = await crud.post.get(id=post_id)
    if not current_post:
        raise IdNotFoundException(Post, post_id)
    post_updated = await crud.post.update(obj_new=post, obj_current=current_post)
    return create_response(data=post_updated)


@router.delete("/{post_id}")
async def remove_post(
    post_id: UUID,
    current_user: User = Depends(
        deps.get_current_user()
    ),
) -> IDeleteResponseBase[IPostRead]:
    """
    Deletes a post by its id
    """
    current_post = await crud.post.get(id=post_id)
    if not current_post:
        raise IdNotFoundException(Post, post_id)
    post = await crud.post.remove(id=post_id)
    return create_response(data=post)


    params: Params = Depends(),
    current_user: User = Depends(deps.get_current_user()),


@router.get("/{post_id}/comments")
async def get_comment_list(
    post_id: UUID,
    current_user: User = Depends(
        deps.get_current_user()
    ),
) ->  IGetResponsePaginated[IPostRead]:
    """
    get comments from a post by its id
    """
    # select
    pass 


@router.post("/like/{post_id}")
async def like_post(
    post_id: UUID,
    current_user: User = Depends(deps.get_current_user()),
) -> IGetResponseBase[IPostReadWithUser]:
    """
    Gets a post by its id
    """
    post = await crud.post.like(
        id=post_id, 
        current_user=current_user
        # user_id=current_user.id
    )
    if not post:
        raise IdNotFoundException(Post, post_id)
    return create_response(data=post)
