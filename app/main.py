from typing import Union
from fastapi import FastAPI
from pydantic import BaseModel as PydanticBaseModel
from app.core.settings.db import Database
from contextlib import asynccontextmanager
from .core.models.base import BaseModel


DATABASE_URL = "sqlite+aiosqlite:///./test.db"


@asynccontextmanager
async def lifespan(_fastapi_app: FastAPI):
   await db.connect()
   async with db.engine.begin() as connection:
       await connection.run_sync(BaseModel.metadata.create_all)
   yield
   await db.disconnect()

db = Database(url=DATABASE_URL)
app = FastAPI(lifespan=lifespan)


class Item(PydanticBaseModel):
    name: str
    price: float
    is_offer: Union[bool, None] = None

@app.get(path="/health", tags=["System"])
async def health():
   ok = await db.ping()
   return {"status": "ok" if ok else "error"}
@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {"item_name": item.name, "item_id": item_id}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        app,
        port=8000,
        log_level="info",
        use_colors=False,
    )
