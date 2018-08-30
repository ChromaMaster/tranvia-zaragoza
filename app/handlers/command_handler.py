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

from app import logging
logger = logging.getLogger(__name__)


def start(bot, update):
    """ Function than it's executed when the command '/start' is received """
    logger.debug("Start command received")
    start_message = """
    Introduzca el nombre (o parte de el) de una parada para obtener el tiempo \
de llegada del próximo tranvía"""
    bot.send_message(chat_id=update.message.chat_id,
                     text="")


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
