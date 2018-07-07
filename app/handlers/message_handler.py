from app import fetch


def message(bot, update):
    """ Function than it's executed when a plain text message is received """
    text = update.message.text.upper()

    bot.send_message(chat_id=update.message.chat_id, text=text)
