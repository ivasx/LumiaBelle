from datetime import datetime
from decimal import Decimal
from typing import List

from sqlalchemy import Integer, String, Numeric, ForeignKey, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.models.base import BaseModel


class OrderModel(BaseModel):
    __tablename__ = 'order'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'), nullable=False, index=True)
    address_id: Mapped[int] = mapped_column(ForeignKey('useraddress.id'), nullable=False)
    total_amount: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default='Pending')
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, server_default=func.now())

    user: Mapped['UserModel'] = relationship(back_populates='orders')
    address: Mapped['UserAddressModel'] = relationship()
    items: Mapped[List['OrderItemModel']] = relationship(back_populates='order', cascade='all, delete-orphan')
