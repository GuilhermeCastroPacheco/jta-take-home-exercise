import httpx
import os
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("DUMMYJSON_BASE_URL")

async def fetch_users() -> dict:
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BASE_URL}/users?limit=0")
        response.raise_for_status()
        return response.json()

async def fetch_user(user_id: int) -> dict:
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BASE_URL}/users/{user_id}")
        response.raise_for_status()
        return response.json()

async def fetch_products() -> dict:
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BASE_URL}/products?limit=0")
        response.raise_for_status()
        return response.json()

async def fetch_product(product_id: int) -> dict:
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BASE_URL}/products/{product_id}")
        response.raise_for_status()
        return response.json()