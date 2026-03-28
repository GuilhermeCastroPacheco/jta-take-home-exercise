from external.dummyjson import fetch_users, fetch_user, fetch_products
from external.universities import get_universities
from schemas.user import UserSchema
from schemas.product import ProductSchema
from typing import List
from collections import defaultdict

UNIVERSITIES = get_universities()

def parse_users(raw: dict) -> List[UserSchema]:
    return [UserSchema(**user) for user in raw["users"]]

def get_age_group(age: int) -> str:
    if age <= 25:
        return "18-25"
    elif age <= 30:
        return "26-30"
    elif age <= 35:
        return "31-35"
    elif age <= 40:
        return "36-40"
    else:
        return "40+"

async def get_users_list() -> List[dict]:
    raw = await fetch_users()
    users = parse_users(raw)
    return [u.model_dump() for u in users]

async def get_users_summary() -> dict:
    raw = await fetch_users()
    users = parse_users(raw)

    # Distribuição por género
    gender_distribution = {}
    for u in users:
        gender_distribution[u.gender] = gender_distribution.get(u.gender, 0) + 1

    # Distribuição por faixa etária
    age_groups = {"18-25": 0, "26-30": 0, "31-35": 0, "36-40": 0, "40+": 0}
    for u in users:
        age_groups[get_age_group(u.age)] += 1

    # Top empresas por número de utilizadores
    company_counts = {}
    for u in users:
        name = u.company.name
        company_counts[name] = company_counts.get(name, 0) + 1
    top_companies = sorted(company_counts.items(), key=lambda x: x[1], reverse=True)[:5]

    # Distribuição por role
    role_distribution = {}
    for u in users:
        role_distribution[u.role] = role_distribution.get(u.role, 0) + 1

    # Utilizadores recentes (últimos 5 por id)
    recent_users = sorted(users, key=lambda x: x.id, reverse=True)[:5]

    # Distribuição age + gender
    age_gender_distribution = {}
    for u in users:
        key = f"{u.gender} {get_age_group(u.age)}"
        age_gender_distribution[key] = age_gender_distribution.get(key, 0) + 1

    # Percentagem de utilizadores com média de reviews >= 4
    products_raw = await fetch_products()
    products = [ProductSchema(**p) for p in products_raw["products"]]

    email_to_user = {u.email.lower(): u for u in users}

    user_ratings = {}
    for product in products:
        for review in product.reviews:
            email = review.reviewerEmail.lower()
            if email in email_to_user:
                if email not in user_ratings:
                    user_ratings[email] = []
                user_ratings[email].append(review.rating)

    users_with_reviews = len(user_ratings)
    high_rating_count = sum(
        1 for ratings in user_ratings.values()
        if sum(ratings) / len(ratings) >= 4
    )
    high_rating_pct = round((high_rating_count / users_with_reviews * 100), 1) if users_with_reviews > 0 else 0

    return {
        "total": len(users),
        "gender_distribution": gender_distribution,
        "age_groups": age_groups,
        "top_companies": [{"name": k, "count": v} for k, v in top_companies],
        "role_distribution": role_distribution,
        "recent_users": [u.model_dump() for u in recent_users],
        "age_gender_distribution": age_gender_distribution,
        "high_rating_pct": high_rating_pct
    }

