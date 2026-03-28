from external.dummyjson import fetch_products, fetch_product
from schemas.product import ProductSchema
from typing import List

def parse_products(raw: dict) -> List[ProductSchema]:
    return [ProductSchema(**product) for product in raw["products"]]

async def get_products_list() -> List[dict]:
    raw = await fetch_products()
    products = parse_products(raw)
    return [p.model_dump() for p in products]

async def get_products_summary() -> dict:
    raw = await fetch_products()
    products = parse_products(raw)

    # Métricas gerais
    avg_price = sum(p.price for p in products) / len(products)
    avg_rating = sum(p.rating for p in products) / len(products)
    avg_discount = sum(p.discountPercentage for p in products) / len(products)

    # Agregação por categoria
    category_map = {}
    for p in products:
        if p.category not in category_map:
            category_map[p.category] = {"count": 0, "total_price": 0, "total_rating": 0, "total_stock": 0}
        category_map[p.category]["count"] += 1
        category_map[p.category]["total_price"] += p.price
        category_map[p.category]["total_rating"] += p.rating
        category_map[p.category]["total_stock"] += p.stock

    by_category = [
        {
            "category": cat,
            "count": vals["count"],
            "avg_price": round(vals["total_price"] / vals["count"], 2),
            "avg_rating": round(vals["total_rating"] / vals["count"], 2),
            "total_stock": vals["total_stock"]
        }
        for cat, vals in category_map.items()
    ]

    # Distribuição por availability status
    availability_distribution = {}
    for p in products:
        availability_distribution[p.availabilityStatus] = availability_distribution.get(p.availabilityStatus, 0) + 1

    # Produtos com baixo stock (stock abaixo do minimumOrderQuantity)
    low_stock = [
        p.model_dump() for p in products
        if p.stock < p.minimumOrderQuantity
    ]

    # Top 5 produtos melhor avaliados
    top_rated = sorted(products, key=lambda x: x.rating, reverse=True)[:5]

    # Produtos recentes (últimos 5 por id)
    recent_products = sorted(products, key=lambda x: x.id, reverse=True)[:5]

    return {
        "total": len(products),
        "avg_price": round(avg_price, 2),
        "avg_rating": round(avg_rating, 2),
        "avg_discount": round(avg_discount, 2),
        "by_category": by_category,
        "availability_distribution": availability_distribution,
        "low_stock": low_stock,
        "top_rated": [p.model_dump() for p in top_rated],
        "recent_products": [p.model_dump() for p in recent_products]
    }

async def get_products_insights() -> dict:
    raw = await fetch_products()
    products = parse_products(raw)

    # Relação preço vs rating (para scatter plot)
    price_vs_rating = [
        {"id": p.id, "title": p.title, "price": p.price, "rating": p.rating, "category": p.category}
        for p in products
    ]

    # Oportunidades de desconto: desconto alto + rating alto
    discount_opportunities = [
        p.model_dump() for p in products
        if p.discountPercentage >= 10 and p.rating >= 4.5
    ]

    # Risco de rutura de stock
    stock_risk = [
        {
            "id": p.id,
            "title": p.title,
            "stock": p.stock,
            "minimumOrderQuantity": p.minimumOrderQuantity,
            "category": p.category
        }
        for p in products
        if p.stock < p.minimumOrderQuantity
    ]

    # Distribuição de preços por categoria (para box plot ou bar chart)
    price_distribution = {}
    for p in products:
        if p.category not in price_distribution:
            price_distribution[p.category] = []
        price_distribution[p.category].append(p.price)

    price_ranges = [
        {
            "category": cat,
            "min": round(min(prices), 2),
            "max": round(max(prices), 2),
            "avg": round(sum(prices) / len(prices), 2)
        }
        for cat, prices in price_distribution.items()
    ]

    return {
        "price_vs_rating": price_vs_rating,
        "discount_opportunities": discount_opportunities,
        "stock_risk": stock_risk,
        "price_ranges": price_ranges
    }

async def get_product_detail(product_id: int) -> dict:
    raw = await fetch_product(product_id)
    product = ProductSchema(**raw)
    return product.model_dump()

async def get_products_aggregation() -> dict:
    raw = await fetch_products()
    products = parse_products(raw)

    all_categories = sorted(set(p.category for p in products))
    all_brands = sorted(set(p.brand for p in products if p.brand))
    all_tags = sorted(set(tag for p in products for tag in p.tags))

    def median(values):
        sorted_vals = sorted(values)
        n = len(sorted_vals)
        mid = n // 2
        if n % 2 == 0:
            return round((sorted_vals[mid - 1] + sorted_vals[mid]) / 2, 2)
        return round(sorted_vals[mid], 2)

    def aggregate(items):
        prices = [p.price for p in items]
        stocks = [p.stock for p in items]
        ratings = [p.rating for p in items]
        return {
            "count": len(items),
            "price": {
                "min": round(min(prices), 2),
                "max": round(max(prices), 2),
                "avg": round(sum(prices) / len(prices), 2),
                "median": median(prices),
                "total": round(sum(prices), 2)
            },
            "stock": {
                "min": min(stocks),
                "max": max(stocks),
                "avg": round(sum(stocks) / len(stocks), 2),
                "median": median(stocks),
                "total": sum(stocks)
            },
            "rating": {
                "min": round(min(ratings), 2),
                "max": round(max(ratings), 2),
                "avg": round(sum(ratings) / len(ratings), 2),
                "median": median(ratings)
            }
        }

    return {
        "overall": aggregate(products),
        "by_category": {cat: aggregate([p for p in products if p.category == cat]) for cat in all_categories},
        "by_brand": {brand: aggregate([p for p in products if p.brand == brand]) for brand in all_brands},
        "by_tag": {tag: aggregate([p for p in products if tag in p.tags]) for tag in all_tags},
        "by_category_brand": {
            cat: {
                brand: aggregate([p for p in products if p.category == cat and p.brand == brand])
                for brand in sorted(set(p.brand for p in products if p.category == cat and p.brand))
            }
            for cat in all_categories
        },
        "filter_options": {
            "categories": all_categories,
            "brands": all_brands,
            "tags": all_tags
        }
    }