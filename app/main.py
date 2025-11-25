from typing import Union
from fastapi import FastAPI
from pydantic import BaseModel as PydanticBaseModel
from contextlib import asynccontextmanager

from app.core.settings.db import db
from app.core.models.base import BaseModel

from app.routers import api_router

@asynccontextmanager
async def lifespan(_fastapi_app: FastAPI):
   await db.connect()
   async with db.engine.begin() as connection:
       await connection.run_sync(BaseModel.metadata.create_all)
   yield
   await db.disconnect()


app = FastAPI(lifespan=lifespan)

app.include_router(api_router, prefix="/api")

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


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        app,
        port=8000,
        log_level="info",
        use_colors=False,
    )
