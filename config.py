from fastapi import FastAPI
from auth import a_router


app = FastAPI()
app.include_router(a_router)



@app.get('/')
async def root():
    return {"message": "root xabari"}


@app.get('/items')
async def read_items():
    return {'message': 'test api items'}


@app.get('/user')
async def user():
    return {'message': 'user page'}


@app.get('/user/{id}')
async def read_user(id: int):
    return {'message': f'user id = {id}'}

