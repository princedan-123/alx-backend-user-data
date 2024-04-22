#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import NoResultFound, InvalidRequestError

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

    def add_user(self, email: str, hashed_password: str):
        """A method that adds a new row in the database"""
        row = User(email=email, hashed_password=hashed_password)
        session = self._session
        session.add(row)
        session.commit()
        return row

    def find_user_by(self, **kwargs):
        """
        A method that takes arbitrary keyword argument,
        with which it filters a query.
        """
        session = self._session
        keys = list(kwargs.keys())
        key = keys[0]
        values = list(kwargs.values())
        value = values[0]
        try:
            query = session.query(User).filter_by(**kwargs).first()
            if not query:
                raise NoResultFound()
        except AttributeError as error:
            raise InvalidRequestError()
        return query
