from pydantic import BaseModel
from typing import Optional


class RegisterUser(BaseModel):
    id: Optional[int]
    first_name: str
    last_name: str
    username: str
    password: str
    email: str
    address_id: Optional[int]


class LoginUser(BaseModel):
    username: str
    password: str
