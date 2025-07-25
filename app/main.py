from fastapi import FastAPI
from app.routes.tickets import router as ticket_router
from app.database.mongo import connect_to_mongo
from app.routes.tickets import router as ticket_router
from app.routes.agent import router as agent_router

app = FastAPI()

@app.on_event("startup")
async def startup_db():
    await connect_to_mongo()

app.include_router(ticket_router)
app.include_router(agent_router) 