import asyncio
import time

from botcore import hook
import botcore
from botcommands.core_initdb import findtable
from botcommands.core_initdb import subchans
from sqlalchemy.exc import IntegrityError

from sqlalchemy import select

@hook.on_start()
def load_api(bot):
    global sub_prefix
    global sub_separator

    sub_prefix = bot.config.get("modular", {}).get("channel_prefix")
    sub_separator = bot.config.get("modular", {}).get("channel_separator")

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

def createsubchan(chan, conn, nick, subchan_name):
    subchan_real = "{}{}{}{}".format(sub_prefix, chan[1:], sub_separator, subchan_name)
    conn.join(subchan_real)
    conn.invite(nick, subchan_real)


@hook.command
def subadd(text, conn, db, chan, nick, notice, message):
    if text != '' and " " in text and chan != nick:
        args = text.split(" ")
        try:
            subchan_name = args[0]
            createsubchan(chan, conn, nick, subchan_name)
        except:
            return "Please specify the name for your sub-channel."
    elif text !='' and chan != nick:
        subchan_name = text
        createsubchan(chan, conn, nick, subchan_name)
    else:
        return "Command is not complete. Please read the manual."

