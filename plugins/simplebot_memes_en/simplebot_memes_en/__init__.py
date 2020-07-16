# -*- coding: utf-8 -*-
import tempfile

from deltabot.hookspec import deltabot_hookimpl
import bs4
import requests
# typing
from deltabot import DeltaBot
from deltabot.commands import IncomingCommand
# ======


version = '1.0.0'
ua = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:60.0) Gecko/20100101'
ua += ' Firefox/60.0'
HEADERS = {
    'user-agent': ua
}
dbot: DeltaBot


# ======== Hooks ===============

@deltabot_hookimpl
def deltabot_init(bot: DeltaBot) -> None:
    global dbot
    dbot = bot
    getdefault('max_meme_size', 1024*200)

    bot.commands.register(name='/memecenter', func=cmd_memecenter)


# ======== Commands ===============


def cmd_memecenter(cmd: IncomingCommand) -> tuple:
    """Get a random memes from www.memecenter.com
    """
    def _get_image():
        url = 'https://www.memecenter.com'
        with requests.get(url, headers=HEADERS) as r:
            r.raise_for_status()
            soup = bs4.BeautifulSoup(r.text, 'html.parser')
        url = soup.find('a', class_='random')['href']
        with requests.get(url, headers=HEADERS) as r:
            r.raise_for_status()
            soup = bs4.BeautifulSoup(r.text, 'html.parser')
        img_desc = soup.title.get_text().strip()
        img_url = soup.find('div', id='fdc_download').a['href']
        return (img_desc, img_url)

    return get_meme(_get_image)


# ======== Utilities ===============

def get_meme(get_image) -> tuple:
    img = b''
    max_meme_size = int(getdefault('max_meme_size'))
    for i in range(10):
        img_desc, img_url = get_image()
        with requests.get(img_url, headers=HEADERS) as r:
            r.raise_for_status()
            if len(r.content) <= max_meme_size:
                img = r.content
                break
            if not img or len(img) > len(r.content):
                img = r.content

    ext = img_url.split('/')[-1].split('?')[0].split('#')[0].split('.')[-1]
    fd, path = tempfile.mkstemp(prefix='meme-', suffix='.'+ext)
    with open(fd, 'wb') as f:
        f.write(img)

    text = '{}\n\n{}'.format(img_desc, img_url)
    return (text, path)


def getdefault(key: str, value=None) -> str:
    val = dbot.get(key, scope=__name__)
    if val is None and value is not None:
        dbot.set(key, value, scope=__name__)
        val = value
    return val
