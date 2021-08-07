# -*- coding: utf-8 -*-

from dataclasses import dataclass


@dataclass(frozen=True)
class Message:
    welcome: str = 'PUNKS NOT DEAD!'

    ask_address: str = 'Enter mixnode address\nto get information about it'

    validator_statistic: str = (
        'Mixnode information\nreceived successfully\n\n'
        '┌ Rank: %s\n'
        '├─── Identity Key <a href="https://nodes.guru/nym/mixnodecheck?address=%s"><b>%s</b></a>\n'
        '├─── Sphinx Key: %s\n'
        '├─── Owner: %s\n'
        '├─── Layer: %s\n'
        '├─── Location: %s\n'
        '├─── Version: %s\n'
        '├─── Host: %s\n'
        '├─── Total Amount: %s\n'
        '├───── Bond: %s\n'
        '└───── Delegated: %s\n'
    )

    validator_not_found: str = "Sorry, we can't find\na validator with specified address"

    leaderboard_title: str = 'Leaderboard. Page %s/%s\n'

    leaderboard_note: str = (
        '\n┌ Rank: %s\n'
        '├─── Identity Key <a href="https://nodes.guru/nym/mixnodecheck?address=%s"><b>%s</b></a>\n'
        '├─── Sphinx Key: %s\n'
        '├─── Owner: %s\n'
        '├─── Version: %s\n'
        '├─── Host: %s\n'
        '├─── Total Amount: %s\n'
        '├───── Bond: %s\n'
        '└───── Delegated: %s\n'
    )


message = Message
