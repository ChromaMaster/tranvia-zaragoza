import os
import hashlib
from influxdb import InfluxDBClient
import datetime
import dateutil
from pytz import timezone
from functools import wraps
from app import logging
logger = logging.getLogger(__name__)

from app import stops

from threading import Lock

connection = None
insert_lock = None

import os
MONITORING_HOST = os.environ.get("MONITORING_HOST")
MONITORING_PORT = os.environ.get("MONITORING_PORT")
MONITORING_USER = os.environ.get("MONITORING_USER")
MONITORING_PASS = os.environ.get("MONITORING_PASS")
MONITORING_DATABASE_NAME = os.environ.get("MONITORING_DATABASE_NAME")


def check_connection(f):
    """ Checks if connection is created. """
    @wraps(f)
    def wrapper(*args, **kwargs):
        # Can't perform function if not connected to database
        if connection is None:
            return
        return f(*args, **kwargs)
    return wrapper


def monitor(f):
    """ Decorator used to monitor the executed bot functions """
    @wraps(f)
    def wrapper(bot, update, *args, **kwargs):

        # Do not monitor if host not set
        if(MONITORING_HOST is None or MONITORING_PORT is None or
           MONITORING_USER is None or MONITORING_PASS is None or
           MONITORING_DATABASE_NAME is None):
            return f(bot, update, *args, **kwargs)

        now = datetime.datetime.now(timezone('Europe/Madrid'))
        # CallbackQuery message
        if update.callback_query:
            chat_id = update.callback_query.message.chat_id
            text = update.callback_query.data
            action = "update"

        # Plain message
        else:
            chat_id = update.message.chat_id
            text = update.message.text.upper()
            action = "new"

        chat_id_hash = hashlib.sha224(str(chat_id).encode()).hexdigest()

        stops_names = [stop["title"] for stop in stops]

        # sorted(set(stops_names)) gets just the unique tram stops
        # and stores in the database
        logger.info(now)
        for stop in sorted(set(stops_names)):
            if text in stop:
                insert_row(chat_id_hash, now, action, stop)

        return f(bot, update, *args, **kwargs)
    return wrapper


def create_connection(host, port, user, password):
    """ Opens a connection with the InfluxDB database """
    global connection, insert_lock

    connection = InfluxDBClient(host=host, port=port, username=user,
                                password=password, database=MONITORING_DATABASE_NAME)

    # Creates the database if not exists
    connection.create_database(MONITORING_DATABASE_NAME)

    # Lock used for inserting data
    insert_lock = Lock()


def insert_row(user_id, now, action, stop):
    """ Inserts a point into the database with the stop the user requested """
    insert_lock.acquire()

    # If connection is opened
    if connection:
        points = [
            {
                "measurement": "requests",
                "tags": {
                    "tag_user_id": user_id,
                    "tag_action": action,
                    "tag_stop": stop
                },
                "time": now,
                "fields": {
                    "stop": stop
                }
            }
        ]

        connection.write_points(points)

    insert_lock.release()


@check_connection
def get_global_stats(init_date, end_date):
    """ Return total number of requests, percentage of "new" or "update" requests
    depending on action, hours of usage """

    #
    # NUMBER OF REQUESTS
    #
    res = connection.query("SELECT count(*) FROM requests")

    # Checks if there is any requests yet
    if len(list(res.get_points())) == 0:
        return

    number_of_requests = list(res.get_points())[0]["count_stop"]
    msg = "Total number of requests: {}\n".format(number_of_requests)

    #
    # NUMBER OF NEW/UPDATE REQUESTS
    #
    res = connection.query("SELECT count(*) FROM requests GROUP BY tag_action")
    action_count = {}
    for key, item in res.items():
        action_count[key[1]["tag_action"]] = list(item)[0]["count_stop"]

    msg += "\tNumber of **new** requests: {} ({:.1%})\n".format(
        action_count.get("new", 0), action_count.get("new", 0)/number_of_requests)

    msg += "\tNumber of **update** requests: {} ({:.1%})\n".format(
        action_count.get("update", 0), action_count.get("update", 0)/number_of_requests)

    #
    # RUSH HOURS
    #
    msg += "\tRush Hours:\n"
    res = connection.query(
        "SELECT count(*) FROM requests GROUP BY time(1h) TZ('Europe/Madrid')")
    dates = list(res.get_points())

    # Agregate hours between hours
    hours = {}
    for date in dates:
        key = str(dateutil.parser.parse(date["time"]).hour)
        if not key in hours:
            hours[key] = date["count_stop"]
        else:
            hours[key] += date["count_stop"]

    # Get the keys sorted by descending value
    sorted_hours = sorted(hours, key=hours.get, reverse=True)

    for hour in sorted_hours[0:5]:
        msg += "\t\tHour {}: {} ({:.1%})\n".format(hour,
                                                   hours[hour], hours[hour]/number_of_requests)

    return msg


@check_connection
def get_user_stats(init_date, end_date):
    """ Return stats related to users usage. Eg. total count of users, mean of usage per user, ... """

    #
    # USER COUNT
    #
    res = connection.query(
        "SHOW TAG VALUES CARDINALITY FROM requests WITH KEY = tag_user_id")

    # Checks if there is any requests yet
    if len(list(res.get_points())) == 0:
        return

    number_of_users = list(res.get_points())[0]["count"]
    msg = "Users count: {}".format(number_of_users)

    return msg


@check_connection
def get_stop_stats(init_date, end_date):
    """ Return the most requested stops, """

    #
    # RANKING
    #
    ranking = []
    res = connection.query("SELECT count(*) FROM requests GROUP BY tag_stop")

    # Checks if there is any requests yet
    if len(list(res.get_points())) == 0:
        return

    msg = "Stops ranking: \n"

    for key, item in res.items():
        ranking.append((key[1]["tag_stop"], list(item)[0]["count_stop"]))

    ranking.sort(key=lambda x: x[1], reverse=True)
    for stop, count in ranking:
        msg += "\t\t{}: {}\n".format(stop, count)

    return msg


# If monitoring env vars has been provided, connect to database.
if(MONITORING_HOST is not None and MONITORING_PORT is not None and
   MONITORING_USER is not None and MONITORING_PASS is not None and
   MONITORING_DATABASE_NAME is not None):

    logger.info("Monitoring enabled")

    create_connection(MONITORING_HOST, MONITORING_PORT, MONITORING_USER,
                      MONITORING_PASS)
