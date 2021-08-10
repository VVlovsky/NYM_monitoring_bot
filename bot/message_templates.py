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

    ask_address: str = 'Enter mixnode identity key / sphinx key /\nowner address to get information about it.'

    validator_statistic: str = (
        'Mixnode information\nreceived successfully\n\n'
        '<pre>┌ Rank: </pre>%s\n'
        '<pre>├──💻 Host:     </pre>%s\n'
        '<pre>├──🔑 Identity: </pre><a href="https://nodes.guru/nym/mixnodecheck?address=%s"><b>%s</b></a>\n'
        '<pre>├──🔐 Sphinx:   </pre>%s\n'
        '<pre>├──🧍 Owner:    </pre>%s\n'
        '<pre>├──⛓ Layer:    </pre>%s\n'
        '<pre>├──🌍 Location: </pre>%s\n'
        '<pre>├──🧩 Version:  </pre>%s\n'
        '<pre>│\n</pre>'
        '<pre>├─── Most Recent ipv4: </pre>%s\n'
        '<pre>├─── Most Recent ipv6: </pre>%s\n'
        '<pre>├─── Last Hour ipv4:   </pre>%s\n'
        '<pre>├─── Last Hour ipv6:   </pre>%s\n'
        '<pre>├─── Last Day ipv4:    </pre>%s\n'
        '<pre>├─── Last Day ipv6:    </pre>%s\n'
        '<pre>├─── Last Week ipv4:   </pre>%s\n'
        '<pre>├─── Last Week ipv6:   </pre>%s\n'
        '<pre>│\n</pre>'
        '<pre>└──💰 Total:        </pre>%s\n'
        '<pre>   ├──💵 Bond:      </pre>%s\n'
        '<pre>   └──💸 Delegated: </pre>%s\n'

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
        '<pre>\n┌ Rank: </pre>%s\n'
        '<pre>├──💻 Host:     </pre>%s\n'
        '<pre>├──🔑 Identity: </pre><a href="https://nodes.guru/nym/mixnodecheck?address=%s"><b>%s</b></a>\n'
        '<pre>├──🔐 Sphinx:   </pre>%s\n'
        '<pre>├──🧍 Owner:    </pre>%s\n'
        '<pre>└──💰 Total:        </pre>%s\n'
        '<pre>   ├──💵 Bond:      </pre>%s\n'
        '<pre>   └──💸 Delegated: </pre>%s\n'
    )


message = MessageTemplates
