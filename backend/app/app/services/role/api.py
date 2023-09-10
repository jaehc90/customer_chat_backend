from uuid import UUID
from app.utils.exceptions import (
    ContentNoChangeException,
    IdNotFoundException,
    NameExistException,
)
from fastapi import APIRouter, Depends, status
from fastapi_pagination import Params
from app import crud
from app.api import deps
from app.models.role_model import Role
from app.models.user_model import User
from app.schemas.base_response_schema import (
    IGetResponseBase,
    IGetResponsePaginated,
    IPostResponseBase,
    IPutResponseBase,
    create_response,
)
from app.schemas.role_schema import IRoleCreate, IRoleEnum, IRoleRead, IRoleUpdate

router = APIRouter()


@router.get("")
async def get_roles(
    params: Params = Depends(),
    current_user: User = Depends(deps.get_current_user()),
) -> IGetResponsePaginated[IRoleRead]:
    """
    Gets a paginated list of roles
    """
    roles = await crud.role.get_multi_paginated(params=params)
    return create_response(data=roles)


@router.get(
    "/{role_id}",
    status_code=status.HTTP_200_OK,
)
async def get_role_by_id(
    role_id: UUID,
    current_user: User = Depends(deps.get_current_user()),
) -> IGetResponseBase[IRoleRead]:
    """
    Gets a role by its id
    """
    role = await crud.role.get(id=role_id)
    if role:
        return create_response(data=role)
    else:
        raise IdNotFoundException(Role, id=role_id)


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_role(
    role: IRoleCreate,
    current_user: User = Depends(
        deps.get_current_user(required_roles=[IRoleEnum.admin])
    ),
) -> IPostResponseBase[IRoleRead]:
    """
    Create a new role
    """
    role_current = await crud.role.get_role_by_name(name=role.name)
    if not role_current:
        new_permission = await crud.role.create(obj_in=role)
        return create_response(data=new_permission)
    else:
        raise NameExistException(Role, name=role_current.name)


@router.put("/{role_id}")
async def update_permission(
    role_id: UUID,
    role: IRoleUpdate,
    current_user: User = Depends(
        deps.get_current_user(required_roles=[IRoleEnum.admin])
    ),
) -> IPutResponseBase[IRoleRead]:
    """
    Updates the permission of a role by its id
    """
    current_role = await crud.role.get(id=role_id)
    if not current_role:
        raise IdNotFoundException(Role, id=role_id)

    if current_role.name == role.name and current_role.description == role.description:
        raise ContentNoChangeException()

    exist_role = await crud.role.get_role_by_name(name=role.name)
    if exist_role:
        raise NameExistException(Role, name=role.name)

    updated_role = await crud.role.update(obj_current=current_role, obj_new=role)
    return create_response(data=updated_role)
