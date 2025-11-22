from fastapi import APIRouter, HTTPException
from app.core.assigner import assign_agent
from app.core.nlp_classifier import classify_ticket
from app.database.mongo import db
from app.database.redis_client import redis_client
from app.models.ticket import TicketCreate
import json

router = APIRouter()

# ---------------------------------------------------------
# CREATE TICKET + ASSIGN AGENT + INVALIDATE CACHE
# ---------------------------------------------------------
@router.post("/create-ticket")
async def create_ticket(ticket: TicketCreate):
    # Step 1: NLP Classify the ticket query
    category = classify_ticket(ticket.query)

    # Step 2: Assign an available agent for this category
    agent = await assign_agent(category)
    if not agent:
        raise HTTPException(
            status_code=503,
            detail="No available agent in this department"
        )

    # Step 3: Prepare the ticket object to insert
    ticket_data = ticket.dict()
    ticket_data["category"] = category
    ticket_data["assigned_agent"] = agent["email"]
    ticket_data["status"] = "open"

    # Step 4: Insert the ticket into MongoDB
    await db["tickets"].insert_one(ticket_data)

    # Step 5: Invalidate the popular categories cache
    await redis_client.delete("popular_categories")

    # Step 6: Respond back
    return {
        "message": "Ticket created successfully",
        "assigned_to": agent["name"],
        "email": agent["email"],
        "category": category
    }


# ---------------------------------------------------------
# POPULAR CATEGORIES (WITH REDIS CACHING)
# ---------------------------------------------------------
@router.get("/popular-categories")
async def get_popular_categories():
    cache_key = "popular_categories"

    # 1 — Check Redis cache first
    cached = await redis_client.get(cache_key)
    if cached:
        return {"source": "redis", "data": json.loads(cached)}

    # 2 — No cache → compute from MongoDB
    data = await db["tickets"].aggregate([
        {"$group": {"_id": "$category", "count": {"$sum": 1}}},
        {"$project": {"category": "$_id", "count": 1, "_id": 0}},
        {"$sort": {"count": -1}},
        {"$limit": 10}
    ]).to_list(length=None)

    # 3 — Store fresh result in Redis (10 mins)
    await redis_client.set(cache_key, json.dumps(data), ex=600)

    # 4 — Return Mongo result
    return {"source": "mongodb", "data": data}
