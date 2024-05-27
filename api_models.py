from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tags: list[str] = []
    tax: float | None = None


@app.get('/items')
async def read_items() -> list[Item]:
    return [
        Item(name='test name', description='test description', price=123),
        Item(name='test name', description='test description', price=321),
    ]