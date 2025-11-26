import pytest
import pytest_asyncio


@pytest_asyncio.fixture()
async def cart_item_payload(cart_factory, product_variant_factory, faker):
    cart = await cart_factory()
    variant = await product_variant_factory()
    return {
        "cart_id": cart.id,
        "product_variant_id": variant.id,
        "quantity": faker.random_int(min=1, max=10),
    }


@pytest.mark.asyncio
async def test_create_cart_item(client, cart_factory, cart_item_payload):
    cart_id = cart_item_payload["cart_id"]
    response = await client.post(f"/api/cart_item/{cart_id}", json=cart_item_payload)
    assert response.status_code == 201
    data = response.json()
    assert data["cart_id"] == cart_item_payload["cart_id"]
    assert data["product_variant_id"] == cart_item_payload["product_variant_id"]
    assert data["quantity"] == cart_item_payload["quantity"]


@pytest.mark.asyncio
async def test_get_cart_items(client, cart_item_factory):
    cart_item1 = await cart_item_factory()
    cart_item2 = await cart_item_factory(cart=cart_item1.cart)
    cart_item3 = await cart_item_factory(cart=cart_item1.cart)

    response = await client.get(f"/api/cart_item/{cart_item1.cart_id}/items")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 3


@pytest.mark.asyncio
async def test_get_cart_item(client, cart_item_factory):
    cart_item = await cart_item_factory()
    response = await client.get(f"/api/cart_item/{cart_item.cart_id}/items/{cart_item.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == cart_item.id
    assert data["cart_id"] == cart_item.cart_id
    assert data["product_variant_id"] == cart_item.product_variant_id
    assert data["quantity"] == cart_item.quantity


@pytest.mark.asyncio
async def test_update_cart_item(client, cart_item_factory, product_variant_factory):
    cart_item = await cart_item_factory()
    new_variant = await product_variant_factory()

    updated_payload = {
        "cart_id": cart_item.cart_id,
        "product_variant_id": new_variant.id,
        "quantity": 5,
    }
    response = await client.put(
        f"/api/cart_item/{cart_item.cart_id}/items/{cart_item.id}",
        json=updated_payload
    )
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == cart_item.id
    assert data["cart_id"] == updated_payload["cart_id"]
    assert data["product_variant_id"] == updated_payload["product_variant_id"]
    assert data["quantity"] == updated_payload["quantity"]


@pytest.mark.asyncio
async def test_partial_update_cart_item(client, cart_item_factory):
    cart_item = await cart_item_factory()
    partial_payload = {
        "quantity": 8,
    }
    response = await client.patch(
        f"/api/cart_item/{cart_item.cart_id}/items/{cart_item.id}",
        json=partial_payload
    )
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == cart_item.id
    assert data["quantity"] == partial_payload["quantity"]
    assert data["cart_id"] == cart_item.cart_id
    assert data["product_variant_id"] == cart_item.product_variant_id


@pytest.mark.asyncio
async def test_delete_cart_item(client, cart_item_factory, auth_headers):
    cart_item = await cart_item_factory()
    response = await client.delete(
        f"/api/cart_item/{cart_item.cart_id}/items/{cart_item.id}",
        headers=auth_headers
    )
    assert response.status_code == 204


@pytest.mark.asyncio
async def test_delete_cart_item_unauthorized(client, cart_item_factory):
    cart_item = await cart_item_factory()
    response = await client.delete(
        f"/api/cart_item/{cart_item.cart_id}/items/{cart_item.id}"
    )
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_get_nonexistent_cart_item(client, cart_factory):
    cart = await cart_factory()
    response = await client.get(f"/api/cart_item/{cart.id}/items/9999")
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Cart item not found"


@pytest.mark.asyncio
async def test_get_cart_items_empty_cart(client, cart_factory):
    cart = await cart_factory()
    response = await client.get(f"/api/cart_item/{cart.id}/items")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 0