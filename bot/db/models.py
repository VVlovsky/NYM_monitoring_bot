# -*- coding: utf-8 -*-

from sqlalchemy import Column, String, Integer, Float, Boolean
from sqlalchemy.ext.declarative import declarative_base


def wrapped_models(Base: declarative_base):
    class ValidatorData(Base):
        __tablename__ = 'validator_static'

        id = Column(Integer, primary_key=True, autoincrement=True)
        rank = Column(Integer)
        total_amount = Column(String)
        delegation_denom = Column(String)
        delegation_amount = Column(String)
        bond_denom = Column(String)
        bond_amount = Column(String)
        owner = Column(String, unique=True)
        host = Column(String)
        layer = Column(String)
        location = Column(String)
        sphinx_key = Column(String)
        identity_key = Column(String)
        version = Column(String)
        mix_port = Column(String)
        verloc_port = Column(String)
        http_api_port = Column(String)

    class Leaderboard(Base):
        __tablename__ = 'leaderboard'

        id = Column(Integer, primary_key=True, autoincrement=True)
        text = Column(String)

    class ValidatorByUserId(Base):
        __tablename__ = 'validator_by_user_id'

        id = Column(Integer, primary_key=True, autoincrement=True)
        user_id = Column(String, unique=True)
        identity_key = Column(String, unique=True)

    return ValidatorData, Leaderboard, ValidatorByUserId
