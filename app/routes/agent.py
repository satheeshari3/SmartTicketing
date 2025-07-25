from fastapi import APIRouter, HTTPException
from app.models.agent import Agent
from app.database.mongo import db

router = APIRouter()

@router.post("/register-agent")
async def register_agent(agent: Agent):
    existing = await db["agents"].find_one({"email": agent.email})
    if existing:
        raise HTTPException(status_code=400, detail="Agent already exists")

    result = await db["agents"].insert_one(agent.dict())
    if not result.inserted_id:
        raise HTTPException(status_code=500, detail="Failed to register agent")
    
    return {"message": "Agent registered successfully", "agent_id": str(result.inserted_id)}
