from project.dao import GenresDAO
from project.dao.main import MoviesDAO
from project.dao.main import DirectorsDAO
from project.dao.auth_dao import AuthDAO
from project.dao.user_dao import UserDAO

from project.services import GenresService
from project.services.movies_service import MoviesService
from project.services.directors_service import DirectorsService
from project.services.auth_service import AuthService
from project.services.user_service import UserService

from project.setup.db import db

# DAO
genre_dao = GenresDAO(db.session)
movie_dao = MoviesDAO(db.session)
director_dao = DirectorsDAO(db.session)
auth_dao = AuthDAO(db.session)
user_dao = UserDAO(db.session)

# Services
genre_service = GenresService(dao=genre_dao)
movie_service = MoviesService(dao=movie_dao)
director_service = DirectorsService(dao=director_dao)
auth_service = AuthService(dao=auth_dao)
user_service = UserService(dao=user_dao)
