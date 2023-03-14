from flask import request
from flask_restx import Namespace, Resource

from project.container import user_service
from project.setup.api.models import user

api = Namespace('user')


@api.route('/') # информация о пользователе в БД
class UserView(Resource):
    @api.expect(user)
    @api.response(201, description='OK')
    def get(self):
        """
        Получаем информацию о пользователе!
        """
        user_service.get_one(request.json)
        return "OK", 201

    def patch(self, uid):
        """
        Изменяем информацию пользователя (имя или фамилия или любимый жанр).
        """
        data = request.json
        data["id"] = uid

        user = user_service.update(data)

        if None in [data]:
            return '', 400

        return user, 200


@api.route('/password/') # Обновление пароля пользователя
class UserView(Resource):
    @api.expect(user)
    @api.marshal_with(user, code=200)
    def put(self, uid):
        """
        Обновляем пароль пользователя.
        """
        data = request.json
        password = data.get('password', None)

        if None in [password]:
            return '', 400

        passwords = user_service.update_password(password)

        return passwords, 201
