# E-Commerce API

**Українська** | [English](README.md)

Сучасний RESTful API для e-commerce додатків, побудований на FastAPI та SQLAlchemy. Цей проєкт надає повне backend рішення для управління продуктами, користувачами, замовленнями та кошиками покупок.

## Можливості

- **Управління користувачами**: Повна система автентифікації з реєстрацією, входом та управлінням профілем
- **Каталог продуктів**: Мультикатегорійна система продуктів з варіантами (розмір, колір), відстеження інвентарю
- **Кошик покупок**: Постійна функціональність кошика з управлінням товарами
- **Обробка замовлень**: Повне управління життєвим циклом замовлення від створення до завершення
- **Async/Await**: Побудовано на async Python для високої продуктивності
- **База даних**: SQLAlchemy ORM з підтримкою async, SQLite для розробки
- **Тестування**: Комплексний набір тестів з використанням pytest та фабрик

## Технологічний стек

- **Фреймворк**: FastAPI
- **База даних**: SQLAlchemy (async), SQLite
- **Автентифікація**: OAuth2 з Password flow
- **Хешування паролів**: Passlib з bcrypt
- **Тестування**: Pytest, pytest-asyncio, Factory Boy, Faker
- **HTTP клієнт**: HTTPX (для тестування)

## Структура проєкту

```
app/
├── core/
│   ├── models/         # Моделі бази даних
│   └── settings/       # Конфігурація та налаштування бази даних
├── users/
│   ├── models/         # Моделі User, Cart, UserAddress
│   ├── routers/        # Ендпоінти користувачів
│   └── schemas/        # Pydantic схеми для валідації
├── products/
│   ├── models/         # Моделі Product, Category, Size, Color, ProductVariant
│   ├── routers/        # Ендпоінти продуктів
│   └── schemas/        # Pydantic схеми
├── orders/
│   ├── models/         # Моделі Order, OrderItem, CartItem
│   ├── routers/        # Ендпоінти замовлень
│   └── schemas/        # Pydantic схеми
├── utils/              # Утиліти (автентифікація, шифрування)
└── main.py             # Точка входу додатку

tests/
├── users/              # Тести користувачів
├── products/           # Тести продуктів
├── orders/             # Тести замовлень
└── conftest.py         # Конфігурація pytest та фікстури
```

## Встановлення

### Передумови

- Python 3.9 або вище
- Менеджер пакетів pip

### Налаштування

1. Клонуйте репозиторій:
```bash
git clone <repository-url>
cd <project-directory>
```

2. Створіть та активуйте віртуальне середовище:
```bash
python -m venv venv
source venv/bin/activate  # На Windows: venv\Scripts\activate
```

3. Встановіть залежності:
```bash
pip install -r requirements.txt
```

## Запуск додатку

Запустіть сервер розробки:

```bash
python app/main.py
```

API буде доступний за адресою `http://localhost:8000`

Інтерактивна документація API (Swagger UI) буде доступна за адресою:
- `http://localhost:8000/docs`

Альтернативна документація API (ReDoc) за адресою:
- `http://localhost:8000/redoc`

## Тестування

Запуск повного набору тестів:

```bash
pytest
```

Запуск тестів зі звітом покриття:

```bash
pytest --cov=app
```

Запуск конкретного файлу тестів:

```bash
pytest tests/users/test_user_endpoints.py
```

## API Ендпоінти

### Автентифікація

- `POST /api/users/login` - Вхід користувача (повертає токен доступу)

### Користувачі

- `POST /api/users/` - Створити нового користувача
- `GET /api/users/` - Отримати всіх користувачів
- `GET /api/users/{user_id}` - Отримати користувача за ID
- `PUT /api/users/{user_id}` - Оновити користувача
- `PATCH /api/users/{user_id}` - Частково оновити користувача
- `DELETE /api/users/{user_id}` - Видалити користувача (потрібна автентифікація)

### Адреси користувачів

- `POST /api/user_addresses/` - Створити нову адресу
- `GET /api/user_addresses/` - Отримати всі адреси
- `GET /api/user_addresses/{address_id}` - Отримати адресу за ID
- `PUT /api/user_addresses/{address_id}` - Оновити адресу
- `PATCH /api/user_addresses/{address_id}` - Частково оновити адресу
- `DELETE /api/user_addresses/{address_id}` - Видалити адресу (потрібна автентифікація)

### Продукти

- `POST /api/products/` - Створити новий продукт
- `GET /api/products/` - Отримати всі продукти
- `GET /api/products/{product_id}` - Отримати продукт за ID
- `PUT /api/products/{product_id}` - Оновити продукт
- `PATCH /api/products/{product_id}` - Частково оновити продукт
- `DELETE /api/products/{product_id}` - Видалити продукт (потрібна автентифікація)

### Категорії

- `POST /api/categories/` - Створити нову категорію
- `GET /api/categories/` - Отримати всі категорії
- `GET /api/categories/{category_id}` - Отримати категорію за ID
- `PUT /api/categories/{category_id}` - Оновити категорію
- `PATCH /api/categories/{category_id}` - Частково оновити категорію
- `DELETE /api/categories/{category_id}` - Видалити категорію (потрібна автентифікація)

### Варіанти продуктів

