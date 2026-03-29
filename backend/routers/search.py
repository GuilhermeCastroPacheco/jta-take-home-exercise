from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import httpx
import os
import json

router = APIRouter()

class SearchQuery(BaseModel):
    query: str

SYSTEM_PROMPT = """You are a navigation assistant for a data dashboard application about users and products.

The app has these routes and filters:

ROUTES:
- / (home dashboard)
- /users (users summary page)
- /users/all (users table with filters)
- /products (products summary page)
- /products/all (products table with filters)

FILTERS for /users/all:
- role: "admin", "moderator", "user"
- gender: "male", "female"
- state: any US state name
- city: any US city name
- age_range: "18-25", "26-30", "31-35", "36-40", "40+"

FILTERS for /products/all:
- category: "beauty", "fragrances", "furniture", "groceries", "home-decoration", "kitchen-accessories", "laptops", "mens-shirts", "mens-shoes", "mens-watches", "mobile-accessories", "motorcycle", "skin-care", "smartphones", "sports-accessories", "sunglasses", "tablets", "tops", "vehicle", "womens-bags", "womens-dresses", "womens-jewellery", "womens-shoes", "womens-watches"
- brand: any brand name
- availabilityStatus: "In Stock", "Low Stock", "Out of Stock"
- attention: true (shows products needing attention)

SORT for /products/all:
- sortField: "price", "rating", "stock"
- sortDir: "asc" or "desc"

SORT for /users/all:
- sortField: "name", "age"
- sortDir: "asc" or "desc"

Given a user query, respond ONLY with a valid JSON object like this:
{
  "route": "/users/all",
  "filters": { "gender": "female", "age_range": "26-30" },
  "sortField": "",
  "sortDir": "desc",
  "explanation": "Showing female users aged 26-30"
}

If you cannot understand the query, return:
{ "error": "I could not understand that query. Try something like 'show female users' or 'low stock products'" }

Respond ONLY with the JSON object, no other text."""

@router.post("/search")
async def ai_search(body: SearchQuery):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://api.anthropic.com/v1/messages",
                headers={
                    "x-api-key": os.getenv("ANTHROPIC_API_KEY"),
                    "anthropic-version": "2023-06-01",
                    "content-type": "application/json"
                },
                json={
                    "model": "claude-haiku-4-5-20251001",
                    "max_tokens": 500,
                    "system": SYSTEM_PROMPT,
                    "messages": [{"role": "user", "content": body.query}]
                },
                timeout=30.0
            )
            data = response.json()
            text = data["content"][0]["text"]
            clean = text.replace("```json", "").replace("```", "").strip()
            return json.loads(clean)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))