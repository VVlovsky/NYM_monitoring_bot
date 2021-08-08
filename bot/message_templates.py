# -*- coding: utf-8 -*-

from dataclasses import dataclass


@dataclass(frozen=True)
class MessageTemplates:
    welcome: str = 'Hello, thank you for using our bot.\n\n' \
                   'We would like to warn you that we have the access to all the messages that you send here,' \
                   ' so please do not send any sensitive information like private keys or mnemonics phrases.\n\n' \
                   'If you have any problems - tag @MadnessV in the <a href="https://t.me/nymchan"><b>NYM</b></a> or' \
                   ' <a href="https://t.me/NYM_Russian"><b>NYM Russian</b></a> chats 🙂\n' \
                   '\nCurrent number of mixnodes is %s'

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
        '│\n'
        '├─── <pre>Most Recent ipv4: %s</pre>\n'
        '├─── <pre>Most Recent ipv6: %s</pre>\n'
        '├─── <pre>Last Hour ipv4:   %s</pre>\n'
        '├─── <pre>Last Hour ipv6:   %s</pre>\n'
        '├─── <pre>Last Day ipv4:    %s</pre>\n'
        '├─── <pre>Last Day ipv6:    %s</pre>\n'
        '├─── <pre>Last Week ipv4:   %s</pre>\n'
        '├─── <pre>Last Week ipv6:   %s</pre>\n'
        '│\n'
        '<pre>├─── Total:       %s</pre>\n'
        '<pre>├───── Bond:      %s</pre>\n'
        '<pre>└───── Delegated: %s</pre>\n'

    )

    db_problem = str(
        'Leaderboard. Page %s/?\n'
        'Something goes wrong. ⚠️\n'
        'It looks like a problem with DB.\n'
        'Please wait a few minutes.\n'
        'If the problem reoccurs - please tag @MadnessV in the <a href="https://t.me/nymchan"><b>NYM</b></a> or' \
        ' <a href="https://t.me/NYM_Russian"><b>NYM Russian</b></a> chats 🙂\n'
    )

    validator_not_found: str = "Sorry, we can't find\na mixnode with specified address"

    leaderboard_title: str = 'Leaderboard. Page %s/%s\n'

    leaderboard_note: str = (
        '\n┌ Rank: %s\n'
        '├─── Identity Key <a href="https://nodes.guru/nym/mixnodecheck?address=%s"><b>%s</b></a>\n'
        '├─── Sphinx Key: %s\n'
        '├─── Owner: %s\n'
        '├─── Host: %s\n'
        '├─── Total Amount: %s\n'
        '├───── Bond: %s\n'
        '└───── Delegated: %s\n'
    )


message = MessageTemplates