- `POST /api/product_variants/` - Створити новий варіант продукту
- `GET /api/product_variants/` - Отримати всі варіанти продуктів
- `GET /api/product_variants/{variant_id}` - Отримати варіант за ID
- `PUT /api/product_variants/{variant_id}` - Оновити варіант
- `PATCH /api/product_variants/{variant_id}` - Частково оновити варіант
- `DELETE /api/product_variants/{variant_id}` - Видалити варіант (потрібна автентифікація)

### Розміри та кольори

- `POST /api/sizes/` - Створити новий розмір
- `GET /api/sizes/` - Отримати всі розміри
- `POST /api/colors/` - Створити новий колір
- `GET /api/colors/` - Отримати всі кольори

### Кошики

- `POST /api/carts/` - Створити новий кошик
- `GET /api/carts/` - Отримати всі кошики
- `GET /api/carts/{cart_id}` - Отримати кошик за ID
- `PUT /api/carts/{cart_id}` - Оновити кошик
- `PATCH /api/carts/{cart_id}` - Частково оновити кошик
- `DELETE /api/carts/{cart_id}` - Видалити кошик (потрібна автентифікація)

### Елементи кошика

- `POST /api/cart_item/{cart_id}` - Додати товар до кошика
- `GET /api/cart_item/{cart_id}/items` - Отримати всі товари кошика
- `GET /api/cart_item/{cart_id}/items/{cart_item_id}` - Отримати товар кошика за ID
- `PUT /api/cart_item/{cart_id}/items/{cart_item_id}` - Оновити товар кошика
- `PATCH /api/cart_item/{cart_id}/items/{cart_item_id}` - Частково оновити товар кошика
- `DELETE /api/cart_item/{cart_id}/items/{cart_item_id}` - Видалити товар кошика (потрібна автентифікація)

### Замовлення

- `POST /api/orders/` - Створити нове замовлення
- `GET /api/orders/` - Отримати всі замовлення
- `GET /api/orders/{order_id}` - Отримати замовлення за ID
- `PUT /api/orders/{order_id}` - Оновити замовлення
- `PATCH /api/orders/{order_id}` - Частково оновити замовлення
- `DELETE /api/orders/{order_id}` - Видалити замовлення (потрібна автентифікація)

### Елементи замовлення

- `POST /api/order_items/` - Створити новий елемент замовлення
- `GET /api/order_items/` - Отримати всі елементи замовлень
- `GET /api/order_items/{order_item_id}` - Отримати елемент замовлення за ID
- `PUT /api/order_items/{order_item_id}` - Оновити елемент замовлення
- `PATCH /api/order_items/{order_item_id}` - Частково оновити елемент замовлення
- `DELETE /api/order_items/{order_item_id}` - Видалити елемент замовлення (потрібна автентифікація)

### Система

- `GET /` - Кореневий ендпоінт (перевірка працездатності)
- `GET /health` - Перевірка стану бази даних

## Автентифікація

Захищені ендпоінти вимагають автентифікації за допомогою Bearer токену. Для доступу до захищених ендпоінтів:

1. Створіть обліковий запис користувача через `POST /api/users/`
2. Увійдіть через `POST /api/users/login`, щоб отримати токен доступу
3. Включайте токен у наступні запити:

```bash
Authorization: Bearer <ваш-токен-доступу>
```

## Схема бази даних

Додаток використовує наступні основні сутності:

- **User**: Облікові записи користувачів з автентифікацією
- **UserAddress**: Адреси доставки користувачів
- **Cart**: Кошики покупок, прив'язані до користувачів
- **CartItem**: Товари в кошиках покупок
- **Product**: Елементи каталогу продуктів
- **ProductVariant**: Варіації продуктів (комбінації розмірів, кольорів)
- **Category**: Категорії продуктів
- **Size**: Доступні розміри продуктів
- **Color**: Доступні кольори продуктів
- **Order**: Замовлення клієнтів
- **OrderItem**: Елементи в замовленнях

## Розробка

### Додавання нових ендпоінтів

1. Створіть або оновіть моделі в `app/*/models/`
2. Створіть відповідні схеми в `app/*/schemas/`
3. Реалізуйте ендпоінти роутера в `app/*/routers/`
4. Зареєструйте роутер в `app/routers/__init__.py`
5. Напишіть тести в `tests/*/`

### Міграції бази даних

Поточне налаштування використовує метод `create_all()` SQLAlchemy при запуску. Для production розгляньте можливість впровадження Alembic для належних міграцій бази даних.

## Співпраця

1. Форкніть репозиторій
2. Створіть гілку з новою функцією (`git checkout -b feature/amazing-feature`)
3. Закомітьте свої зміни (`git commit -m 'Add some amazing feature'`)
4. Запуште в гілку (`git push origin feature/amazing-feature`)
5. Відкрийте Pull Request

## Ліцензія

Цей проєкт є відкритим кодом і доступний під [MIT License](LICENSE).

## Контакти

Для питань або пропозицій, будь ласка, відкрийте issue в репозиторії.

---

**Примітка**: Це налаштування для розробки. Для production розгортання переконайтеся, що ви:
- Використовуєте production-grade базу даних (PostgreSQL, MySQL)
- Впроваджуєте належну JWT токен автентифікацію
- Додаєте обмеження частоти запитів та заголовки безпеки
- Налаштовуєте належне логування та моніторинг
- Використовуєте змінні середовища для конфігурації
- Увімкнули HTTPS/TLS шифрування