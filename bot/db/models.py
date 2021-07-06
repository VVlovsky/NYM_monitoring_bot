# -*- coding: utf-8 -*-

from sqlalchemy import Column, String, Integer, Float, Boolean
from sqlalchemy.ext.declarative import declarative_base


def wrapped_models(Base: declarative_base):
    class ValidatorData(Base):
        __tablename__ = 'validator_static'

        id = Column(Integer, primary_key=True, autoincrement=True)
        # is_active = Column(Boolean)
        # address = Column(String, unique=True)

        # score = Column(Integer)
        # daily_score_changes = Column(Integer)
        # weekly_score_changes = Column(Integer)
        # monthly_score_changes = Column(Integer)

        # response_time = Column(Float)
        # average_response_time = Column(Float)
        #
        # responses = Column(Integer)
        # daily_responses_changes = Column(Integer)
        # weekly_responses_changes = Column(Integer)
        # monthly_responses_changes = Column(Integer)
        #
        # current_stake = Column(Float)
        # daily_stake_changes = Column(Float)
        # weekly_stake_changes = Column(Float)
        # monthly_stake_changes = Column(Float)
        rank = Column(Integer)
        denom = Column(String)
        amount = Column(String)
        owner = Column(String, unique=True)
        host = Column(String)
        layer = Column(Integer)
        location = Column(String)
        sphinx_key = Column(String)
        identity_key = Column(String)
        version = Column(String)

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
