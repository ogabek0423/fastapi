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


