from fastapi import APIRouter

m_router = APIRouter(prefix="/models")


@m_router.get('/')
async def test():
    return {
        'message': 'test xabar'
    }


@m_router.get('/z')
async def test2():
    z = {
        'code': 'python',
        'api': 'fast api',
        'host': 'localhost',
    }
    return z


@m_router.get('/model1')
async def model1():
    return {
        'message': 'model 1 page'
    }


@m_router.get('/model2')
async def model2():
    return {
        'message': 'model 2 page'
    }


@m_router.get('/model3')
async def model3():
    return {
        'message': 'model 3 page'
    }


