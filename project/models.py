from sqlalchemy import Column, String, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship

from project.setup.db import models


class Genre(models.Base):
    __tablename__ = 'genres'
    name = Column(String(100), unique=True, nullable=False)


class Director(models.Base):
    __tablename__ = 'directors'
    name = Column(String(100), unique=True, nullable=False)


class Movie(models.Base):
    __tablename__ = 'movies'
    title = Column(String(255), nullable=False)
    description = Column(String(255), nullable=False)
    trailer = Column(String(255), nullable=False)
    year = Column(Integer, nullable=False)
    rating = Column(Float, nullable=False)
    genre_id = Column(Integer, ForeignKey("genres.id"), nullable=False)
    genre = relationship("Genre")
    director_id = Column(Integer, ForeignKey("directors.id"), nullable=False)
    director = relationship("Director")


class User(models.Base):
    __tablename__ = 'users'
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(300), nullable=False)
    name = Column(String(100))
    surname = Column(String(100))
    favourite_genre = Column(Integer, ForeignKey(f'{Genre.__tablename__}.id'))
    genre = relationship("Genre")
