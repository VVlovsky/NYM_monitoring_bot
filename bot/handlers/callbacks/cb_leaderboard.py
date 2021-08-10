# -*- coding: utf-8 -*-

from asyncio import gather
from aiogram import Dispatcher
from aiogram.types import CallbackQuery
from aiogram.dispatcher import FSMContext
from ..states import Page
from ...db.config import config
from ...message_templates import MessageTemplates, message
from ...keyboards import Keyboard


async def leaderboard_page(call: CallbackQuery, state: FSMContext):
    await state.reset_state()
    lb = config.get_leaderboard()
    last_note_id = await lb.get_rows_count()
    obj = await lb.get_row_by_id(note_id=1)

    try:
        note_text = obj.text
        text_response = 'Leaderboard. Page %s/%s\n' % (1, last_note_id) + note_text
    except Exception as e:
        print(f'WARN: {e}')
        text_response = message.db_problem % 1

    try:
        await gather(
            call.message.edit_text(
                text=text_response, reply_markup=Keyboard.switch_page(1, last_note_id), disable_web_page_preview=True
            ),
            Page.note_id.set()
        )
    except Exception as e:
        print(f'WARN: {e}')


async def turn_leaderboard_page(call: CallbackQuery, state: FSMContext):
    await call.answer()
    lb = config.get_leaderboard()
    current_note_id = (await state.get_data()).get('page', 1)
    last_note_id = await lb.get_rows_count()

    if call.data == 'next':

        if len(await state.get_data()) == 0:
            current_note_id = 2

            obj = await lb.get_row_by_id(note_id=current_note_id)
            try:
                note_text = obj.text
                text_response = 'Leaderboard. Page %s/%s\n' % (current_note_id, last_note_id) + note_text
            except Exception as e:
                print(f'WARN: {e}')
                text_response = message.db_problem % current_note_id

            try:
                response = call.message.edit_text(
                    text=text_response, reply_markup=Keyboard.switch_page(current_note_id, last_note_id),
                    disable_web_page_preview=True
                )
                await gather(response, state.update_data(page=2))

            except Exception as e:
                print(f'WARN: {e}')


        else:
            current_note_id += 1

            obj = await lb.get_row_by_id(note_id=current_note_id)
            try:
                note_text = obj.text
                text_response = 'Leaderboard. Page %s/%s\n' % (current_note_id, last_note_id) + note_text
            except Exception as e:
                print(f'WARN: {e}')
                text_response = message.db_problem % current_note_id

            try:
                response = call.message.edit_text(
                    text=text_response, reply_markup=Keyboard.switch_page(current_note_id, last_note_id),
                    disable_web_page_preview=True
                )
                await gather(response, state.update_data(page=current_note_id))

            except Exception as e:
                print(f'WARN: {e}')


    elif call.data == 'back':
        current_note_id -= 1

        obj = await lb.get_row_by_id(note_id=current_note_id)
        try:
            note_text = obj.text
            text_response = 'Leaderboard. Page %s/%s\n' % (current_note_id, last_note_id) + note_text
        except Exception as e:
            print(f'WARN: {e}')
            text_response = message.db_problem % current_note_id

        try:
            response = call.message.edit_text(
                text=text_response, reply_markup=Keyboard.switch_page(current_note_id, last_note_id),
                disable_web_page_preview=True
            )
            await gather(response, state.update_data(page=current_note_id))

        except Exception as e:
            print(f'WARN: {e}')

    elif call.data == 'home':
        await call.answer()
        response = call.message.edit_text(
            text=MessageTemplates.welcome % await config.get_validator_static().get_rows_count(),
            reply_markup=Keyboard.main_menu(),
            disable_web_page_preview=True)

        await gather(response, state.finish())


def register_leaderboard_callbacks(dp: Dispatcher):
    dp.register_callback_query_handler(
        leaderboard_page, lambda CallbackQuery: CallbackQuery.data == 'leaderboard', state='*'
    )

    dp.register_callback_query_handler(turn_leaderboard_page,
                                       lambda CallbackQuery: CallbackQuery.data in ['next', 'back', 'home'], state='*')
