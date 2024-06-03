from fastapi import APIRouter
from db.database import Session, ENGINE
from db.schemas import ModuleModel
from db.models import Modules, Lesson
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


@module_router.get("/{id}")
async def get_modules(id: int):
    module = session.query(Modules).filter(Modules.id == id).first()
    context = [
        {
            "id": module.id,
            "name": module.name,
            "description": module.description,
            "lesson_id": module.lesson_id
        }
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


@module_router.put('/{id}')
async def update_module(id: int, module: ModuleModel):
    check = session.query(Modules).filter(Modules.id == id).first()
    check_new_id = session.query(Modules).filter(Modules.id == module.id).first()
    lesson_id = session.query(Lesson).filter(Lesson.id == module.lesson_id).first()
    if check:
        if lesson_id:
            if check_new_id is None or check_new_id.id == id:
                for key, value in module.dict().items():
                    setattr(check, key, value)
                    session.commit()

                data = {
                    "code": 200,
                    "message": "Module updated"
                }

                return jsonable_encoder(data)

            return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Module uchun bu id allaqachon ishlatilgan")
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bunday id ga ega dars yo'q")
    return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="malumot topilmadi!")


@module_router.delete("/{id}")
async def delete_module(id: int):
    modul = session.query(Modules).filter(Modules.id == id).first()
    if modul:
        session.delete(modul)
        session.commit()
        return HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="Module deleted")
    return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found!")
