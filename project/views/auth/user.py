from flask import request
from flask_restx import Namespace, Resource

from project.container import user_service
from project.decorators import auth_required
from project.setup.api.models import user

api = Namespace('user')


@api.route('/')
class UserViews(Resource):
    """
    Класс данных о пользователях
    """
    @auth_required
    @api.marshal_with(user, as_list=True, code=200, description='OK')
    def get(self):
        """
        Получаем одного пользователя
        """
        data = request.headers['Authorization']
        return user_service.decode_token(data), 200

    @auth_required
    @api.marshal_with(user, as_list=True, code=200, description='OK')
    def patch(self):
        """
        Изменяем данные пользователя, кроме пароля
        """
        patched_user = request.json

        data = request.headers['Authorization']
        user = user_service.decode_token(data)

        return user_service.patch_user(patched_user, user), 201


@api.route('/password/')
class UserViews(Resource):
    @auth_required
    def put(self):
        """
        Изменяем пароль пользователя
        """
        req_json = request.json
        new_password = req_json["password"]

        data = request.headers['Authorization']
        user = user_service.decode_token(data)

        return user_service.change_password(user, new_password), 201
