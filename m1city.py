from fastapi import APIRouter
from db.database import Session, ENGINE
from schemas import CityModel
from models import City
from fastapi import HTTPException, status
from fastapi.encoders import jsonable_encoder


session = Session(bind=ENGINE)

city_router = APIRouter(prefix="/city")


@city_router.get("/")
async def get_all_cities():
    city_list = session.query(City).all()
    context = [
        {
            "id": city.id,
            "name": city.name
        }
        for city in city_list
    ]
    return jsonable_encoder(context)


@city_router.post('/create_city')
async def create_city(city: CityModel):
    city_check = session.query(City).filter(City.id == city.id)
    if city_check is not None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="City already exists")

    new_city = City(
        id=city.id,
        name=city.name
    )
    session.add(new_city)
    session.commit()
    return HTTPException(status_code=status.HTTP_201_CREATED, detail="city created successfully")


