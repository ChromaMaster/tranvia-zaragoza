from functools import wraps
from app import logging
logger = logging.getLogger(__name__)

import os
admin_id = os.environ.get("BOT_ADMIN_ID")


def only_whitelist(f):
    """ Ensure user is present in whitelist. Function wrapped should receive

        Wrapped function has to get a Bot object as first parameter (args[0]) and 
        Update object as secont one (args[1]).

        args[0] -- Bot object
        args[1] -- Update object
    """
    @wraps(f)
    def wrapper(bot, update, *args, **kwargs):
        if admin_id is None:
            message = "ERROR: BOT_ADMIN_ID no definido.\n"\
                "debes definirlo para ejecutar los comandos de administrador.\n\n"\
                " Si tu eres el administrador, tu id es {}".format(
                    update.effective_user.id)
            bot.send_message(chat_id=update.message.chat_id, text=message)
            return
        if update.effective_user.id == admin_id:
            message = "No esta autorizado a utilizar este comando"
            bot.send_message(chat_id=update.message.chat_id, text=message)
            return
        return f(bot, update, *args, **kwargs)
    return wrapper
