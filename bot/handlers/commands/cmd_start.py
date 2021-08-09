# -*- coding: utf-8 -*-

from aiogram import Dispatcher
import pathlib

from bot.db.config import config
from ...message_templates import MessageTemplates
from ...keyboards import Keyboard


async def cmd_start(message):
    await message.answer_animation(
        animation=(open(f'{pathlib.Path(__file__).parent.resolve()}/../../../media/nym_welcome.mp4', 'rb')),
        width=848, height=848, duration=1)
    await message.answer(text=MessageTemplates.welcome % await config.get_validator_static().get_rows_count(),
                         reply_markup=Keyboard.main_menu(),
                         disable_web_page_preview=True)


def register_start_cmd(dp: Dispatcher):
    dp.register_message_handler(cmd_start, commands='start', state='*')
