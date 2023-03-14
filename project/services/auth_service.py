import calendar
import datetime


import jwt
from flask import current_app
from flask_restx import abort

from project.services.users_service import UserService
from project.tools.security import compose_passwords


class AuthService:
    def __init__(self, user_service: UserService):
        self.user_service = user_service

    def generate_tokens(self, email, password, is_refresh=False):
        user = self.user_service.get_by_email(email)

        if user is None:
            abort(404)

        if not is_refresh:
            if not compose_passwords(user.password, password):
                abort(400)

        data = {
            "email": user.email,
        }

        # 15 min for access_token
        min15 = datetime.datetime.utcnow() + datetime.timedelta(minutes=15)
        data['exp'] = calendar.timegm(min15.timetuple())
        access_token = jwt.encode(data, key=current_app.config["SECRET_KEY"],
                                  algorithm=current_app.config["JWT_ALGORITHM"])

        # 130 days for refresh_token
        days130 = datetime.datetime.utcnow() + datetime.timedelta(days=130)
        data['exp'] = calendar.timegm(days130.timetuple())
        refresh_token = jwt.encode(data, key=current_app.config["SECRET_KEY"],
                                   algorithm=current_app.config["JWT_ALGORITHM"])

        return {
            "access_token": access_token,
            "refresh_token": refresh_token
        }

    def approve_refresh_token(self, refresh_token):
        """
        Функция создания новой пары access_token и refresh_token по refresh_token

        """
        data = jwt.decode(jwt=refresh_token,
                          key=current_app.config["SECRET_KEY"],
                          algorithm=current_app.config["JWT_ALGORITHM"]
        )

        email = data.get("email")
        user = self.user_service.get_by_email(email=email)

        if user is None:
            raise Exception()

        return self.generate_tokens(email, user.password, is_refresh=True)

