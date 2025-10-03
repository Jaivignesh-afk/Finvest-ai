from fastapi import APIRouter

from src.api.v1 import health, auth ,chat


# To include more routes go as
# from src.api.v1 import <module_name>
# then at the end of file api_router.include_router(<module_name>.router)

api_router = APIRouter()
api_router.include_router(health.router)
api_router.include_router(auth.router)
api_router.include_router(chat.router)
