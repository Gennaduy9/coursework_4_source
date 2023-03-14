

from flask import Flask, jsonify, render_template


# from sqlalchemy.event import api
# from requests import api
# from charset_normalizer import api

from flask_restx import api

from project.exceptions import BaseServiceError

from project.setup.api import api

from project.setup.db import db

from project.views import auth_ns, genres_ns, user_ns, directors_ns, movies_ns

from project.views.auth.auth import api
from project.views.auth.user import api
from project.views.main.directors import api
from project.views.main.genres import api
from project.views.main.movies import api


def base_service_error_handler(exception: BaseServiceError):
    return jsonify(
        {
            'error': str(exception)
        }
    ), exception.code


def create_app(config_object):
    app = Flask(__name__)
    app.config.from_object(config_object)

    db.init_app(app)

    @app.route('/')
    def index():
        return render_template('index.html')

    api.init_app(app)

    # Регистрация эндпоинтов
    api.add_namespace(auth_ns)
    api.add_namespace(user_ns)
    api.add_namespace(genres_ns)
    api.add_namespace(directors_ns)
    api.add_namespace(movies_ns)

    app.register_error_handler(BaseServiceError, base_service_error_handler)

    return app
