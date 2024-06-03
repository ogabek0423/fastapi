from fastapi import APIRouter
from db.database import Session, ENGINE
from db.schemas import CourseModel
from db.models import Courses, Modules, User
from fastapi import HTTPException, status
from fastapi.encoders import jsonable_encoder


session = Session(bind=ENGINE)
course_router = APIRouter(prefix="/courses")


@course_router.get("/")
async def get_courses():
    courses = session.query(Courses).all()
    return jsonable_encoder(courses)


@course_router.get("/{id}")
async def get_courses(id: int):
    courses = session.query(Courses).filter(Courses.id == id).first()
    return jsonable_encoder(courses)


@course_router.post("/create")
async def create_course(course: CourseModel):
    check = session.query(Courses).filter(Courses.id == course.id).first()
    if check:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="This course already exists")

    new_course = Courses(
        id=course.id,
        name=course.name,
        description=course.description,
        module_id=course.module_id,
        user_id=course.user_id
    )
    session.add(new_course)
    session.commit()
    return HTTPException(status_code=status.HTTP_201_CREATED, detail="Course created successfully")


@course_router.put("/{id}")
async def update_course(id: int, course: CourseModel):
    check = session.query(Courses).filter(Courses.id == id).first()
    check_new_id = session.query(Courses).filter(Courses.id == course.id).first()
    check_user = session.query(User).filter(User.id == course.user_id).first()
    check_module = session.query(Modules).filter(Modules.id == course.module_id).first()
    if check:
        if check_new_id is None or check_new_id.id == course.id:
            if check_user:
                if check_module:
                    for key, value in course.dict().items():
                        setattr(check, key, value)
                        session.commit()
                    data = {
                            "code": 200,
                            "message": "Course updated successfully"
                        }
                    return jsonable_encoder(data)
                return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Module id is not created")
            return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User id is not correct")
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Berilgan yangi id da malumot mavjud!")

    return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="malumot topilmadi")


@course_router.delete("/{id}")
async def delete_course(id: int):
    item = session.query(Courses).filter(Courses.id == id).first()
    if item:
        session.delete(item)
        session.commit()
        return HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="Course deleted successfully")
    return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course does not exist")

