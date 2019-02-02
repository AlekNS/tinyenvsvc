# -*- coding: utf-8 -*-
from .db import db


class User(db.Model):
    '''
    Default simple User model.
    '''
    __tablename__ = 'users'

    # pylint: disable=no-member
    id = db.Column(db.Integer(), primary_key=True)
    email = db.Column('email', db.Unicode(), nullable=False, unique=True)
    password = db.Column('password_hash', db.Unicode(), nullable=False)
