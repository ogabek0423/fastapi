from db.database import ENGINE, Base
from models import User, Payments, PayType, City, Address, Lesson, Modules, Courses

Base.metadata.create_all(ENGINE)
