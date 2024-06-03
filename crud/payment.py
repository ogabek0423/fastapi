from fastapi import APIRouter
from db.database import Session, ENGINE
from db.schemas import PayModel
from db.models import Payments, User
from fastapi import HTTPException, status
from fastapi.encoders import jsonable_encoder


session = Session(bind=ENGINE)
pay_router = APIRouter(prefix="/payment")


@pay_router.get('/')
async def get_all_payments():
    payments = session.query(Payments).all()
    return jsonable_encoder(payments)


@pay_router.get('/{id}')
async def get_all_payments(id: int):
    payment = session.query(Payments).first()
    return jsonable_encoder(payment)


@pay_router.post('/create')
async def create_payment(payment: PayModel):
    check = session.query(Payments).filter(Payments.id == payment.id).first()
    if check:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Payment already exists")

    new_payment = Payments(
        id=payment.id,
        amount=payment.amount,
        type=payment.type,
        user_id=payment.user_id
    )
    session.add(new_payment)
    session.commit()
    return HTTPException(status_code=status.HTTP_201_CREATED, detail="Payment created successfully")


@pay_router.put('/{id}')
async def update_payment(id: int, update: PayModel):
    check = session.query(Payments).filter(Payments.id == id).first()
    new_id = session.query(Payments).filter(Payments.id == update.id).first()
    user_id = session.query(User).filter(User.id == update.user_id).first()

    if check:
        if new_id is None or new_id.id == update.id:
            if user_id:
                for key, value in update.dict().items():
                    setattr(check, key, value)
                    session.commit()
                data = {
                    "code": 200,
                    "message": "Payment updated successfully"
                }
                return jsonable_encoder(data)
            return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bunday user mavjud emas!")
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Berilgan yangi id da malumot mavjud!")
    return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=" malumot topilmadi!")


@pay_router.delete("/{id}")
async def delete_payment(id: int):
    item = session.query(Payments).filter(Payments.id == id).first()
    if item:
        session.delete(item)
        session.commit()
        data = {"message": "Payment deleted successfully"}
        return jsonable_encoder(data)

    return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="not found")
