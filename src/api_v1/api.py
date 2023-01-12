from fastapi import APIRouter

from src.api_v1.endpoints import users, roles, login

api_v1_router = APIRouter()
api_v1_router.include_router(login.router)
api_v1_router.include_router(users.router, prefix='/api/v1')
api_v1_router.include_router(roles.router, prefix='/api/v1')
