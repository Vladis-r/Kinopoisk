from flask_sqlalchemy import BaseQuery
from sqlalchemy import desc
from werkzeug.exceptions import NotFound
from typing import Optional, List

from project.dao.base import BaseDAO
from project.models import Genre, Movie, Director
from project.dao.base import T


class GenresDAO(BaseDAO[Genre]):
    __model__ = Genre


class MoviesDAO(BaseDAO[Movie]):
    __model__ = Movie

    def get_all_new(self, page: Optional[int] = None) -> List[T]:
        stmt: BaseQuery = self._db_session.query(self.__model__).order_by(desc(self.__model__.year))
        if page:
            try:
                return stmt.paginate(page, self._items_per_page).items
            except NotFound:
                return []
        return stmt.all()


class DirectorsDAO(BaseDAO[Director]):
    __model__ = Director
