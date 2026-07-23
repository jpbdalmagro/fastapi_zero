from sqlalchemy import select

from fastapi_zero.models import User


def test_create_user(session):
    user = User(username='teste', email='mail@mail.com', password='teste')

    session.add(user)
    session.commit()
    result = session.scalar(select(User).where(User.email == 'mail@mail.com'))

    assert result.username == 'teste'
