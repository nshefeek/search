from fastapi import FastAPI, APIRouter


router = APIRouter()


@router.get('/')
async def index():
    return "Hello"
