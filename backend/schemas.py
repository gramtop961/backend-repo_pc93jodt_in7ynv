from __future__ import annotations

from typing import Optional
from pydantic import BaseModel, Field

# Luxury service lead form (collection name: lead)
class Lead(BaseModel):
    full_name: str = Field(..., min_length=2, max_length=100)
    email: str = Field(...)
    phone: Optional[str] = Field(default=None, max_length=30)
    service: str = Field(..., description="Requested service type")
    message: Optional[str] = Field(default=None, max_length=1000)
    source: Optional[str] = Field(default="website")

# Newsletter subscriptions (collection name: subscription)
class Subscription(BaseModel):
    email: str
    tag: Optional[str] = Field(default="luxury")
