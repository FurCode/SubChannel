import asyncio
import time

from botcore import hook
import botcore
from botcommands.core_initdb import findtable
from sqlalchemy.exc import IntegrityError

from sqlalchemy import select

def checkforlisting(db, chan):
    count_query = select([findtable]) \
        .where(findtable.c.deleted != 1) \
        .where(findtable.c.chan == chan.lower()) \
        .count()
    count = db.execute(count_query).fetchall()[0][0]

    if count == 0:
        return False
    else:
        return True

@hook.command
def sublist(text, db, chan, nick, notice, message):

    if " " in text:
        args = text.split(" ")
        chan = args[0]
    elif text is not None and chan == nick:
        chan = text

    if chan[:1] != '#':
        notice('Please specify a channel.', nick)
    elif checkforlisting(db, chan) is not True:
        notice('The channel {} has no subchannels.'.format(chan), nick)
    else:
        notice('Sub-channel listing for {}'.format(chan), nick)