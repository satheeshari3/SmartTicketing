from app.database.mongo import db

async def assign_agent(department: str):
    agent = await db["agents"].find_one(
        {"department": department},
        sort=[("active_tickets", 1)]
    )
    if agent:
        # Increment active tickets
        await db["agents"].update_one(
            {"_id": agent["_id"]},
            {"$inc": {"active_tickets": 1}}
        )
    return agent
