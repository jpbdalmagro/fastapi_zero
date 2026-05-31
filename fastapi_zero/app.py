from http import HTTPStatus

from fastapi import FastAPI, HTTPException

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
def create_user(user: UserSchema):

    user_with_id = UserDB(id=len(database) + 1, **user.model_dump())

    database.append(user_with_id)

    return user_with_id


@app.get('/users/', status_code=HTTPStatus.OK, response_model=UserList)
def read_users():
    return {'users': database}


@app.put('/users/{user_id}', response_model=UserPublicSchema)
def update_user(user_id: int, user: UserSchema):
    if not 0 < user_id < len(database):
        raise H
    
    user_with_id = UserDB(id=user_id, **user.model_dump())

    database[user_id - 1] = user_with_id

    return user_with_id
