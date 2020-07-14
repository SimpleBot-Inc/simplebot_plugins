# -*- coding: utf-8 -*-
from deltabot.hookspec import deltabot_hookimpl
# typing
from deltabot import DeltaBot
from deltabot.commands import IncomingCommand
# ======


version = '1.0.0'


@deltabot_hookimpl
def deltabot_init(bot: DeltaBot) -> None:
    bot.commands.register(name="/echo", func=cmd_echo)


def cmd_echo(cmd: IncomingCommand) -> str:
    """Echoes back received text.

    To use it you can simply send a message starting with
    the command '/echo'. Example: `/echo hello world`
    """
    return cmd.payload or 'echo'