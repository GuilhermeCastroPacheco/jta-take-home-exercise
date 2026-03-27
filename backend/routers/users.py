from fastapi import APIRouter, HTTPException
from services.users import get_users_list, get_users_summary, get_user_detail, get_users_insights, get_users_geo

router = APIRouter()

@router.get("/summary")
async def users_summary():
    try:
        return await get_users_summary()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/list")
async def users_list():
    try:
        return await get_users_list()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/insights")
async def users_insights():
    try:
        return await get_users_insights()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/geo")
async def users_geo():
    try:
        return await get_users_geo()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{user_id}")
async def user_detail(user_id: int):
    try:
        return await get_user_detail(user_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))