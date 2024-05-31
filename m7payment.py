from fastapi import APIRouter
from db.database import Session, ENGINE
from schemas import PayModel
from models import Payments
from fastapi import HTTPException, status
from fastapi.encoders import jsonable_encoder


session = Session(bind=ENGINE)
pay_router = APIRouter(prefix="/payment")


@pay_router.get('/')
async def get_all_payments():
    payments = session.query(Payments).all()
    return jsonable_encoder(payments)


@pay_router.post('/create')
async def create_payment(payment: PayModel):
    check = session.query(Payments).filter(Payments.id == payment.id)
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



