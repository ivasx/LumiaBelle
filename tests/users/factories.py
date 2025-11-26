import factory
from app.users.models.user import UserModel
from app.users.models.user_address import UserAddressModel
from app.users.models.cart import CartModel
from app.utils.encrypt import hash_password

class UserFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = UserModel
        sqlalchemy_session_persistence = "commit"

    email = factory.Faker("email")
    hashed_password = factory.LazyAttribute(lambda o: hash_password("password123"))
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    phone_number = factory.Sequence(lambda n: f"+38050{n:07d}")
    is_active = True

class UserAddressFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = UserAddressModel
        sqlalchemy_session_persistence = "commit"

    user = factory.SubFactory(UserFactory)
    address_line1 = factory.Faker("street_address")
    city = factory.Faker("city")
    zip_code = factory.Faker("zipcode")
    is_default = False

class CartFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = CartModel
        sqlalchemy_session_persistence = "commit"

    user = factory.SubFactory(UserFactory)