import asyncio
import time

from botcore.util import botvars
from botcore import hook
import botcore
from sqlalchemy import select
from sqlalchemy import Table, Column, String, PrimaryKeyConstraint
from sqlalchemy.types import REAL
from sqlalchemy.exc import IntegrityError


findtable = Table(
    'channels_under_sub',
    botvars.metadata,
    Column('chan', String),
    Column('add_nick', String),
    Column('conn', String),
    Column('time', REAL),
    Column('deleted', String, default=0),
    PrimaryKeyConstraint('chan', 'add_nick', 'conn')
)

subchans = Table(
    'subchans',
    botvars.metadata,
    Column('chan', String),
    Column('add_nick', String),
    Column('subchan', String),
    Column('conn', String),
    Column('time', REAL),
    Column('topic', String),
    Column('deleted', String, default=0),
    PrimaryKeyConstraint('subchan', 'add_nick', 'conn')
)