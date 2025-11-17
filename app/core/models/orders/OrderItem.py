from decimal import Decimal

from sqlalchemy import Integer, ForeignKey, UniqueConstraint, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.models.base import BaseModel


class OrderItem(BaseModel):
    __tablename__ = 'order_item'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    order_id: Mapped[int] = mapped_column(
        ForeignKey('order.id'),
        nullable=False,
        index=True
    )
    product_variant_id: Mapped[int] = mapped_column(
        ForeignKey('product_variant.id'),
        nullable=False
    )
    quantity: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    price_at_order: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)

    order: Mapped['Order'] = relationship(back_populates='items')
    product_variant: Mapped['ProductVariant'] = relationship()
