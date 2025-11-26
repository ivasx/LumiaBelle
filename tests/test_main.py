import pytest


@pytest.mark.asyncio
async def test_root_endpoint(client):
    response = await client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data == {"Hello": "World"}


@pytest.mark.asyncio
async def test_health_endpoint(client):
    response = await client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert data["status"] in ["ok", "error"]


@pytest.mark.asyncio
async def test_nonexistent_endpoint(client):
    response = await client.get("/nonexistent")
    assert response.status_code == 404