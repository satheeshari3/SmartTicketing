from pydantic import BaseModel, EmailStr

class Agent(BaseModel):
    name: str
    email: EmailStr
    department: str
    active_tickets: int = 0
