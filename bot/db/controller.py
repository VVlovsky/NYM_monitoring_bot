# -*- coding: utf-8 -*-

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base

from .config import config
from .models import wrapped_models as wrapped_models_func
from .methods import wrapped_methods


async def init_async_db():
    engine = create_async_engine(r'sqlite+aiosqlite:///./test.db', future=True, echo=True)

    session = sessionmaker(
        engine, expire_on_commit=False, class_=AsyncSession
    )

    base = declarative_base()
    config.set_base(base)
    wrapped_models = await wrapped_models_func(base)

    async with engine.begin() as conn:
        await conn.run_sync(base.metadata.drop_all)
        await conn.run_sync(base.metadata.create_all)

    validator_static, leaderboard, validator_by_user_id = await wrapped_methods(wrapped_models, session)
    return validator_static, leaderboard, validator_by_user_id
