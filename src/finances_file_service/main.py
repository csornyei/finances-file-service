from typing import Union

from fastapi import FastAPI

from finances_file_service.routes import router

app = FastAPI()

app.include_router(router, prefix="/api/v1", tags=["api"])


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
async def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}
