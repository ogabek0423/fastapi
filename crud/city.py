from fastapi import APIRouter
from db.database import Session, ENGINE
from db.schemas import CityModel
from db.models import City
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


@city_router.get("/{id}")
async def get_all_cities(id: int):
    check_city = session.query(City).filter(City.id == id).first()
    context = [
        {
            "id": check_city.id,
            "name": check_city.name
        }
    ]
    return jsonable_encoder(context)


@city_router.post('/create_city')
async def create_city(city: CityModel):
    city_check = session.query(City).filter(City.id == city.id).first()
    if city_check:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="City already exists")

    new_city = City(
        id=city.id,
        name=city.name
    )
    session.add(new_city)
    session.commit()
    return HTTPException(status_code=status.HTTP_201_CREATED, detail="city created successfully")


@city_router.put("/{id}")
async def update_city(id: int, city: CityModel):
    check = session.query(City).filter(City.id == id).first()
    check_id = session.query(City).filter(City.id == city.id).first()
    if check:
        if check_id is None or check_id.id == id:
            for key, value in city.dict(exclude_unset=True).items():
                setattr(check, key, value)
                session.commit()

            data = {
                "code": 200,
                "message": "update city"
            }
            return jsonable_encoder(data)

        return HTTPException(status_code=status.HTTP_409_CONFLICT, detail="yangi berilgan id da malumot mavjud!")

    return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")


@city_router.delete("/{id}")
async def delete_city(id: int):
    check = session.query(City).filter(City.id == id).first()
    if check:
        session.delete(check)
        session.commit()
        return HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="Deleted")

    return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")


