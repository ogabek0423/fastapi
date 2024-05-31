from fastapi import APIRouter
from db.database import Session, ENGINE
from schemas import PayTypeModel
from models import PayType
from fastapi import HTTPException, status
from fastapi.encoders import jsonable_encoder


session = Session(bind=ENGINE)
pyt_router = APIRouter(prefix="/pyt")


@pyt_router.get('/')
async def get_all_pay_types():
    pyt_list = session.query(PayType).all()
    return jsonable_encoder(pyt_list)


@pyt_router.post('/create')
async def create_pay_type(pytype: PayTypeModel):
    check = session.query(PayType).filter(PayType.id == pytype.id)
    if check:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='PayType already exists')

    pay_type = PayType(
        id=pytype.id,
        type=pytype.type
    )
    session.add(pay_type)
    session.commit()
    return HTTPException(status_code=status.HTTP_201_CREATED, detail='PayType created successfully')


