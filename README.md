# E-Commerce API

[Українська](README-ua.md) | **English**

A modern RESTful API for e-commerce applications built with FastAPI and SQLAlchemy. This project provides a complete backend solution for managing products, users, orders, and shopping carts.

## Features

- **User Management**: Complete authentication system with registration, login, and profile management
- **Product Catalog**: Multi-category product system with variants (size, color), inventory tracking
- **Shopping Cart**: Persistent cart functionality with item management
- **Order Processing**: Full order lifecycle management from creation to completion
- **Async/Await**: Built on async Python for high performance
- **Database**: SQLAlchemy ORM with async support, SQLite for development
- **Testing**: Comprehensive test suite using pytest with factories

## Tech Stack

- **Framework**: FastAPI
- **Database**: SQLAlchemy (async), SQLite
- **Authentication**: OAuth2 with Password flow
- **Password Hashing**: Passlib with bcrypt
- **Testing**: Pytest, pytest-asyncio, Factory Boy, Faker
- **HTTP Client**: HTTPX (for testing)

## Project Structure

```
app/
├── core/
│   ├── models/         # Database models
│   └── settings/       # Configuration and database setup
├── users/
│   ├── models/         # User, Cart, UserAddress models
│   ├── routers/        # User-related endpoints
│   └── schemas/        # Pydantic schemas for validation
├── products/
│   ├── models/         # Product, Category, Size, Color, ProductVariant models
│   ├── routers/        # Product-related endpoints
│   └── schemas/        # Pydantic schemas
├── orders/
│   ├── models/         # Order, OrderItem, CartItem models
│   ├── routers/        # Order-related endpoints
│   └── schemas/        # Pydantic schemas
├── utils/              # Utilities (auth, encryption)
└── main.py             # Application entry point

tests/
├── users/              # User-related tests
├── products/           # Product-related tests
├── orders/             # Order-related tests
└── conftest.py         # Pytest configuration and fixtures
```

## Installation

### Prerequisites

- Python 3.9 or higher
- pip package manager

### Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd <project-directory>
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Application

Start the development server:

```bash
python app/main.py
```

The API will be available at `http://localhost:8000`

Interactive API documentation (Swagger UI) will be available at:
- `http://localhost:8000/docs`

Alternative API documentation (ReDoc) at:
- `http://localhost:8000/redoc`

## Testing

Run the complete test suite:

```bash
pytest
```

Run tests with coverage report:

```bash
pytest --cov=app
```

Run specific test file:

```bash
pytest tests/users/test_user_endpoints.py
```

## API Endpoints

### Authentication

- `POST /api/users/login` - User login (returns access token)

### Users

- `POST /api/users/` - Create new user
- `GET /api/users/` - Get all users
- `GET /api/users/{user_id}` - Get user by ID
- `PUT /api/users/{user_id}` - Update user
- `PATCH /api/users/{user_id}` - Partially update user
- `DELETE /api/users/{user_id}` - Delete user (requires authentication)

### User Addresses

- `POST /api/user_addresses/` - Create new address
- `GET /api/user_addresses/` - Get all addresses
- `GET /api/user_addresses/{address_id}` - Get address by ID
- `PUT /api/user_addresses/{address_id}` - Update address
- `PATCH /api/user_addresses/{address_id}` - Partially update address
- `DELETE /api/user_addresses/{address_id}` - Delete address (requires authentication)

### Products

- `POST /api/products/` - Create new product
- `GET /api/products/` - Get all products
- `GET /api/products/{product_id}` - Get product by ID
- `PUT /api/products/{product_id}` - Update product
- `PATCH /api/products/{product_id}` - Partially update product
- `DELETE /api/products/{product_id}` - Delete product (requires authentication)

### Categories

- `POST /api/categories/` - Create new category
- `GET /api/categories/` - Get all categories
- `GET /api/categories/{category_id}` - Get category by ID
- `PUT /api/categories/{category_id}` - Update category
- `PATCH /api/categories/{category_id}` - Partially update category
- `DELETE /api/categories/{category_id}` - Delete category (requires authentication)

