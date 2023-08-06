
import asyncio
import os
from telethon import TelegramClient
from telethon.sessions import StringSession
from Extre.connections import client_connection, redis_connection
from Extre import *
from Extre import *
from Extre.utils import extremepro_cmd, amanpandey_cmd, load_module, humanbytes, register, command, start_assistant, errors_handler, progress, human_to_bytes, time_formatter, is_admin
from Extre.config import Config
from Extre.var import Var
from Extre.variables import Var
from Extre import CMD_LIST, CMD_HELP, CMD_HELP_BOT, BRAIN_CHECKER, INT_PLUG, LOAD_PLUG, COUNT_MSG, USERS, COUNT_PM, LASTMSG, CMD_HELP, ISAFK, AFKREASON, SUDO_LIST

async def bash(cmd):
    process = await asyncio.create_subprocess_shell(
        cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    stdout, stderr = await process.communicate()
    err = stderr.decode().strip()
    out = stdout.decode().strip()
    return out, err


def time_formatter(milliseconds: int) -> str:
    """Inputs time in milliseconds, to get beautified time,
    as string"""
    seconds, milliseconds = divmod(int(milliseconds), 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    tmp = (
        ((str(days) + " day(s), ") if days else "")
        + ((str(hours) + " hour(s), ") if hours else "")
        + ((str(minutes) + " minute(s), ") if minutes else "")
        + ((str(seconds) + " second(s), ") if seconds else "")
        + ((str(milliseconds) + " millisecond(s), ") if milliseconds else "")
    )
    return tmp[:-2]