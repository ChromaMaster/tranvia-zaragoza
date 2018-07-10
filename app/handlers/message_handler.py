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


def message(bot, update):
    """ Function than it's executed when a plain text message is received """
    logger.debug("Plain message received")
    text = update.message.text.upper()

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

    # No stop matched
    if(msg == ""):
        msg = "La parada introducida no existe. Pruebe de nuevo"

    bot.send_message(chat_id=update.message.chat_id,
                     parse_mode='markdown', text=msg)

    logger.debug("Plain message handling finished")
