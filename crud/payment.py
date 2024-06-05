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
    context = [
        {
            "id": payment.id,
            "amount": payment.amount,
            "user": {
                "id": payment.user_i.id,
                "first_name": payment.user_i.first_name,
                "last_name": payment.user_i.last_name,
                "username": payment.user_i.username,
                "email": payment.user_i.email
            },
            "type": {
                "id": payment.pay_t.id,
                "type": payment.pay_t.type
            },
            "course": {
                "id": payment.course.id,
                "name": payment.course.name,
                "description": payment.course.description,
                "module": {
                    "id": payment.course.modl.id,
                    "name": payment.course.modl.name,
                    "description": payment.course.modl.description,
                    "lesson": {
                        'id': payment.course.modl.lson.id,
                        'title': payment.course.modl.lson.title
                    }
                }
            }
        }
        for payment in payments
    ]
    return jsonable_encoder(context)


@pay_router.get('/{id}')
async def get_one_payment(id: int):
    payment = session.query(Payments).filter(Payments.user_id == id).first()
    data = {
            "id": payment.id,
            "amount": payment.amount,
            "type": {
                "id": payment.pay_t.id,
                "type": payment.pay_t.type
            },
            "user": {
                "id": payment.user_i.id,
                "first_name": payment.user_i.first_name,
                "last_name": payment.user_i.last_name,
                "username": payment.user_i.username,
                "email": payment.user_i.email
            },
            "course": {
                "id": payment.course.id,
                "name": payment.course.name,
                "description": payment.course.description,
                "module": {
                    "id": payment.course.modl.id,
                    "name": payment.course.modl.name,
                    "description": payment.course.modl.description,
                    "lesson": {
                        'id': payment.course.modl.lson.id,
                        'title': payment.course.modl.lson.title
                    }
                }
            }
        }
    return jsonable_encoder(data)


@pay_router.get('/user_pays/{id}')
async def get_user_pays(id: int):
    payments = session.query(Payments).filter(Payments.user_id == id).all()
    if payments:
        context = [
            {
                "id": payment.id,
                "amount": payment.amount,
                "type": {
                    "id": payment.pay_t.id,
                    "type": payment.pay_t.type
                },
                "user": {
                    "id": payment.user_i.id,
                    "first_name": payment.user_i.first_name,
                    "last_name": payment.user_i.last_name,
                    "username": payment.user_i.username,
                    "email": payment.user_i.email
                },
                "course": {
                    "id": payment.course.id,
                    "name": payment.course.name,
                    "description": payment.course.description,
                    "module": {
                        "id": payment.course.modl.id,
                        "name": payment.course.modl.name,
                        "description": payment.course.modl.description,
                        "lesson": {
                            'id': payment.course.modl.lson.id,
                            'title': payment.course.modl.lson.title
                        }
                    }
                }
            }
            for payment in payments
        ]
        return jsonable_encoder(context)
    return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Payment does not exist")


@pay_router.get('/user_total_pay/{id}')
async def user_total_pay(id:int):
    payments = session.query(Payments).filter(Payments.user_id == id).all()
    if payments:
        count = len(payments)
        total = 0
        name = ''
        for payment in payments:
            total += payment.amount
            name = payment.user_i.username
        data = {
            "foydalanuvchi": name,
            "total pay": total,
            "count pay": count
        }
        return jsonable_encoder(data)
    return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Data does not exist")


@pay_router.post('/create')
async def create_payment(payment: PayModel):
    check = session.query(Payments).filter(Payments.id == payment.id).first()
    if check:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Payment already exists")

    new_payment = Payments(
        id=payment.id,
        amount=payment.amount,
        type=payment.type,
        user_id=payment.user_id,
        course_id=payment.course_id
    )
    session.add(new_payment)
    session.commit()
    payment = new_payment
    data = {
            "msg": "Payment created",
            "id": payment.id,
            "amount": payment.amount,
            "type": {
                "id": payment.pay_t.id,
                "type": payment.pay_t.type
            },
            "user": {
                "id": payment.user_i.id,
                "first_name": payment.user_i.first_name,
                "last_name": payment.user_i.last_name,
                "username": payment.user_i.username,
                "email": payment.user_i.email
            },
            "course": {
                "id": payment.course.id,
                "name": payment.course.name,
                "description": payment.course.description,
                "module": {
                    "id": payment.course.modl.id,
                    "name": payment.course.modl.name,
                    "description": payment.course.modl.description,
                    "lesson": {
                        'id': payment.course.modl.lson.id,
                        'title': payment.course.modl.lson.title
                    }
                }
            }
            if payment.course else None
            if payment.course.modl else None
            if payment.course.modl.lson else None
        }
    return HTTPException(status_code=status.HTTP_201_CREATED, detail=data)


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
                payment = check
                data = {
                    "id": payment.id,
                    "amount": payment.amount,
                    "type": {
                        "id": payment.pay_t.id,
                        "type": payment.pay_t.type
                    },
                    "course": {
                        "id": payment.course.id,
                        "name": payment.course.name,
                        "description": payment.course.description,
                        "module": {
                            "id": payment.course.modl.id,
                            "name": payment.course.modl.name,
                            "description": payment.course.modl.description,
                            "lesson": {
                                'id': payment.course.modl.lson.id,
                                'title': payment.course.modl.lson.title
                            }
                        }
                    }
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