async def get_user_detail(user_id: int) -> dict:
    users_raw = await fetch_users()
    products_raw = await fetch_products()

    raw = await fetch_user(user_id)
    user = UserSchema(**raw)

    products = [ProductSchema(**p) for p in products_raw["products"]]

    # Reviews do utilizador
    user_reviews = []
    for product in products:
        for review in product.reviews:
            if review.reviewerEmail.lower() == user.email.lower():
                user_reviews.append({
                    "productId": product.id,
                    "productTitle": product.title,
                    "productThumbnail": product.thumbnail,
                    "productCategory": product.category,
                    "productBrand": product.brand or "No brand",
                    "productTags": product.tags,
                    "rating": review.rating,
                    "comment": review.comment,
                })

    # Reviews summary
    reviews_summary = {}
    if user_reviews:
        ratings = [r["rating"] for r in user_reviews]
        
        by_category = {}
        by_tags = {}
        by_product = {}
        
        for r in user_reviews:
            # by category
            cat = r["productCategory"]
            by_category[cat] = by_category.get(cat, 0) + 1
            
            # by tags
            for tag in r["productTags"]:
                by_tags[tag] = by_tags.get(tag, 0) + 1
            
            # by product
            by_product[r["productTitle"]] = by_product.get(r["productTitle"], 0) + 1

        reviews_summary = {
            "total": len(user_reviews),
            "avg_rating": round(sum(ratings) / len(ratings), 2),
            "min_rating": min(ratings),
            "max_rating": max(ratings),
            "by_category": by_category,
            "by_tags": by_tags,
            "by_product": by_product,
            "by_rating": {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
        }
        for r in user_reviews:
            reviews_summary["by_rating"][r["rating"]] += 1

    # University data
    universities = get_universities()
    university_data = universities.get(user.university, {})

    return {
        **user.model_dump(),
        "university_data": university_data,
        "reviews": user_reviews,
        "reviews_summary": reviews_summary
    }

async def get_users_insights() -> dict:
    users_raw = await fetch_users()
    products_raw = await fetch_products()

    users = parse_users(users_raw)
    products = [ProductSchema(**p) for p in products_raw["products"]]

    email_to_user = {u.email.lower(): u for u in users}

    reviews = []
    for product in products:
        for review in product.reviews:
            reviews.append({
                "reviewerEmail": review.reviewerEmail.lower(),
                "rating": review.rating,
                "productCategory": product.category,
                "productBrand": product.brand or "No brand",
                "productTags": product.tags,
            })

    user_ratings = defaultdict(list)
    for r in reviews:
        if r["reviewerEmail"] in email_to_user:
            user_ratings[r["reviewerEmail"]].append(r)

    user_review_data = []
    for email, user_reviews in user_ratings.items():
        user = email_to_user[email]
        avg_rating = sum(r["rating"] for r in user_reviews) / len(user_reviews)
        user_review_data.append({
            "email": email,
            "gender": user.gender,
            "age": user.age,
            "age_group": get_age_group(user.age),
            "state": user.address.state,
            "avg_rating": round(avg_rating, 2),
            "reviews": user_reviews
        })

    emails_with_reviews = set(user_ratings.keys())
    no_review_count = sum(1 for u in users if u.email.lower() not in emails_with_reviews)

    all_categories = sorted(set(r["productCategory"] for r in reviews))
    all_brands = sorted(set(r["productBrand"] for r in reviews))
    all_tags = sorted(set(tag for r in reviews for tag in r["productTags"]))

    return {
        "user_review_data": user_review_data,
        "no_review_count": no_review_count,
        "total_users": len(users),
        "filter_options": {
            "categories": all_categories,
            "brands": all_brands,
            "tags": all_tags
        }
    }

async def get_users_geo() -> dict:
    raw = await fetch_users()
    users = parse_users(raw)

    def aggregate_by_location(location_type):
        by_state = {}
        by_city = {}

        for u in users:
            if location_type == "address":
                state = u.address.state
                city = u.address.city
            elif location_type == "company":
                state = u.company.address.state
                city = u.company.address.city
            elif location_type == "university":
                uni_data = UNIVERSITIES.get(u.university)
                if not uni_data:
                    continue
                state = uni_data["state"]
                city = uni_data["city"]
            else:
                continue

            by_state[state] = by_state.get(state, 0) + 1
            if state not in by_city:
                by_city[state] = {}
            by_city[state][city] = by_city[state].get(city, 0) + 1

        return {
            "by_state": by_state,
            "by_city": by_city
        }

    return {
        "address": aggregate_by_location("address"),
        "company": aggregate_by_location("company"),
        "university": aggregate_by_location("university")
    }