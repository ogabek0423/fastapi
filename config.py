from fastapi import FastAPI
from auth import a_router
from models import m_router

app = FastAPI()
app.include_router(a_router)
app.include_router(m_router)


@app.get('/')
async def root():
    return {"message": "root xabari"}


@app.get('/items')
async def read_items():
    return {'message': 'test api items'}


@app.get('/test')
async def test():
    return {'message': 'test xabar'}

