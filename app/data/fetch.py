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


from app import logging
logger = logging.getLogger(__name__)

import requests
import json

GENERAL_URL = "http://www.zaragoza.es/api/recurso/urbanismo-infraestructuras/tranvia.json?rf=html&results_only=false&srsname=utm30n"

# This url will give just the id and the name of the stop
ALL_STOPS_INFO = "https://www.zaragoza.es/sede/servicio/urbanismo-infraestructuras/transporte-urbano/parada-tranvia?fl=id%2C%20title&rf=html&srsname=utm30n&start=0"

# This url will give the tram stop time. Tram stop will be fill the `{}`
SINGLE_STOP = "https://www.zaragoza.es/sede/servicio/urbanismo-infraestructuras/transporte-urbano/parada-tranvia/{}?fl=destinos&rf=html&srsname=utm30n"


def do_get_request(url):
    """ Function used to do get requests"""
    headers = {
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64; rv:61.0) Gecko/20100101 Firefox/61.0",
        "content-type": "application/json",
        "accept": "application/json"
    }
    r = requests.get(url, headers=headers)
    r.raise_for_status()

    return r


def get_all_stops_info():
    """ Gets the data (id and name) of all the tram stops so lates queries can 
    use that kind of data.
    Returns a tuple (data, err). data is a dict"""
    logger.info("Fetching stops info")
    try:
        req = do_get_request(ALL_STOPS_INFO)
        data = json.loads(req.text)["result"]

        # The api replaces all the 'ñ' with 'n' so this casts backwards
        for item in data:
            item["title"] = item["title"].replace("ESPANA", "ESPAÑA")

        logger.debug("Data fetched from the api")
        return (data, False)
    except requests.exceptions.HTTPError as err:
        # logger.critical("stops data couldn't be fetched")
        logger.critical(err)
        return (None, True)


def get_stop_info(stop):
    """ Gets the data of a stop.
    Returns a tuple (data, err). data is a dict """
    try:
        logger.debug(SINGLE_STOP.format(stop))
        req = do_get_request(SINGLE_STOP.format(stop))
        # TODO: Figure out why json.loads(req.text)["destinos"] does not work
        data = json.loads(req.text)

        logger.debug("Stop info fetched from the api")

        return (data, False)
    except requests.exceptions.HTTPError as err:
        # logger.critical("stop info couldn't ")
        logger.critical(err)
        return ("", True)
