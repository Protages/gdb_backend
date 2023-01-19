from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.models import models
from src.schemas.role_schemas import Role, RoleCreate, RoleUpdate
from src.crud import role_crud
from src.api_v1.depends import get_db, oauth2_scheme, Pagination
from src.core import config
from src.core.security import (
    authenticate_user, 
    authenticate_user_by_token, 
    create_access_token
)

router = APIRouter(tags=['Roles'])


@router.get('/role/{role_id}', response_model=Role)
async def read_role(role_id: int, db: Session = Depends(get_db)):
    role = role_crud.get_role_by_id(db=db, role_id=role_id)
    return role


@router.get('/role/all/', response_model=list[Role])
async def read_all_roles(
        paginator: Pagination = Depends(), db: Session = Depends(get_db)
    ):
    db_roles = role_crud.get_all_roles(db=db, size=paginator.size, page=paginator.page)
    return db_roles


@router.post('/role', response_model=Role)
async def create_role(role: RoleCreate, db: Session = Depends(get_db)):
    role = role_crud.create_role(db=db, role=role)
    return role


@router.put('/role', response_model=Role)
async def update_role(role_id: int, role: RoleUpdate, db: Session = Depends(get_db)):
    role = role_crud.update_role(db=db, role_id=role_id, role=role)
    return role


@router.delete('/role/{role_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_role(role_id: int, db: Session = Depends(get_db)):
    response = role_crud.delete_role(db=db, role_id=role_id)
    return response
