.PHONY: all
all: echo friends groupmaster tictactoe translator webgrabber wikiquote xkcd admin shortcuts rss facebook mastodon avatar meme cartv cuba_weather xmpp chess reversi irc

.PHONY: echo
echo:
	echo y | pip uninstall simplebot_echo; pip install plugins/simplebot_echo

.PHONY: friends
friends:
	echo y | pip uninstall simplebot_friends; pip install plugins/simplebot_friends

.PHONY: groupmaster
groupmaster:
	echo y | pip uninstall simplebot_groupmaster; pip install plugins/simplebot_groupmaster

.PHONY: tictactoe
tictactoe:
	echo y | pip uninstall simplebot_tictactoe; pip install plugins/simplebot_tictactoe

.PHONY: translator
translator:
	echo y | pip uninstall simplebot_translator; pip install plugins/simplebot_translator

.PHONY: webgrabber
webgrabber:
	echo y | pip uninstall simplebot_webgrabber; pip install plugins/simplebot_webgrabber

.PHONY: wikiquote
wikiquote:
	echo y | pip uninstall simplebot_wikiquote; pip install plugins/simplebot_wikiquote

.PHONY: xkcd
xkcd:
	echo y | pip uninstall simplebot_xkcd; pip install plugins/simplebot_xkcd

.PHONY: admin
admin:
	echo y | pip uninstall simplebot_admin; pip install plugins/simplebot_admin

.PHONY: shortcuts
shortcuts:
	echo y | pip uninstall simplebot_shortcuts; pip install plugins/simplebot_shortcuts

.PHONY: rss
rss:
	echo y | pip uninstall simplebot_rss; pip install plugins/simplebot_rss

.PHONY: facebook
facebook:
	echo y | pip uninstall simplebot_facebook; pip install plugins/simplebot_facebook

.PHONY: mastodon
mastodon:
	echo y | pip uninstall simplebot_mastodon; pip install plugins/simplebot_mastodon

.PHONY: avatar
avatar:
	echo y | pip uninstall simplebot_avatar; pip install plugins/simplebot_avatar

.PHONY: meme
meme:
	echo y | pip uninstall simplebot_meme; pip install plugins/simplebot_meme

.PHONY: cartv
cartv:
	echo y | pip uninstall simplebot_cartv; pip install plugins/simplebot_cartv

.PHONY: cuba_weather
cuba_weather:
	echo y | pip uninstall simplebot_cubaweather; pip install plugins/simplebot_cubaweather

.PHONY: xmpp
xmpp:
	echo y | pip uninstall simplebot_xmpp; pip install plugins/simplebot_xmpp

.PHONY: chess
chess:
	echo y | pip uninstall simplebot_chess; pip install plugins/simplebot_chess

.PHONY: reversi
reversi:
	echo y | pip uninstall simplebot_reversi; pip install plugins/simplebot_reversi

.PHONY: irc
irc:
	echo y | pip uninstall simplebot_irc; pip install plugins/simplebot_irc
