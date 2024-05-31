from fastapi import APIRouter
from db.database import Session, ENGINE
from schemas import AddressModel
from models import Address
from fastapi import HTTPException, status
from fastapi.encoders import jsonable_encoder


session = Session(bind=ENGINE)
address_router = APIRouter(prefix="/address")


@address_router.get('/')
async def get_addresses():
    addresses = session.query(Address).all()
    context = [
        {
            "id": address.id,
            "name": address.name,
            "city_id": address.city_id
        }
        for address in addresses
    ]

    return jsonable_encoder(context)


@address_router.post('/create_address')
async def create_address(address: AddressModel):
    adr_check = session.query(Address).filter(Address.id == address.id)
    if adr_check:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Address is already registered")

    new_adr = Address(
        id=address.id,
        name=address.name,
        city_id=address.city_id
    )
    session.add(new_adr)
    session.commit()
    return HTTPException(status_code=status.HTTP_201_CREATED, detail="Address has been created!")

