# -*- coding: utf-8 -*-
import asyncio
import itertools
from asyncio import gather

from .controller import validator_static, leaderboard

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


async def update_validator_table():
    for data_dict in sorted(await request_get(cfg.api_validator_data, return_json=True),
                            key=lambda k: int(k['amount'][0]['amount']), reverse=True):
        data_dict = dict(itertools.chain.from_iterable(itertools.starmap(unpack, data_dict.items())))
        filter_by_address = {'identity_key': data_dict['identity_key']}

        get_validator_data = validator_static.get_row_by_criteria(criteria=filter_by_address)

        if get_validator_data:
            data_dict.pop('identity_key')
            validator_static.upgrade_row_by_criteria(data_dict, criteria=filter_by_address)
        else:
            validator_static.paste_row(data_dict)
            print(f'added_row: {data_dict}')

    validator_static.commit()


async def update_leaderboard_table():
    leaderboard.delete_all_rows()

    counter = 0
    note = ''
    for data in sorted(validator_static.get_all_rows(), key=lambda k: k.amount, reverse=True):
        counter += 1

        short_address = data.identity_key[0:4] + '...' + data.identity_key[-5:-1]
        short_sphinx = data.sphinx_key[0:4] + '...' + data.sphinx_key[-5:-1]
        short_owner = data.owner[0:4] + '...' + data.owner[-5:-1]
        hals = str(int(data.amount) // 1000000) + '.' + str(int(data.amount) % 1000000) + ' HAL'

        # if not data.rank:
        #     validator_static.upgrade_row_by_criteria({'rank': counter}, {'identity_key': data.identity_key})

        note += message.leaderboard_note % (counter,
                                            data.identity_key, short_address, short_sphinx, short_owner, data.layer,
                                            data.location, data.version,
                                            data.host, hals)

        print(note)

        if counter % 3 == 0:
            leaderboard.paste_row({'text': note})
            note = ''

    leaderboard.commit()


async def update_data():
    while True:
        await gather(update_validator_table(), update_leaderboard_table())
        await asyncio.sleep(120)
