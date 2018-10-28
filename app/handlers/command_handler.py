"""
tranvia-zaragoza
Copyright (C) 2018  ChromaMaster

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""


from app import fetch
from app import stops
from app import monitoring
from app import access_control

from app import logging
logger = logging.getLogger(__name__)

from telegram import ChatAction


def start(bot, update):
    """ Function than it's executed when the command '/start' is received """
    logger.debug("Start command received")
    start_message = """
    Bienvenido, para utilizar el bot introduzca el nombre de un parada (o parte de él) \
para ver el tiempo de llegada del próximo tranvía"""
    bot.send_message(chat_id=update.message.chat_id,
                     text=start_message)


def help(bot, update):
    """ Function that it's executed when the command '/ayuda' is received """
    logger.debug("Help command received")
    help_message = """
    Introduzca el nombre (o parte de el) de una parada para obtener el tiempo \
de llegada del próximo tranvía"""

    bot.send_message(chat_id=update.message.chat_id,
                     parse_mode='markdown', text=help_message)


def about(bot, update):
    """ Function that it's executed when the command '/sobre_nosotros' is received """
    logger.debug("About command received")
    about_message = """ Este bot ha sido creado por *Púlsar*, la Asociacíon de \
Software Libre de la Universidad de Zaragoza, bajo la licencia *GPLv3*.

Puedes contribuir a este proyectoen la siguiente dirección: \
https://gitlab.unizar.es/pulsar/tranvia-zaragoza"""

    bot.send_message(chat_id=update.message.chat_id,
                     parse_mode='markdown', text=about_message)


@access_control.only_whitelist
def stats(bot, update, args):
    """   """
    chat_id = update.message.chat_id

    # TODO: Complete this to allow getting stats between two dates.

    # if len(args) < 2:
    #     msg = "USAGE: "
    #     bot.send_message(chat_id=update.message.chat_id,
    #                      parse_mode='markdown', text=msg)
    # Get args
    # init_date = args[0]
    # end_date = args[1]

    init_date = ""
    end_date = ""

    # Sends feedback to user that the bot is actually do someting
    bot.send_chat_action(chat_id=chat_id, action=ChatAction.TYPING)

    # Get the current stats of usage
    global_stats = monitoring.get_global_stats(init_date, end_date)
    users_stats = monitoring.get_user_stats(init_date, end_date)
    stop_stats = monitoring.get_stop_stats(init_date, end_date)

    msg = "*GLOBAL STATS*\n" \
        "{}\n\n" \
        "*USER STATS*\n" \
        "{}\n\n" \
        "*STOP STATS*\n" \
        "{}\n".format(global_stats, users_stats, stop_stats)

    bot.send_message(chat_id=update.message.chat_id,
                     parse_mode='markdown', text=msg)
