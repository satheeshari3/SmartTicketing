from fastapi import APIRouter, HTTPException
from app.core.assigner import assign_agent
from app.core.nlp_classifier import classify_ticket
from app.database.mongo import db
from app.models.ticket import TicketCreate  # ✅ Import the right model

router = APIRouter()

@router.post("/create-ticket")
async def create_ticket(ticket: TicketCreate):
    # Step 1: NLP classification
    category = classify_ticket(ticket.query)  # 'billing', 'technical', etc.

    # Step 2: Assign agent
    agent = await assign_agent(category)
    if not agent:
        raise HTTPException(status_code=503, detail="No available agent in this department")

    # Step 3: Store ticket in MongoDB
    ticket_data = ticket.dict()
    ticket_data["category"] = category
    ticket_data["assigned_agent"] = agent["email"]
    ticket_data["status"] = "open"

    await db["tickets"].insert_one(ticket_data)

    return {
        "message": "Ticket created successfully",
        "assigned_to": agent["name"],
        "email": agent["email"],
        "category": category
    }