### Product Variants

- `POST /api/product_variants/` - Create new product variant
- `GET /api/product_variants/` - Get all product variants
- `GET /api/product_variants/{variant_id}` - Get variant by ID
- `PUT /api/product_variants/{variant_id}` - Update variant
- `PATCH /api/product_variants/{variant_id}` - Partially update variant
- `DELETE /api/product_variants/{variant_id}` - Delete variant (requires authentication)

### Sizes & Colors

- `POST /api/sizes/` - Create new size
- `GET /api/sizes/` - Get all sizes
- `POST /api/colors/` - Create new color
- `GET /api/colors/` - Get all colors

### Carts

- `POST /api/carts/` - Create new cart
- `GET /api/carts/` - Get all carts
- `GET /api/carts/{cart_id}` - Get cart by ID
- `PUT /api/carts/{cart_id}` - Update cart
- `PATCH /api/carts/{cart_id}` - Partially update cart
- `DELETE /api/carts/{cart_id}` - Delete cart (requires authentication)

### Cart Items

- `POST /api/cart_item/{cart_id}` - Add item to cart
- `GET /api/cart_item/{cart_id}/items` - Get all cart items
- `GET /api/cart_item/{cart_id}/items/{cart_item_id}` - Get cart item by ID
- `PUT /api/cart_item/{cart_id}/items/{cart_item_id}` - Update cart item
- `PATCH /api/cart_item/{cart_id}/items/{cart_item_id}` - Partially update cart item
- `DELETE /api/cart_item/{cart_id}/items/{cart_item_id}` - Delete cart item (requires authentication)

### Orders

- `POST /api/orders/` - Create new order
- `GET /api/orders/` - Get all orders
- `GET /api/orders/{order_id}` - Get order by ID
- `PUT /api/orders/{order_id}` - Update order
- `PATCH /api/orders/{order_id}` - Partially update order
- `DELETE /api/orders/{order_id}` - Delete order (requires authentication)

### Order Items

- `POST /api/order_items/` - Create new order item
- `GET /api/order_items/` - Get all order items
- `GET /api/order_items/{order_item_id}` - Get order item by ID
- `PUT /api/order_items/{order_item_id}` - Update order item
- `PATCH /api/order_items/{order_item_id}` - Partially update order item
- `DELETE /api/order_items/{order_item_id}` - Delete order item (requires authentication)

### System

- `GET /` - Root endpoint (health check)
- `GET /health` - Database health check

## Authentication

Protected endpoints require authentication using Bearer token. To access protected endpoints:

1. Create a user account via `POST /api/users/`
2. Login via `POST /api/users/login` to receive an access token
3. Include the token in subsequent requests:

```bash
Authorization: Bearer <your-access-token>
```

## Database Schema

The application uses the following main entities:

- **User**: User accounts with authentication
- **UserAddress**: User delivery addresses
- **Cart**: Shopping carts linked to users
- **CartItem**: Items in shopping carts
- **Product**: Product catalog items
- **ProductVariant**: Product variations (size, color combinations)
- **Category**: Product categories
- **Size**: Available product sizes
- **Color**: Available product colors
- **Order**: Customer orders
- **OrderItem**: Items within orders

## Development

### Adding New Endpoints

1. Create or update models in `app/*/models/`
2. Create corresponding schemas in `app/*/schemas/`
3. Implement router endpoints in `app/*/routers/`
4. Register router in `app/routers/__init__.py`
5. Write tests in `tests/*/`

### Database Migrations

The current setup uses SQLAlchemy's `create_all()` method on startup. For production, consider implementing Alembic for proper database migrations.

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is open source and available under the [MIT License](LICENSE).

## Contact

For questions or suggestions, please open an issue in the repository.

---

**Note**: This is a development setup. For production deployment, ensure you:
- Use a production-grade database (PostgreSQL, MySQL)
- Implement proper JWT token authentication
- Add rate limiting and security headers
- Set up proper logging and monitoring
- Use environment variables for configuration
- Enable HTTPS/TLS encryption