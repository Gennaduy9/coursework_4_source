from typing import Optional

from flask_sqlalchemy import BaseQuery

from sqlalchemy import desc
from sqlalchemy.exc import IntegrityError

from werkzeug.exceptions import NotFound

from project.models import Genre
from project.models import Director
from project.models import Movie
from project.models import User
from project.exceptions import UserAlreadyExists
from project.tools.security import generate_password_hash


from project.dao.base import BaseDAO


class GenresDAO(BaseDAO[Genre]):
    __model__ = Genre


class DirectorsDAO(BaseDAO[Director]):
    __model__ = Director


class MoviesDAO(BaseDAO[Movie]):
    __model__ = Movie

    def get_all_by_filter(self, status: Optional[str], page: Optional[int] = None) -> list[Movie]:
        stmt: BaseQuery = self._db_session.query(self.__model__)
        if status == 'new':
            stmt = stmt.order_by(desc(self.__model__.year))
        else:
            stmt = stmt.order_by(self.__model__.year)
        if page:
            try:
                return stmt.paginate(page, self._items_per_page).items
            except NotFound:
                return []
        return stmt.all()


class UserDAO:
    def __init__(self, session):
        self.session = session

    def get_one(self, uid):
        return self.session.query(User).get(uid)

    def get_by_email(self, email):
        return self.session.query(User).filter(User.email == email).first()

    def get_all(self):
        return self.session.query(User).all()

    def create(self, user_d):
        try:
            user = User(**user_d)
            self.session.add(user)
            self.session.commit()
        except IntegrityError:
            raise UserAlreadyExists
        return user

    def delete(self, uid):
        user = self.get_one(uid)
        self.session.delete(user)
        self.session.commit()

    def update(self, user_data):
        user = self.get_one(user_data.get("id"))
        if user_data.get("email"):
            user.email = user_data.get("email")
        if user_data.get("password"):
            user.password = user_data.get("password")
        if user_data.get("name"):
            user.name = user_data.get("name")
        if user_data.get("surname"):
            user.surname = user_data.get("surname")
        if user_data.get("favourite_genre"):
            user.favourite_genre = user_data.get("favourite_genre")
        try:
            self.session.add(user)
            self.session.commit()
        except IntegrityError:
            raise UserAlreadyExists

    def update_password(self, email, new_password):
        user = self.get_by_email(email)
        user.password = generate_password_hash(new_password)

        self.session.add(user)
        self.session.commit()

