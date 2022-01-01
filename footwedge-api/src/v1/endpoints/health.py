from fastapi import APIRouter

from v1.constants import API_VERSION

router = APIRouter()


@router.get('/health')
def get_health():
    return f'Footwedge API Version: {API_VERSION}'
