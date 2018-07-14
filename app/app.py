"""
tranvia-zaragoza
Copyright (C) 2018  Púlsar

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


from . import logging
logger = logging.getLogger(__name__)

from app import app_config
from app import stops

from app import message_handler
from app import command_handler

from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters


def run():
    updater = Updater(token=app_config['token'])
    dispatcher = updater.dispatcher

    # Command handlers
    start_handler = CommandHandler('start', command_handler.start)
    help_handler = CommandHandler('help', command_handler.help)
    about_handler = CommandHandler('about', command_handler.about)

    # Message handlers
    plain_text_handler = MessageHandler(Filters.text, message_handler.message)

    # Adding the handlers
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(help_handler)
    dispatcher.add_handler(about_handler)

    dispatcher.add_handler(plain_text_handler)

    # Starting the bot
    updater.start_polling()

    logger.info("Bot running...")
