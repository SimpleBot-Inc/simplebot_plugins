# -*- coding: utf-8 -*-
from datetime import datetime
import html

from deltabot.hookspec import deltabot_hookimpl
import requests
import pytz
# typing
from deltabot import DeltaBot
from deltabot.commands import IncomingCommand
# ===


version = '1.0.0'
url = 'http://www.tvcubana.icrt.cu/cartv/cartv-core/app.php'
url += '?action=dia&canal={0}&fecha={1}'
tv_emoji, cal_emoji, aster_emoji = '📺', '📆', '✳'
channels = ['Cubavision', 'Telerebelde', 'Educativo', 'Educativo 2',
            'Multivision', 'Canal Clave', 'Caribe', 'Habana']


@deltabot_hookimpl
def deltabot_init(bot: DeltaBot) -> None:
    bot.commands.register(name="/cartv", func=cmd_cartv)


def cmd_cartv(cmd: IncomingCommand) -> str:
    """Muestra la cartelera de la TV cubana.

    Muestra la cartelera para el canal dado o la cartelera para todos
    los canales si no se le pasa ningún canal.
    Ejemplo: `/cartv Cubavision`
    """
    eastern = pytz.timezone("US/Eastern")
    today = datetime.now(eastern).strftime('%d-%m-%Y')

    if cmd.payload:
        if cmd.payload not in channels:
            return 'El canal puede ser:\n{}'.format('\n'.join(channels))
        chans = [cmd.payload]
    else:
        chans = channels

    text = ''
    for chan in chans:
        with requests.get(url.format(chan, today)) as req:
            req.raise_for_status()
            text += format_channel(req.text)
        text += '\n\n'
    return text


def format_channel(text: str) -> str:
    lines = html.unescape(text).splitlines()
    lines = [ln.strip().replace('\t', ' ') for ln in lines]

    text = '{} {}\n'.format(tv_emoji, lines[0])
    text += '{} {}\n'.format(cal_emoji, lines[1])

    for line in lines[2:]:
        text += '{} {}\n'.format(aster_emoji, line)

    return text