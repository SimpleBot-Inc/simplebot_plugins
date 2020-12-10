import os
import pathlib
import random

from chatterbot import ChatBot
from chatterbot.conversation import Statement
from chatterbot.trainers import ChatterBotCorpusTrainer, ListTrainer
from deltabot import DeltaBot
from deltabot.bot import Replies
from deltabot.commands import IncomingCommand
from deltabot.hookspec import deltabot_hookimpl
from deltachat import Message


version = '1.0.0'
dbot: DeltaBot
cbot: ChatBot
list_trainer: ListTrainer
default_replies = ['😐', '😶', '🙄', '🤔', '😕', '🤯', '🤐', '🥴', '🧐']


# ======== Hooks ===============

@deltabot_hookimpl
def deltabot_init(bot: DeltaBot) -> None:
    global dbot
    dbot = bot
    getdefault('learn', '1')
    getdefault('reply_to_dash', '1')

    bot.filters.register(name=__name__, func=filter_messages)

    bot.commands.register(name="/chatter_learn", func=cmd_learn, admin=True)


@deltabot_hookimpl
def deltabot_start(bot: DeltaBot) -> None:
    global cbot, list_trainer

    locale = bot.get('locale') or 'en'
    corpus = dict(
        es='spanish',
        de='german',
        it='italian',
    )
    if locale == 'es':
        default_replies.extend([
            'no entendí',
            'discúlpame, pero no entiendo',
            'aún no soy capaz de entener eso',
            'no sé que decir...',
            'solo sé que no sé nada...',
            'los robots también nos emborrachamos',
            'voy a decir esto para no dejarte en visto',
            'ahí dice ta-ba-co',
            'eso habría que verlo compay',
        ])
    cbot = ChatBot(
        dbot.self_contact.addr,
        storage_adapter='chatterbot.storage.SQLStorageAdapter',
        database_uri=get_db_uri(bot),
        read_oly=getdefault('learn', '1') in ('0', 'no'),
        logic_adapters= [
            'chatterbot.logic.MathematicalEvaluation',
            {
                'import_path': 'chatterbot.logic.BestMatch',
                'default_response': default_replies,
                'maximum_similarity_threshold': 0.9,
            }
        ],
    )
    list_trainer = ListTrainer(cbot)
    trainer = ChatterBotCorpusTrainer(cbot)
    trainer.train('chatterbot.corpus.' + corpus.get(locale, 'english'))


# ======== Filters ===============

def filter_messages(message: Message, replies: Replies) -> None:
    """Natural language processing and learning.
    """
    if not message.text:
        return

    me = dbot.self_contact
    name = dbot.account.get_config('displayname')
    quote = message.quote

    reply_to_dash = getdefault('reply_to_dash', '1') not in ('0', 'no')
    resp = None
    if reply_to_dash and message.text.startswith('#') and len(message.text) > 1:
        resp = cbot.get_response(message.text[1:])
    elif not message.chat.is_group() or (
            quote and quote.get_sender_contact() == me):
        resp = cbot.get_response(message.text)
    elif me.addr in message.text or (name and name in message.text):
        resp = cbot.get_response(rmprefix(rmprefix(
            message.text, me.addr), name).strip(':,').strip())

    if resp:
        dbot.logger.debug('Confidence: %s | message: %s | reply: %s',
                          resp.confidence, resp.in_response_to, resp.text)
        if resp.confidence > 0.4:
            replies.add(text=resp.text)
        else:
            replies.add(text=random.choice(default_replies))

    if quote and quote.text:
        cbot.learn_response(
            Statement(text=message.text, in_response_to=quote.text))


# ======== Commands ===============

def cmd_learn(command: IncomingCommand, replies: Replies) -> None:
    """Learn new response.

    You must provide two lines, the first line is the question and the
    second line is the response.
    """
    list_trainer.train(command.payload.split('\n', maxsplit=1))
    replies.add(text='✔️Learned.')


# ======== Utilities ===============

def rmprefix(text: str, prefix: str) -> str:
    return text[text.startswith(prefix) and len(prefix):]


def getdefault(key: str, value: str = None) -> str:
    val = dbot.get(key, scope=__name__)
    if val is None and value is not None:
        dbot.set(key, value, scope=__name__)
        val = value
    return val


def get_db_uri(bot) -> str:
    path = os.path.join(os.path.dirname(bot.account.db_path), __name__)
    if not os.path.exists(path):
        os.makedirs(path)
    path = os.path.join(path, 'db.sqlite3')
    return 'sqlite:///' + rmprefix(pathlib.Path(path).as_uri(), 'file://')
