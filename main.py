# -*- coding: utf-8 -*-

import asyncio

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from bot.db.controller import init_async_db
from bot.db.config import Config, config
from bot.handlers.commands.cmd_start import register_start_cmd
from bot.handlers.callbacks.cb_leaderboard import register_leaderboard_callbacks
from bot.handlers.callbacks.cb_validator_info import register_validator_callback
from bot.db.processing import update_data

from config import cfg

bot = Bot(token=cfg.bot_token, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot=bot, storage=MemoryStorage())


async def main():
    validator_static, leaderboard, validator_by_user_id = await init_async_db()
    config.set_tables(validator_static, leaderboard, validator_by_user_id)
    register_start_cmd(dp)
    register_leaderboard_callbacks(dp)
    register_validator_callback(dp)

    await asyncio.gather(dp.start_polling(dp), update_data(validator_static, leaderboard))


asyncio.run(main())
