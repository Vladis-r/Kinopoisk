import calendar
import datetime
import jwt
from flask_restx import abort
from flask import current_app

from project.dao.auth_dao import AuthDAO
from project.tools.security import generate_password_hash, compose_passwords


class AuthService:
    def __init__(self, dao: AuthDAO):
        self.dao = dao

    def register_user(self, reg_user):
        """
        Хешируем полученный пароль и заносим пользователя в БД
        """
        reg_user["password"] = generate_password_hash(reg_user["password"])
        return self.dao.create_user(reg_user)

    def login_user(self, log_user, is_refresh=False):
        """
        Идентифицируем пользователя по email и password и создаём токены
        :param log_user: {email, password}
        :param is_refresh: Проверка пароля. По умолчанию включена (False)
        :return: Возвращаем {access_token, refresh_token}
        """
        try:
            user = self.dao.get_user_by_email(log_user['email'])
        except Exception as e:
            abort(401, message="Email или пароль неверные, попробуйте ещё раз")

        if not is_refresh:
            if not compose_passwords(user.password, log_user['password']):
                abort(401, message='Email или пароль неверные, попробуйте ещё раз')

        some_min = datetime.datetime.utcnow() + datetime.timedelta(minutes=current_app.config["TOKEN_EXPIRE_MINUTES"])
        log_user["exp"] = calendar.timegm(some_min.timetuple())
        access_token = jwt.encode(log_user, current_app.config["SECRET_KEY"], algorithm=current_app.config["PWD_ALGO"])

        some_days = datetime.datetime.utcnow() + datetime.timedelta(days=current_app.config["TOKEN_EXPIRE_DAYS"])
        log_user["exp"] = calendar.timegm(some_days.timetuple())
        refresh_token = jwt.encode(log_user, current_app.config["SECRET_KEY"], algorithm=current_app.config["PWD_ALGO"])

        return {"access_token": access_token, "refresh_token": refresh_token}

    def approve_refresh_token(self, token):
        """
        Обновляем токены
        """
        try:
            data = jwt.decode(token, current_app.config["SECRET_KEY"], algorithms=current_app.config["PWD_ALGO"])
        except Exception as e:
            return False

        return self.login_user(data, is_refresh=True)
