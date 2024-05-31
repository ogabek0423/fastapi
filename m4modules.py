from fastapi import APIRouter
from db.database import Session, ENGINE
from schemas import ModuleModel
from models import Modules
from fastapi import HTTPException, status
from fastapi.encoders import jsonable_encoder


session = Session(bind=ENGINE)
module_router = APIRouter(prefix="/modules")


@module_router.get("/")
async def get_modules():
    modules = session.query(Modules).all()
    context = [
        {
            "id": module.id,
            "name": module.name,
            "description": module.description,
            "lesson_id": module.lesson_id
        }
        for module in modules
    ]

    return jsonable_encoder(context)


@module_router.post('/create')
async def create_module(module: ModuleModel):
    check_module = session.query(Modules).filter(Modules.id == module.id).first()
    if check_module:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Module already exists")

    module_data = Modules(
        id=module.id,
        name=module.name,
        description=module.description,
        lesson_id=module.lesson_id
    )
    session.add(module_data)
    session.commit()
    return HTTPException(status_code=status.HTTP_201_CREATED, detail="Module created successfully")

