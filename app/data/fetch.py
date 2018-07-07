from app import logging
logger = logging.getLogger(__name__)

import requests
import json

GENERAL_URL = "http://www.zaragoza.es/api/recurso/urbanismo-infraestructuras/tranvia.json?rf=html&results_only=false&srsname=utm30n"

# This url will give just the id and the name of the stop
STOP_INFO = 'https://www.zaragoza.es/sede/servicio/urbanismo-infraestructuras/transporte-urbano/parada-tranvia?fl=id%2C%20title&rf=html&srsname=utm30n&start=0'


def do_get_request(url):
    """ Function used to do get requests"""
    headers = {
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:61.0) Gecko/20100101 Firefox/61.0',
        'content-type': 'application/json',
        'accept': 'application/json'
    }
    r = requests.get(url, headers=headers)

    return (r.text, r.status_code)


def get_stops_info():
    """ Gets the data (id and name) of all the tram stops so lates queries can 
    use that kind of data"""
    logger.info("fetching stops info")
    # with open("tram_raw_data.json", "w") as file:
    (req_data, req_status) = do_get_request(STOP_INFO)
    if(req_status == 200):
        data = json.loads(req_data)['result']
        # file.write(json.dumps(data))
        logger.info("data fetched from the api")
        return data
    else:
        logger.critical('stops data couldn\'t be fetched')
