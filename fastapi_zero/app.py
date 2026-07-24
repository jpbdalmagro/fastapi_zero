from http import HTTPStatus

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy import select

from fastapi_zero.database import get_session
from fastapi_zero.models import User
from fastapi_zero.schemas import (
    Message,
    UserDB,
    UserList,
    UserPublicSchema,
    UserSchema,
)

app = FastAPI()

database = []


@app.get('/', response_model=Message)
def read_root():
    return {'message': 'Hello World'}


@app.post(
    '/users/', status_code=HTTPStatus.CREATED, response_model=UserPublicSchema
)
def create_user(user: UserSchema, session=Depends(get_session)):

    db_user = session.scalar(
        select(User).where(
            (User.username == user.username) | (User.email == user.email)
        )
    )

    if db_user:
        if db_user.username == user.username:
            raise HTTPException(
                detail='Username already exists',
                status_code=HTTPStatus.CONFLICT,
            )
        else:
            raise HTTPException(
                detail='Email already exists', status_code=HTTPStatus.CONFLICT
            )

    db_user = User(
        username=user.username, email=user.email, password=user.password
    )

    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user


@app.get('/users/', status_code=HTTPStatus.OK, response_model=UserList)
def read_users(limit=10, offset=0, session=Depends(get_session)):
    users = session.scalars(select(User).limit(limit).offset(offset))
    return {'users': users}


@app.put('/users/{user_id}', response_model=UserPublicSchema)
def update_user(user_id: int, user: UserSchema):
    if user_id < 0 or user_id > len(database):
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Não achei padrinho'
        )

    user_with_id = UserDB(id=user_id, **user.model_dump())

    database[user_id - 1] = user_with_id

    return user_with_id


@app.delete(
    '/users/{user_id}', status_code=HTTPStatus.OK, response_model=Message
)
def delete_user(user_id: int):
    if user_id < 0 or user_id > len(database):
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Não achei padrinho'
        )

    del database[user_id - 1]

    return {'message': 'Foi jogar no Vasco'}


@app.get(
    '/users/{user_id}',
    status_code=HTTPStatus.OK,
    response_model=UserPublicSchema,
)
def get_user_by_id(user_id: int):
    if user_id < 0 or user_id > len(database):
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Não achei padrinho'
        )

    return database[user_id - 1]
