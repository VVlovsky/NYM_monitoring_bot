# -*- coding: utf-8 -*-

from asyncio import gather
from typing import Dict

from aiogram import Dispatcher
from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher import FSMContext

from ..states import SetValidatorAddress

from ...keyboards import Keyboard
from ...message_templates import message
from ...db.config import config
from ...network_methods import request_get


async def check_validator(call: CallbackQuery, state: FSMContext):
    validator_by_user_id = config.get_validator_by_user_id()
    if call.data == 'home':
        await gather(
            state.finish(),
            call.message.edit_text(text=message.welcome % await config.get_validator_static().get_rows_count(),
                                   reply_markup=Keyboard.main_menu(),
                                   disable_web_page_preview=True)
        )
    else:
        try:
            user_id = call.from_user['id']
        except Exception as e:
            print(f'WARN: {e}')
            user_id = None
        row_with_address = await validator_by_user_id.get_row_by_criteria({'user_id': user_id})

        if call.data == 'repeat' and row_with_address:
            row_with_address = None
            await validator_by_user_id.delete_row_by_criteria({'user_id': user_id})

        if not row_with_address:
            call_data = await call.message.edit_text(
                text=message.ask_address, reply_markup=Keyboard.home()
            )
            await gather(
                SetValidatorAddress.address.set(), state.update_data(message_data=call_data)
            )

        else:
            await show_validator_stats(call, state)


async def generate_response(address, data, call_):
    short_address = data.identity_key[0:4] + '...' + data.identity_key[-5:-1]
    short_sphinx = data.sphinx_key[0:4] + '...' + data.sphinx_key[-5:-1]
    short_owner = data.owner[0:4] + '...' + data.owner[-5:-1]
    punks = str(int(data.total_amount) // 1000000) + '.' + str(int(data.total_amount) % 1000000)[:2] + ' PUNK'
    punks_bond = str(int(data.bond_amount) // 1000000) + '.' + str(int(data.bond_amount) % 1000000)[:2] + ' PUNK'
    punks_delegated = str(int(data.delegation_amount) // 1000000) + '.' + str(
        int(data.delegation_amount) % 1000000)[:2] + ' PUNK'

    ip_data_report = await get_report_history(data.identity_key, 'report')
    most_recent_ipv4 = '✅' if ip_data_report.get('most_recent_ipv4', '0') else '❌'
    most_recent_ipv6 = '✅' if ip_data_report.get('most_recent_ipv6', '0') else '❌'
    last_hour_ipv4 = int(ip_data_report.get('last_hour_ipv4', '0'))
    last_hour_ipv6 = int(ip_data_report.get('last_hour_ipv6', '0'))
    last_day_ipv4 = int(ip_data_report.get('last_day_ipv4', '0'))
    last_day_ipv6 = int(ip_data_report.get('last_day_ipv6', '0'))

    ip_data_history = await get_report_history(data.identity_key, 'history')
    sum_uptime_ipv4 = 0
    sum_uptime_ipv6 = 0
    ip_data_history = ip_data_history.get('history', [])
    for day in ip_data_history:
        sum_uptime_ipv4 += int(day.get('ipv4_uptime', '0'))
        sum_uptime_ipv6 += int(day.get('ipv6_uptime', '0'))

    last_week_ipv4 = int((sum_uptime_ipv4 + int(last_day_ipv4)) / (len(ip_data_history) + 1))
    last_week_ipv6 = int((sum_uptime_ipv6 + int(last_day_ipv6)) / (len(ip_data_history) + 1))

    last_hour_ipv4 = f'✅ 100%' if last_hour_ipv4 == 100 else f'⚠️ {last_hour_ipv4}%'
    last_hour_ipv6 = f'✅ 100%' if last_hour_ipv6 == 100 else f'⚠️ {last_hour_ipv6}%'
    last_day_ipv4 = f'✅ 100%' if last_day_ipv4 == 100 else f'⚠️ {last_day_ipv4}%'
    last_day_ipv6 = f'✅ 100%' if last_day_ipv6 == 100 else f'⚠️ {last_day_ipv6}%'
    last_week_ipv4 = f'✅ 100%' if last_week_ipv4 == 100 else f'⚠️ {last_week_ipv4}%'
    last_week_ipv6 = f'✅ 100%' if last_week_ipv6 == 100 else f'⚠️ {last_week_ipv6}%'

    response = call_.edit_text(
        text=message.validator_statistic % (data.rank,
                                            data.identity_key, short_address, short_sphinx, short_owner, data.layer,
                                            data.location, data.version, data.host,
                                            most_recent_ipv4, most_recent_ipv6, last_hour_ipv4, last_hour_ipv6,
                                            last_day_ipv4, last_day_ipv6, last_week_ipv4, last_week_ipv6,
                                            punks, punks_bond, punks_delegated),
        reply_markup=Keyboard.repeat(), disable_web_page_preview=True
    )

    return response


async def get_report_history(id_key: str, endpoint: str) -> Dict:
    url = f'https://testnet-milhon-validator1.nymtech.net/api/v1/status/mixnode/{id_key}/{endpoint}'
    data = await request_get(url, return_json=True)
    return data


async def show_new_validator(call: Message or CallbackQuery, state: FSMContext):
    validator_static = config.get_validator_static()
    validator_by_user_id = config.get_validator_by_user_id()
    if isinstance(call, CallbackQuery):
        response = call.message.edit_text(text=message.welcome % await config.get_validator_static().get_rows_count(),
                                          reply_markup=Keyboard.main_menu(),
                                          disable_web_page_preview=True)

        await gather(response, state.finish())

    else:
        call_: CallbackQuery.message = (await state.get_data()).get('message_data')

        address = call.text
        stats = await validator_static.get_row_by_criteria({'identity_key': address})

        if not stats:
            response = call_.edit_text(text=message.validator_not_found, reply_markup=Keyboard.repeat())

            await gather(call.delete(), response)

        else:
            response = await generate_response(address, stats, call_)
            await validator_by_user_id.paste_row({
                'user_id': call_['chat']['id'], 'identity_key': address
            })
            await validator_by_user_id.commit()

            await gather(call.delete(), response)


async def show_validator_stats(call: Message or CallbackQuery, state: FSMContext):
    validator_static = config.get_validator_static()
    validator_by_user_id = config.get_validator_by_user_id()
    call_: CallbackQuery.message = (await state.get_data()).get('message_data')
    user_id = call.from_user['id']
    row_with_address = await validator_by_user_id.get_row_by_criteria({'user_id': user_id})
    if not row_with_address:
        await show_new_validator(call, state)
    else:
        address = row_with_address.identity_key
        stats = await validator_static.get_row_by_criteria({'identity_key': address})
        if call_:
            response = await generate_response(address, stats, call_)
            await gather(call.delete(), response)
        else:
            response = await generate_response(address, stats, call.message)
            await gather(response)
    await state.finish()


def register_validator_callback(dp: Dispatcher):
    dp.register_callback_query_handler(
        check_validator, lambda CallbackQuery: CallbackQuery.data in [
            'find_validator', 'repeat', 'home'
        ], state='*'
    )

    dp.register_message_handler(show_validator_stats, state=SetValidatorAddress)
    dp.register_callback_query_handler(show_validator_stats, state=SetValidatorAddress)
