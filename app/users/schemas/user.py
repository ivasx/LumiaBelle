from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime


class UserCreateSchema(BaseModel):
    email: str = Field(max_length=255)
    password: str = Field(min_length=8)
    first_name: str = Field(max_length=100)
    last_name: str = Field(max_length=100)
    phone_number: Optional[str] = Field(max_length=20)
    is_active: bool = Field(default=True)
    created_at: Optional[datetime] = Field(default=datetime.now())


class UserResponseSchema(BaseModel):
    id: int = Field(default_factory=int, gt=0)
    email: str
    hashed_password: str
    first_name: str
    last_name: str
    phone_number: Optional[str]
    is_active: bool
    created_at: Optional[datetime]


class UserPartialUpdateSchema(BaseModel):
    email: Optional[str] = Field(default=None, max_length=255)
    hashed_password: Optional[str] = Field(default=None, max_length=255)
    first_name: Optional[str] = Field(default=None, max_length=100)
    last_name: Optional[str] = Field(default=None, max_length=100)
    phone_number: Optional[str] = Field(default=None, max_length=20)
    is_active: Optional[bool] = Field(default=None)
