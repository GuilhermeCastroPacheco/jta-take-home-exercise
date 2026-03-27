from fastapi import APIRouter, HTTPException
from services.products import get_products_list, get_products_summary, get_product_detail, get_products_insights, get_products_aggregation

router = APIRouter()

@router.get("/summary")
async def products_summary():
    try:
        return await get_products_summary()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/list")
async def products_list():
    try:
        return await get_products_list()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/insights")
async def products_insights():
    try:
        return await get_products_insights()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/aggregation")
async def products_aggregation():
    try:
        return await get_products_aggregation()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{product_id}")
async def product_detail(product_id: int):
    try:
        return await get_product_detail(product_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))