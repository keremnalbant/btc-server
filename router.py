from fastapi import APIRouter, status

router = APIRouter()


@router.get("/hc", status_code=status.HTTP_200_OK)
async def health_check():
    return "ok"


@router.get("/create-cookie", status_code=status.HTTP_200_OK)
async def create_cookie():
    return "ok"
