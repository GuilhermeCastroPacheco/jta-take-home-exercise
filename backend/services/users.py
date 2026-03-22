from external.dummyjson import fetch_users, fetch_user
from schemas.user import UserSchema
from typing import List

def parse_users(raw: dict) -> List[UserSchema]:
    return [UserSchema(**user) for user in raw["users"]]

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
    age_groups = {"18-25": 0, "26-30": 0, "31-35": 0, "36-50": 0, "50+": 0}
    for u in users:
        if u.age <= 25:
            age_groups["18-25"] += 1
        elif u.age <= 30:
            age_groups["26-30"] += 1
        elif u.age <= 35:
            age_groups["31-35"] += 1
        elif u.age <= 50:
            age_groups["36-50"] += 1
        else:
            age_groups["50+"] += 1

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

    return {
        "total": len(users),
        "gender_distribution": gender_distribution,
        "age_groups": age_groups,
        "top_companies": [{"name": k, "count": v} for k, v in top_companies],
        "role_distribution": role_distribution,
        "recent_users": [u.model_dump() for u in recent_users]
    }

async def get_user_detail(user_id: int) -> dict:
    raw = await fetch_user(user_id)
    user = UserSchema(**raw)
    return user.model_dump()