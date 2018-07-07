import os
import logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

from .data import fetch

# Loads the config
import yaml
config_path = os.path.join(os.environ['BASE_PATH'], 'etc', 'config.yaml')
with open(config_path, 'r') as ymlfile:
    config = yaml.load(ymlfile)

app_config = config['app']

# Fetchs the data from the api about stop id and name
stops = fetch.get_stops_info()

# Import all handlers
from .handlers import message_handler
from .handlers import command_handler

from . import app
