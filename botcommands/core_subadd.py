import asyncio
import time

from botcore import hook
import botcore
from botcommands.core_initdb import findtable
from botcommands.core_initdb import subchans
from sqlalchemy.exc import IntegrityError

from sqlalchemy import select

@hook.irc_raw("352")
def who_summon(conn, irc_raw=None):
    print(chan_to_drop)
    irc_parsed = irc_raw.split(" ")
    channel = str(irc_parsed[3])
    if channel == chan_to_drop:
        user = str(irc_parsed[7])
        if user != bot_nick:
            print(user)
            conn.kick_user(chan_to_drop, user)


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

def createsubchan(chan, conn, nick, subchan_name, multi):
    subchan_real = "{}{}{}{}".format(sub_prefix, chan[1:], sub_separator, subchan_name)
    conn.join(subchan_real)
    if multi == True:
        print(nick)
        for x in nick:
            conn.invite(x, subchan_real)
    elif multi == False:
        conn.invite(nick, subchan_real)


@hook.command
def subadd(text, conn, db, chan, nick, notice, message):
    if text != '' and " " in text and chan != nick:
        args = text.split(" ")
        try:
            subchan_name = args[0]
        except IndexError:
            return "Please specify the name for your sub-channel."
        message("Creating sub-channel '{}' for you...".format(subchan_name))
        nick_list = args[1:]
        nick_list.append(nick)
        multi = True
        createsubchan(chan, conn, nick_list, subchan_name, multi)

    elif text !='' and chan != nick:
        subchan_name = text
        multi = False
        createsubchan(chan, conn, nick, subchan_name, multi)
    else:
        return "Command is not complete. Please read the manual."

@hook.command
def subdrop(chan, conn):
    global chan_to_drop
    global bot_nick
    chan_to_drop = chan
    bot_nick = conn.nick
    conn.cmd("WHO", chan_to_drop)
    time.sleep(5)
    conn.part(chan_to_drop)