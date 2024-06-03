from fastapi import HTTPException
from fastapi import APIRouter
from fastapi import status
from db.database import Session, ENGINE
from db.models import User, Address
from db.schemas import RegisterUser
from werkzeug import security
from fastapi.encoders import jsonable_encoder

ax_router = APIRouter(prefix='/users_api')
session = Session(bind=ENGINE)


@ax_router.get('/')
async def user_list():
    users = session.query(User).all()
    return jsonable_encoder(users)


@ax_router.get('/{id}')
async def user_one(id:int):
    user = session.query(User).filter(User.id == id).first()
    return jsonable_encoder(user)


@ax_router.post('/create')
async def create(user: RegisterUser):
    username = session.query(User).filter(User.username == user.username).first()
    if username:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Bunday foydalanuvchi mavjud boshqa yarating')

    email = session.query(User).filter(User.email == user.email).first()
    if email or username is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Bunday foydalanuvchi royxatdan otgan')

    new_user = User(
        id=user.id,
        first_name=user.first_name,
        last_name=user.last_name,
        username=user.username,
        email=user.email,
        password=security.generate_password_hash(user.password),
        address_id=user.address_id
    )

    session.add(new_user)
    session.commit()
    raise HTTPException(status_code=status.HTTP_201_CREATED, detail='succes')


@ax_router.put('/{id}')
async def update(id: int, user: RegisterUser):
    adr = session.query(Address).filter(Address.id == user.address_id).first()
    user_check = session.query(User).filter(User.id == id).first()
    id_check = session.query(User).filter(User.id == user.id).first()
    if user_check:
        if adr:
            if id_check is None or adr.id == user.id:
                for key, value in user.dict().items():
                    setattr(user_check, key, value)
                    session.commit()
                data = {
                    "code": 200,
                    "msg": "success"
                }
                return jsonable_encoder(data)
            return HTTPException(status_code=status.HTTP_409_CONFLICT, detail='berilgan id malumotga ega')
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Berilgan manzil id mavjud emas!')
    return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User topilmadi!')


@ax_router.delete('/{id}')
async def delete(id: int):
    x = session.query(User).filter(User.id == id).first()
    if x:
        session.delete(x)
        session.commit()

        return HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail='deleted')

    return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='user not found')

