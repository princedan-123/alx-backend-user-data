#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError
from typing import TypeVar

from user import Base, User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db")
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """A method that adds a new row in the database"""
        row = User(email=email, hashed_password=hashed_password)
        session = self._session
        session.add(row)
        session.commit()
        return row

    def find_user_by(self, **kwargs) -> User:
        """
        A method that takes arbitrary keyword argument,
        with which it filters a query.
        """
        session = self._session
        try:
            query = session.query(User).filter_by(**kwargs).first()
            if not query:
                raise NoResultFound()
        except AttributeError as error:
            raise InvalidRequestError()
        return query

    def update_user(self, user_id: int, **kwargs) -> None:
        """A method that updates a row in the database."""
        session = self._session
        try:
            row = self.find_user_by(id=user_id)
            for attribute, value in kwargs.items():
                setattr(row, attribute, value)
            session.commit()
        except AttributeError as error:
            raise ValueError()
