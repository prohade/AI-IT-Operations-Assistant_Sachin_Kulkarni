from typing import Optional
from pydantic import BaseModel, Field

class Employee(BaseModel):
    employee_id: str
    name: str
    department: str
    email: str
    job_title: str
    status: str

class Ticket(BaseModel):
    ticket_id: str
    employee_id: str
    category: str
    subject: str
    description: str
    priority: str
    status: str
    assigned_to: Optional[str] = None
    created_at: str

class KnowledgeArticle(BaseModel):
    article_id: int
    category: str
    title: str
    content: str
    keywords: str

class TicketCreateRequest(BaseModel):
    employee_id: str = Field(..., min_length=3)
    category: str = Field(..., min_length=2)
    subject: str = Field(..., min_length=3)
    description: str = Field(..., min_length=5)
    priority: str = Field(default="Medium")
