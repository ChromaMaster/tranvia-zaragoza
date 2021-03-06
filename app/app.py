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

import os
import sys
from . import logging
logger = logging.getLogger(__name__)

from app import stops

from app import message_handler
from app import command_handler

from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
from telegram.ext import CallbackQueryHandler


def run():
    try:
        BOT_TOKEN = os.environ["BOT_TOKEN"]
    except KeyError:
        logger.critical("BOT_TOKEN ENVIRONMENT VARIABLE NOT DEFINED")
        sys.exit(1)

    updater = Updater(token=BOT_TOKEN)
    dispatcher = updater.dispatcher

    # Command handlers
    start_handler = CommandHandler('start', command_handler.start)
    help_handler = CommandHandler('help', command_handler.help)
    about_handler = CommandHandler('about', command_handler.about)
    stats_handler = CommandHandler(
        'stats', command_handler.stats, pass_args=True)

    # Message handlers
    plain_text_handler = MessageHandler(Filters.text, message_handler.message)

    # Inline queries handlers
    inline_queries_handler = CallbackQueryHandler(message_handler.inline_query)

    # Adding the handlers
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(help_handler)
    dispatcher.add_handler(about_handler)
    dispatcher.add_handler(stats_handler)

    dispatcher.add_handler(plain_text_handler)

    dispatcher.add_handler(inline_queries_handler)

    # Starting the bot
    updater.start_polling()

    logger.info("Bot running...")
