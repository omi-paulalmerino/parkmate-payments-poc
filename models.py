from pydantic import BaseModel
from typing import Any, Dict, Optional


class Ticket(BaseModel):
  id: Optional[str]
  plate_number: str
  is_paid: bool = False


class TicketCreate(BaseModel):
  plate_number: str
  is_paid: bool = False


class PaymentGcashCreate(BaseModel):
  ticket_id: str
  amount: str


class PaymentGcashOrder(BaseModel):
    response: Dict[str, Any]
    signature: str


class GcashNotifRequest(BaseModel):
    request: Dict[str, Any]
    signature: str

