from fastapi import APIRouter

from .endpoints import (
    golf_club,
    golf_course,
    golf_round,
    health,
    user
)

v1__router = APIRouter()
v1__router.include_router(health.router)
v1__router.include_router(golf_club.router, prefix=f"/{golf_club.PATH_PREFIX}")
v1__router.include_router(golf_course.router, prefix=f"/{golf_course.PATH_PREFIX}")
v1__router.include_router(golf_round.router, prefix=f"/{golf_round.PATH_PREFIX}")
v1__router.include_router(user.router, prefix=f"/{user.PATH_PREFIX}")
