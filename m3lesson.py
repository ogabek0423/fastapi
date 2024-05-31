from fastapi import APIRouter
from db.database import Session, ENGINE
from schemas import LessonModel
from models import Lesson
from fastapi import HTTPException, status
from fastapi.encoders import jsonable_encoder


session = Session(bind=ENGINE)
lesson_router = APIRouter(prefix="/lessons")


@lesson_router.get('/')
async def get_all_lessons():
    lessons = session.query(Lesson).all()
    context = [
        {
            'id': lesson.id,
            'title': lesson.title,
            'description': lesson.description,
            'homework': lesson.homework
        }
        for lesson in lessons
    ]
    return jsonable_encoder(context)


@lesson_router.post('/create')
async def create_lesson(lesson: LessonModel):
    lesson_check = session.query(Lesson).filter(Lesson.id == lesson.id)
    if lesson_check:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Lesson already exists")

    new_lesson = LessonModel(
        id=lesson.id,
        title=lesson.title,
        description=lesson.description,
        homework=lesson.homework
    )
    session.add(new_lesson)
    session.commit()
    return HTTPException(status_code=status.HTTP_201_CREATED, detail="Lesson created successfully")

