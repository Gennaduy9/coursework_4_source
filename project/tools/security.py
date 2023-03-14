import base64
import hashlib
import hmac
from typing import Union


from flask import current_app


def __generate_password_digest(password: str) -> bytes:
    """
    Генерация хеш-пароля

    """
    return hashlib.pbkdf2_hmac(
        hash_name="sha256",
        password=password.encode("utf-8"),
        salt=current_app.config["PWD_HASH_SALT"],
        iterations=current_app.config["PWD_HASH_ITERATIONS"],
    )


def generate_password_hash(password: str) -> str:
    """
    Генерация хеш-пароля

    """
    return base64.b64encode(__generate_password_digest(password)).decode('utf-8')


def compose_passwords(password_hash: Union[str, bytes], password: str) -> bool:
    """
    Сравнение вводимого пароля и пароля, хранящегося в БД

    """
    return hmac.compare_digest(
        base64.b64decode(password_hash),
        hashlib.pbkdf2_hmac('sha256',
                            password=password.encode('utf-8'),
                            salt=current_app.config["PWD_HASH_SALT"],
                            iterations=current_app.config["PWD_HASH_ITERATIONS"])
    )

