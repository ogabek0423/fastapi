from fastapi import APIRouter
from db.database import Session, ENGINE
from schemas import CourseModel
from models import Courses
from fastapi import HTTPException, status
from fastapi.encoders import jsonable_encoder


session = Session(bind=ENGINE)
course_router = APIRouter(prefix="/courses")


@course_router.get("/")
async def get_courses():
    courses = session.query(Courses).all()
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
