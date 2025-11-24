from datetime import datetime
from decimal import Decimal
from typing import Optional
from pydantic import BaseModel, Field


class OrderCreateSchema(BaseModel):
    user_id: int = Field(default_factory=int, ge=0)
    address_id: int = Field(default_factory=int, ge=0)
    total_amount: Decimal = Field(gt=0)
    status: str = Field(max_length=50, default='Pending')
    created_at: datetime = Field(default_factory=datetime.now)


class OrderResponseSchema(BaseModel):
    id: int = Field(default_factory=int, gt=0)
    user_id: int
    address_id: int
    total_amount: Decimal
    status: str
    created_at: datetime


class OrderPartialUpdateSchema(BaseModel):
    user_id: Optional[int] = Field(default=None, ge=0)
    address_id: Optional[int] = Field(default=None, ge=0)
    total_amount: Optional[Decimal] = Field(default=None, decimal_places=2, gt=0)
    status: Optional[str] = Field(default=None, max_length=50)
