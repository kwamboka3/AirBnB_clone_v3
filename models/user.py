#!/usr/bin/python3
""" holds class User"""
import models
from models.base_model import BaseModel, Base
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship, backref
from hashlib import md5


class User(BaseModel, Base):
    """Representation of a user """
    if models.storage_t == 'db':
        __tablename__ = 'users'
        email = Column(String(128), nullable=False)
        password = Column(String(128), nullable=False)
        first_name = Column(String(128), nullable=True)
        last_name = Column(String(128), nullable=True)
        places = relationship(
            "Place",
            cascade="all,delete",
            backref=backref("user"),
            passive_deletes=True,
            single_parent=True)
        reviews = relationship(
            "Review",
            cascade="all,delete",
            backref=backref("user"),
            passive_deletes=True,
            single_parent=True)
    else:
        email = ""
        password = ""
        first_name = ""
        last_name = ""

    def __init__(self, *args, **kwargs):
        """initializes user"""
        super().__init__(*args, **kwargs)

    def __setattr__(self, att_name, value):
        """set encrypted password"""
        if att_name == "password":
            value = md5(value.encode()).hexdigest()
        super().__setattr__(att_name, value)
