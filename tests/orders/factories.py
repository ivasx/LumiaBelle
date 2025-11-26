import factory
from app.orders.models.order import OrderModel
from app.orders.models.order_item import OrderItemModel
from app.orders.models.cart_item import CartItemModel
from tests.products.factories import ProductVariantFactory
from tests.users.factories import UserFactory, UserAddressFactory, CartFactory


class OrderFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = OrderModel
        sqlalchemy_session_persistence = "commit"

    user = factory.SubFactory(UserFactory)
    address = factory.SubFactory(UserAddressFactory)
    total_amount = factory.Faker(
        "pydecimal", left_digits=4, right_digits=2, positive=True
    )
    status = "Pending"

class OrderItemFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = OrderItemModel
        sqlalchemy_session_persistence = "commit"

    order = factory.SubFactory(OrderFactory)
    product_variant = factory.SubFactory(ProductVariantFactory)
    quantity = factory.Faker("random_int", min=1, max=5)
    price_at_order = factory.Faker(
        "pydecimal", left_digits=3, right_digits=2, positive=True
    )

class CartItemFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = CartItemModel
        sqlalchemy_session_persistence = "commit"

    cart = factory.SubFactory(CartFactory)
    variant = factory.SubFactory(ProductVariantFactory)
    quantity = factory.Faker("random_int", min=1, max=10)