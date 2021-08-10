# -*- coding: utf-8 -*-
import asyncio
import itertools
from ..network_methods import request_get
from ..message_templates import message
from config import cfg


def unpack(parent_key, parent_value):
    try:
        if isinstance(parent_value, list):
            items = parent_value[0].items()
        else:
            items = parent_value.items()

    except AttributeError:
        yield (parent_key, parent_value)

    else:
        for key, value in items:
            yield (key, value)


async def update_validator_table(validator_static, leaderboard):
    data = await request_get(cfg.api_validator_data, return_json=True)

    for data_dict in data:
        data_dict['total_delegation']['delegation_denom'] = data_dict['total_delegation'].pop('denom')
        data_dict['total_delegation']['delegation_amount'] = data_dict['total_delegation'].pop('amount')
        data_dict['bond_amount']['bond_denom'] = data_dict['bond_amount'].pop('denom')
        data_dict['bond_amount']['bond_amount'] = data_dict['bond_amount'].pop('amount')
        data_dict['total_amount'] = int(data_dict['bond_amount']['bond_amount']) + int(
            data_dict['total_delegation']['delegation_amount'])

    for data_dict in sorted(data, key=lambda k: int(k['total_amount']), reverse=True):

        data_dict = dict(itertools.chain.from_iterable(itertools.starmap(unpack, data_dict.items())))
        filter_by_address = {'owner': data_dict['owner']}
        get_validator_data = await validator_static.get_row_by_criteria(criteria=filter_by_address)

        if get_validator_data:
            data_dict.pop('owner')
            await validator_static.upgrade_row_by_criteria(data_dict, criteria=filter_by_address)
        else:
            await validator_static.paste_row(data_dict)

    await validator_static.commit()
    await update_leaderboard_table(leaderboard=leaderboard, validator_static=validator_static)


async def update_leaderboard_table(leaderboard, validator_static):

    counter = 0
    note = ''
    all_rows = await validator_static.get_all_rows()
    if all_rows is None:
        return
    for data in sorted(all_rows, key=lambda k: int(k.total_amount) if k.total_amount else 0, reverse=True):

        if not data.identity_key:
            continue

        counter += 1

        short_address = data.identity_key[0:4] + '...' + data.identity_key[-5:]
        short_sphinx = data.sphinx_key[0:4] + '...' + data.sphinx_key[-5:-1]
        short_owner = data.owner[0:4] + '...' + data.owner[-5:-1]
        punks = str(int(data.total_amount) // 1000000) + '.' + str(int(data.total_amount) % 1000000)[:2] + ' PUNK'
        punks_bond = str(int(data.bond_amount) // 1000000) + '.' + str(int(data.bond_amount) % 1000000)[:2] + ' PUNK'
        punks_delegated = str(int(data.delegation_amount) // 1000000) + '.' + str(
            int(data.delegation_amount) % 1000000)[:2] + ' PUNK'

        await validator_static.upgrade_row_by_criteria({'rank': counter}, criteria={'owner': data.owner})
        note += message.leaderboard_note % (counter, data.host,
                                            data.identity_key, short_address, short_sphinx, short_owner,
                                            punks, punks_bond, punks_delegated)

        if counter % 3 == 0:
            leaderboard_page = await leaderboard.get_row_by_criteria(criteria={'id': counter // 3})
            if leaderboard_page:
                await leaderboard.upgrade_row_by_criteria({'text': note}, criteria={'id': counter // 3})
            else:
                await leaderboard.paste_row({'id': counter // 3, 'text': note})

            note = ''

    await leaderboard.commit()


async def update_data(validator_static, leaderboard):
    while True:
        await update_validator_table(leaderboard=leaderboard, validator_static=validator_static)
        await asyncio.sleep(120)
