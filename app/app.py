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

    # Message handlers
    plain_text_handler = MessageHandler(Filters.text, message_handler.message)

    # Adding the handlers
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(help_handler)

    dispatcher.add_handler(plain_text_handler)

    # Starting the bot
    updater.start_polling()

    logger.info("Bot running...")
