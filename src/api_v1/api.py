from fastapi import APIRouter

from src.api_v1.endpoints import (
    users, 
    roles, 
    login, 
    genres, 
    platforms, 
    games,
    reviews,
    comments,
    grades,
    categories
)

prefix = '/api/v1'

api_v1_router = APIRouter()
api_v1_router.include_router(login.router)
api_v1_router.include_router(users.router, prefix=prefix)
api_v1_router.include_router(roles.router, prefix=prefix)
api_v1_router.include_router(genres.router, prefix=prefix)
api_v1_router.include_router(platforms.router, prefix=prefix)
api_v1_router.include_router(games.router, prefix=prefix)
api_v1_router.include_router(reviews.router, prefix=prefix)
api_v1_router.include_router(comments.router, prefix=prefix)
api_v1_router.include_router(grades.router, prefix=prefix)
api_v1_router.include_router(categories.router, prefix=prefix)
