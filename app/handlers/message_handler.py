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

import json
import datetime
from pytz import timezone
from app import fetch
from app import stops
from app import logging
logger = logging.getLogger(__name__)
import unicodedata

from app import monitoring

from telegram import ChatAction, InlineKeyboardButton, InlineKeyboardMarkup
from difflib import SequenceMatcher


def message_filter(text):
    """ Checks if the message fulfils the conditions """

    # The message len must be at least 4 letters
    if(len(text) < 4):
        return False

    return True


def get_similar_stops(text, min_ratio):
    """ Returns all the stops that could be similar by name to 'text' """
    similar_stops = []
    for stop in stops:

        similarity_score = 0.0
        for word in stop["title"].split(" "):
            similarity_score += SequenceMatcher(None, text, word).ratio()

        if (similarity_score > min_ratio):
            if stop["title"] not in [x["title"] for x in similar_stops]:
                similar_stops.append(stop)

    return similar_stops


def get_rid_of_accents(text):
    """  """
    return ''.join(c for c in unicodedata.normalize('NFD', text)
                   if unicodedata.category(c) != 'Mn')


@monitoring.monitor
def inline_query(bot, update):
    """  """
    query = update.callback_query
    chat_id = query.message.chat_id
    message_id = query.message.message_id

    # Sends feedback to user that the bot is actually do someting
    bot.send_chat_action(chat_id=chat_id, action=ChatAction.TYPING)

    stops_info = get_stops_matching(query.data)

    try:
        stops_info = get_stops_info(stops_info)
    except RuntimeError:
        msg = "Oops! Parece que la base de datos del Ayuntamiento Zaragoza no funciona 😢\n\n"\
            "Vuelve a intentarlo en otro momento\n\n" \
            "Sentimos las molestias"
        bot.send_message(chat_id=chat_id, parse_mode='markdown', text=msg)
        return

    msg = create_message(stops_info)

    keyboard = [[InlineKeyboardButton(
        "Actualizar", callback_data=query.data)]]

    bot.edit_message_text(
        chat_id=chat_id, parse_mode='markdown', text=msg, message_id=message_id, reply_markup=InlineKeyboardMarkup(keyboard))


def create_message(stops_info):
    """   """
    now = datetime.datetime.now(timezone('Europe/Madrid'))
    msg = ""
    for key, value in stops_info.items():
        # value["directions"].sort(key=lambda destino:)
        msg += "*{}* (Actualizado {:02}:{:02})\n".format(key,
                                                         now.hour, now.minute)

        # Get rid of the direction if has no trams (e.g end of tram line)
        value["directions"] = [direction for direction in value["directions"]
                               if len(direction["trams"])]

        # Sort the directions, this is just to keep the order of names #ocd
        value["directions"].sort(key=lambda item: item["destino"])

        for direction in value["directions"]:
            msg += "  *Dirección:* {}\n".format(direction["destino"])
            for tram in direction["trams"]:
                msg += "    \U0001f68a {:02} min\n".format(tram["minutos"])
        msg += "\n"
    return msg


def send_message(bot, update, message, original_query):
    """   """
    logger.info(message)
    chat_id = update.message.chat_id
    keyboard = [[InlineKeyboardButton(
        "Actualizar", callback_data=original_query)]]

    bot.send_message(chat_id=chat_id, parse_mode='markdown',
                     text=message, reply_markup=InlineKeyboardMarkup(keyboard))


def get_stops_matching(text):
    """   """
    stops_info = {}
    # Get data if any existing stop match the user query
    for stop in stops:
        if text in stop["title"]:
            logger.debug("Match...")
            # Create a key with the stop value if not exists
            if not stop["title"] in stops_info:
                stops_info[stop["title"]] = {}

            # Create a key with a list of directions if not exists
            if not "directions" in stops_info[stop["title"]]:
                stops_info[stop["title"]]["directions"] = []

            # Appends the stop id
            stops_info[stop["title"]]["directions"].append(
                {"id": stop["id"], "trams": []})

    return stops_info


def get_stops_info(stops_info):
    """   """
    # Fill the dict with api data
    for _, value in stops_info.items():
        for direction in value["directions"]:
            try:    
                # API requests
                req_data = fetch.get_stop_info(direction["id"]) 
                
                # If the api does not return data, the api is down
                if not req_data:                    
                    raise RuntimeError
                
                data = req_data["destinos"]
                # Gets the tram last stop that determines the direction
                direction["destino"] = data[0]["destino"]

                # Appends the tram data
                direction["trams"] = data                                                
                    
            except RuntimeError as e:
                raise
            except KeyError as e:
                print(e)
    
    return stops_info


@monitoring.monitor
def message(bot, update):
    """   """
    chat_id = update.message.chat_id

    # Sends feedback to user that the bot is actually do someting
    bot.send_chat_action(chat_id=chat_id, action=ChatAction.TYPING)

    text = update.message.text.upper()

    # Get rid of the accents
    text = get_rid_of_accents(text)

    stops_info = dict()
    # Returns a object like this, it will be used to create the response message
    # stops_info = {
    #     "PLAZA ARAGON": {
    #         "direction": [
    #             {
    #                 "id": 1311,
    #                 "tram": [
    #                     {
    #                         "destino": "MAGO DE OZ",
    #                         "linea": "L1",
    #                         "minutos": 1
    #                     },
    #                     {
    #                         "destino": "MAGO DE OZ",
    #                         "linea": "L1",
    #                         "minutos": 14
    #                     }
    #                 ]
    #             },
    #             {
    #                 "id": 1312,
    #                 ...
    #             }
    #         ]
    #     },
    #     <name>: {
    #         ...
    #     }
    # }

    if not message_filter(text):
        msg = "El nombre de la parada no es válido.\n" \
            "El nombre debe tener al menos 4 caracteres."\
            "Para más ayuda utiliza /help"
        bot.send_message(chat_id=chat_id, parse_mode='markdown',
                         text=msg, reply_markup=None)
        return

    stops_info = get_stops_matching(text)

    # No stops matched
    if not len(stops_info):
        logger.info("no match")
        msg = "La parada introducida no existe. "

        similar_stops = get_similar_stops(text, 1.1)

        if len(similar_stops) == 0:
            msg += "Pruebe de nuevo"
        else:
            msg += "Quizas se referia a:\n"
            for stop in similar_stops:
                msg += "  • {}\n".format(stop["title"])

        bot.send_message(chat_id=chat_id, parse_mode='markdown', text=msg)
        return

    try:        
        stops_info = get_stops_info(stops_info)        
    except RuntimeError:
        msg = "Oops! Parece que la base de datos del Ayuntamiento Zaragoza no funciona 😢\n\n"\
            "Vuelve a intentarlo en otro momento\n\n" \
            "Sentimos las molestias"
        bot.send_message(chat_id=chat_id, parse_mode='markdown', text=msg)
        return

    # logger.info(json.dumps(stops_info, sort_keys=True, indent=4))
    msg = create_message(stops_info)
    send_message(bot, update, msg, text)
