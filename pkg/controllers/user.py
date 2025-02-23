import json
import jwt
import datetime
from typing import Optional
from fastapi import APIRouter, status, Depends, HTTPException, Header
from pydantic import BaseModel
from starlette.responses import Response
from schemas.user import UserSchema, UserSignInSchema

from pkg.services import user as user_service

router = APIRouter()


# секретный ключ для JWT
SECRET_KEY = "mysecretkey"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30 # время жизни токена


# модель данных для полезной нагрузки токена
class TokenPayload(BaseModel):
    id: int
    role: str
    exp: datetime.datetime


def create_access_token(data: dict, expires_delta: Optional[datetime.timedelta]=None):
    to_encode = data.copy()

    # получаем текущее время в UTC
    if expires_delta:
        expire = datetime.datetime.now(datetime.timezone.utc) + expires_delta
    else:
        expire = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return TokenPayload(**payload)
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials"
        )


# функция для извлечения пользователя из токена
def get_current_user(authorization: str = Header(...)):
    token = authorization.split("Bearer ")[-1]  # извлекаем токен из заголовка
    payload = verify_token(token)
    return payload  # возвращаем юзернейм


@router.post("/sign-up")
def sign_up(user: UserSchema):
    user_from_db = user_service.get_user_by_username(user.username)
    if user_from_db is not None:
        return Response(json.dumps({'error': 'user with this username already exists'}), status.HTTP_400_BAD_REQUEST)
    
    user_service.create_user(user)

    return Response(
        json.dumps({'message': 'user created successfully'}),
        status.HTTP_201_CREATED
    )


@router.post("/sign-in")
def sign_in(user: UserSignInSchema):
    user_from_db = user_service.get_user_by_username_and_password(user.username, user.password)
    if user_from_db is None:
        return Response(
            json.dumps({'error': 'wrong login or password'}), 
            status.HTTP_404_NOT_FOUND
        )

    access_token = create_access_token(
        data={
            "id": user_from_db.id,
            "role": user_from_db.role
        }
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


@router.get("/users")
def get_users():
    return {"users": [{"name": "<NAME>", "email": "<EMAIL>"}]}

