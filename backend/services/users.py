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

    # Gender distribution
    gender_distribution = {}
    for u in users:
        gender_distribution[u.gender] = gender_distribution.get(u.gender, 0) + 1

    # Age group distribution
    age_groups = {"18-25": 0, "26-30": 0, "31-35": 0, "36-40": 0, "40+": 0}
    for u in users:
        age_groups[get_age_group(u.age)] += 1

    # Top companies by number of users
    company_counts = {}
    for u in users:
        name = u.company.name
        company_counts[name] = company_counts.get(name, 0) + 1
    top_companies = sorted(company_counts.items(), key=lambda x: x[1], reverse=True)[:5]

    # Role distribution
    role_distribution = {}
    for u in users:
        role_distribution[u.role] = role_distribution.get(u.role, 0) + 1

    # Most recent users (last 5 by id)
    recent_users = sorted(users, key=lambda x: x.id, reverse=True)[:5]

    # Age + gender distribution
    age_gender_distribution = {}
    for u in users:
        key = f"{u.gender} {get_age_group(u.age)}"
        age_gender_distribution[key] = age_gender_distribution.get(key, 0) + 1

    # Percentage of users with avg review rating >= 4
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

    # User reviews
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
            # By category
            cat = r["productCategory"]
            by_category[cat] = by_category.get(cat, 0) + 1
            # By tags
            for tag in r["productTags"]:
                by_tags[tag] = by_tags.get(tag, 0) + 1
            # By product
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
    university_data = UNIVERSITIES.get(user.university, {})

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
                if state not in by_city:
                    by_city[state] = {}
                by_city[state][city] = by_city[state].get(city, 0) + 1

            elif location_type == "company":
                state = u.company.address.state
                city = u.company.address.city
                if state not in by_city:
                    by_city[state] = {}
                by_city[state][city] = by_city[state].get(city, 0) + 1

            elif location_type == "university":
                uni_data = UNIVERSITIES.get(u.university)
                if not uni_data:
                    continue
                state = uni_data["state"]
                city = uni_data["city"]
                if state not in by_city:
                    by_city[state] = {}
                if city not in by_city[state]:
                    by_city[state][city] = {"count": 0, "universities": {}}
                by_city[state][city]["count"] += 1
                by_city[state][city]["universities"][u.university] = \
                    by_city[state][city]["universities"].get(u.university, 0) + 1
            else:
                continue

            by_state[state] = by_state.get(state, 0) + 1

        return {
            "by_state": by_state,
            "by_city": by_city
        }

    return {
        "address": aggregate_by_location("address"),
        "company": aggregate_by_location("company"),
        "university": aggregate_by_location("university")
    }

async def get_user_suggestions(user_id: int) -> dict:
    raw = await fetch_user(user_id)
    user = UserSchema(**raw)
    products_raw = await fetch_products()
    products = [ProductSchema(**p) for p in products_raw["products"]]
    users_raw = await fetch_users()
    users = parse_users(users_raw)

    # If user has no reviews, return empty suggestions
    user_reviews = []
    for product in products:
        for review in product.reviews:
            if review.reviewerEmail.lower() == user.email.lower():
                user_reviews.append({
                    "productId": product.id,
                    "productCategory": product.category,
                    "productBrand": product.brand,
                    "productTags": product.tags,
                    "rating": review.rating
                })

    if not user_reviews:
        return {"suggestions": []}

    # Extract user preferences from review history
    reviewed_ids = {r["productId"] for r in user_reviews}
    category_counts = {}
    brand_counts = {}
    tag_counts = {}

    for r in user_reviews:
        cat = r["productCategory"]
        category_counts[cat] = category_counts.get(cat, 0) + (1 + r["rating"] / 5)
        if r["productBrand"]:
            brand_counts[r["productBrand"]] = brand_counts.get(r["productBrand"], 0) + 1
        for tag in r["productTags"]:
            tag_counts[tag] = tag_counts.get(tag, 0) + 1

    # Similar users (same gender and age group)
    user_age_group = get_age_group(user.age)
    similar_users = [
        u for u in users
        if u.gender == user.gender
        and get_age_group(u.age) == user_age_group
        and u.id != user.id
    ]

    # Products reviewed by similar users
    similar_reviewed = {}
    for product in products:
        for review in product.reviews:
            for su in similar_users:
                if review.reviewerEmail.lower() == su.email.lower():
                    similar_reviewed[product.id] = similar_reviewed.get(product.id, 0) + review.rating

    # Score each unreviewed product
    scored = []
    for product in products:
        if product.id in reviewed_ids:
            continue
        if product.availabilityStatus == "Out of Stock":
            continue

        score = 0

        # Score by category
        if product.category in category_counts:
            score += category_counts[product.category] * 3

        # Score by brand
        if product.brand and product.brand in brand_counts:
            score += brand_counts[product.brand] * 2

        # Score by tags
        for tag in product.tags:
            if tag in tag_counts:
                score += tag_counts[tag]

        # Score by similar users
        if product.id in similar_reviewed:
            score += similar_reviewed[product.id] * 1.5

        # Score by product rating
        score += product.rating

        if score > 0:
            scored.append((product, score))

    # Top 6 products
    scored.sort(key=lambda x: x[1], reverse=True)
    top = scored[:6]

    return {
        "suggestions": [
            {
                "id": p.id,
                "title": p.title,
                "category": p.category,
                "brand": p.brand,
                "price": p.price,
                "rating": p.rating,
                "thumbnail": p.thumbnail,
                "availabilityStatus": p.availabilityStatus,
                "score": round(score, 2)
            }
            for p, score in top
        ],
        "based_on": {
            "top_categories": sorted(category_counts, key=category_counts.get, reverse=True)[:3],
            "top_tags": sorted(tag_counts, key=tag_counts.get, reverse=True)[:3],
            "similar_users_count": len(similar_users)
        }
    }