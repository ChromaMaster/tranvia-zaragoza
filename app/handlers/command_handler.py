from app import fetch
from app import stops


def start(bot, update):
    """ Function than it's executed when the command '/start' is received """
    bot.send_message(chat_id=update.message.chat_id,
                     text="I'm a bot, please talk to me!")


def help(bot, update):
    """ Function that it's executed when the command '/help' is received """
    help_message = """
  """
    msg = ""
    for stop in stops:
        print(stop)
        msg += "*" + stop['title'] + "*:" + stop['id'] + "\n"
    bot.send_message(chat_id=update.message.chat_id,
                     parse_mode='markdown', text=help_message)
