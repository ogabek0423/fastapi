from fastapi import APIRouter
from db.database import Session, ENGINE
from db.schemas import PayTypeModel
from db.models import PayType
from fastapi import HTTPException, status
from fastapi.encoders import jsonable_encoder


session = Session(bind=ENGINE)
pyt_router = APIRouter(prefix="/pyt")


@pyt_router.get('/')
async def get_all_pay_types():
    pyt_list = session.query(PayType).all()
    return jsonable_encoder(pyt_list)


@pyt_router.get('/{id}')
async def get_all_pay_types(id: int):
    pyt = session.query(PayType).filter(PayType.id == id).first()
    return jsonable_encoder(pyt)


@pyt_router.post('/create')
async def create_pay_type(pytype: PayTypeModel):
    check = session.query(PayType).filter(PayType.id == pytype.id).first()
    if check:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='PayType already exists')

    pay_type = PayType(
        id=pytype.id,
        type=pytype.type
    )
    session.add(pay_type)
    session.commit()
    return HTTPException(status_code=status.HTTP_201_CREATED, detail='PayType created successfully')


@pyt_router.put('/{id}')
async def update_pay_type(id: int, pytype: PayTypeModel):
    check = session.query(PayType).filter(PayType.id == id).first()
    new_id = session.query(PayType).filter(PayType.id == pytype.id).first()
    if check:
        if new_id is not None or new_id.id == pytype.id:
            for key, value in pytype.dict().items():
                setattr(new_id, key, value)
                session.commit()
            data = {
                    "code": 200,
                    "message": "PayType updated successfully"
            }
            return jsonable_encoder(data)

        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="berilgan yangi id da malumot bor")

    return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Malumot topilmadi!")


@pyt_router.delete('/{id}')
async def delete_pay_type(id: int):
    pyt = session.query(PayType).filter(PayType.id == id).first()
    if pyt:
        session.delete(pyt)
        session.commit()
        return HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="PayType deleted successfully")
    return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Malumot topilmadi!")

