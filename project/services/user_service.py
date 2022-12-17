import calendar
import datetime

import jwt
from flask import current_app, abort

from project.dao.user_dao import UserDAO
from project.tools.security import compose_passwords


class UserService:
    def __init__(self, dao: UserDAO):
        self.dao = dao

    def get_user_by_email(self, email):
        """
        Получаем пользователя по email
        """
        return self.dao.get_user_by_email(email)

    def patch_user(self, patched_user, user):
        """
        Обновляем данные о пользователе
        :param patched_user: Новые данные
        :param user: Объект пользователя
        :return: Обновлённый объект пользователя
        """
        return self.dao.patch_user(patched_user, user)

    def decode_token(self, data):
        """
        Декодируем токен и возвращаем пользователя
        """
        token = data.split("Bearer ")[-1]
        try:
            data = jwt.decode(token, current_app.config["SECRET_KEY"], algorithms=current_app.config["PWD_ALGO"])
        except Exception as e:
            abort(401), ""
        user = self.get_user_by_email(data["email"])
        return user

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

    def change_password(self, user, new_password):
        """
        Смена пароля пользователя
        """
        user = self.dao.change_password(user, new_password)
        return self.login_user({"email": user.email, "password": user.password}, is_refresh=True)
