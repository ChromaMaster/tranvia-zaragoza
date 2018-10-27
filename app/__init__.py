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


import os
import logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)
from .data import fetch

# Loads the config
# logger.debug("Loading the config...")
# import yaml
# config_path = os.path.join(os.environ['BASE_PATH'], 'etc', 'config.yaml')
# with open(config_path, 'r') as ymlfile:
#     config = yaml.load(ymlfile)

# app_config = config['app']

logger.debug("Config loaded...")

# Fetchs the data from the api about stop id and name
stops = fetch.get_all_stops_info()

# Import all handlers
from .handlers import message_handler
from .handlers import command_handler

from . import monitoring

from . import app
