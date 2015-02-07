__author__ = 'foxlet'

import asyncio
import time

from botcore import hook
import botcore

@hook.command
def chanlist(message):
    message("Test.")