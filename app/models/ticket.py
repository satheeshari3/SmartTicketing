from pydantic import BaseModel


class TicketBase(BaseModel):
    email: str
    query: str
    # 🚫 Remove category — it's determined internally
    # category: str | None = None


class TicketCreate(TicketBase):
    pass

class TicketInDB(TicketBase):
    id: str
    assigned_to: str | None = None
    created_at: str
