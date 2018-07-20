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


from app import fetch
from app import stops
from app import logging
logger = logging.getLogger(__name__)
import unicodedata

from telegram import ChatAction
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

        print("{} : {}".format(stop["title"], similarity_score))

        if (similarity_score > min_ratio):
            if stop["title"] not in [x["title"] for x in similar_stops]:
                similar_stops.append(stop)

    return similar_stops


def get_rid_of_accents(text):
    return ''.join(c for c in unicodedata.normalize('NFD', text)
                   if unicodedata.category(c) != 'Mn')


def message(bot, update):
    """ Function than it's executed when a plain text message is received """
    logger.debug("Plain message received")

    chat_id = update.message.chat_id

    # Sends feedback to user that the bot is actually do someting
    bot.send_chat_action(chat_id=chat_id, action=ChatAction.TYPING)

    text = update.message.text.upper()

    # Get rid of the accents
    text = get_rid_of_accents(text)

    stops_info = dict()
    # stops_info = {
    #     "PLAZA ARAGON": {
    #         "direction": [
    #             {
    #                 "id": 1311,
    #                 "tram": [
    #                     {}
    #                 ]
    #             },
    #             {
    #                 "id": 1312
    #             }
    #         ]
    #     },
    #     <name>: {
    #         ...
    #     }
    # }

    if(message_filter(text)):
        # Creates the main structure
        logger.debug("Searching for stop matching")
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

        # Fill the dict with api data
        for key, value in stops_info.items():
            for direction in value["directions"]:
                logger.debug(
                    "Trying to fetch data for stop: {}".format(direction["id"]))
                req_data, err = fetch.get_stop_info(direction["id"])
                try:
                    data = req_data["destinos"]
                    print("DATA: {}".format(data))

                    # Gets the tram last stop that determines the direction
                    direction["destino"] = data[0]["destino"]

                    # Appends the tram data
                    direction["trams"] = data
                except KeyError as e:
                    print(e)

        # Create the response to the user query
        logger.debug("Creating the response")
        msg = ""
        for key, value in stops_info.items():
            # value["directions"].sort(key=lambda destino:)
            msg += "*{}*\n".format(key)

            # Sort the directions, this is just to keep the order of names #ocd
            value["directions"].sort(key=lambda item: item["destino"])

            for direction in value["directions"]:
                msg += "  *Dirección:* {}\n".format(direction["destino"])
                for tram in direction["trams"]:
                    msg += "    \U0001f68a {:02} min\n".format(tram["minutos"])
            msg += "\n"

        # No stop matched, so return suggestion if there are
        if(msg == ""):
            msg = "La parada introducida no existe. "

            similar_stops = get_similar_stops(text, 1.1)

            if len(similar_stops) == 0:
                msg += "Pruebe de nuevo"
            else:
                msg += "Quizas se referia a:\n"
                for stop in similar_stops:
                    msg += "  \u2022 {}\n".format(stop["title"])

    else:  # Invalid stop name
        msg = """El nombre de la parada no es valido.\
El nombre debe tener al menos 4 caracteres.
Para mas ayuda utiliza /help"""

    bot.send_message(chat_id=chat_id, parse_mode='markdown', text=msg)

    logger.debug("Plain message handling finished")
