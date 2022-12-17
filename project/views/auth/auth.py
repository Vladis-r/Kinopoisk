from flask_restx import Namespace, Resource
from flask import request, abort

from project.container import auth_service

api = Namespace('auth')


@api.route('/register/')
class AuthRegisterViews(Resource):
    """
    Класс регистрации и аутентификации пользователей
    """
    def post(self):
        """
        Получаем {email, password} от пользователя и сохраняем в БД
        """
        req_json = request.json
        email = req_json.get("email", None)
        password = req_json.get("password", None)
        if None in [email, password]:
            abort(400)
        auth_service.register_user(req_json)
        return 'Пользователь успешно зарегистрирован', 201


@api.route('/login/')
class AuthLoginViews(Resource):
    """
    Проводим аутентификацию пользователя
    """
    def post(self):
        """
        Аутентификация пользователя по email и password
        :return: access и refresh tokens
        """
        req_json = request.json
        email = req_json.get("email", None)
        password = req_json.get("password", None)
        if None in [email, password]:
            abort(400)

        return auth_service.login_user(req_json), 201

    def put(self):
        """
        Обновляем токены пользователю
        """
        tokens = request.json
        tokens = auth_service.approve_refresh_token(tokens["refresh_token"])
        if not tokens:
            return 'Время действия токена истекло, пройдите авторизацию', 401
        else:
            return tokens, 201
