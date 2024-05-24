from fastapi import APIRouter

a_router = APIRouter(prefix='/auth', tags=['auth'])


@a_router.get('/')
async def hello():
    return {
        'message': 'Hello World api!'
    }


@a_router.get('/login')
async def login():
    return {
        'message': 'login page'
    }


@a_router.get('/register')
async def register():
    return {
        'message': 'register page'
    }


@a_router.get('/logout')
async def logout():
    return {
        'message': 'logout page'
    }
