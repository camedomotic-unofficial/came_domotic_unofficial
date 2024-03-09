# Copyright 2024 - GitHub user: fredericks1982

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


"""TEST
This library allows to interact with a CAME ETI/Domo server.

The login to the remote server is managed by the library, and performed only
when required. You can always check the status of the server with the
is_authenticated property.

The library is based on the HTTP messages exchanged by the CAME Domotic Android
app. The library is not complete and does not cover all the features
of a CAME ETI/Domo server.

The library is not official and is not supported by CAME.
Use it at your own risk


Usage:
    from came_domotic_unofficial import CameETIDomoServer

    with CameETIDomoServer("192.168.0.0", "username", "password") as server:
        features = server.get_features() # list of available features
        entities = server.get_entities() # list of managed entities
        server.set_entity_status(entities[0], EntityStatus.ON)
"""

# pylint: disable=unused-import

import sys
import logging
from importlib.metadata import version, PackageNotFoundError
from .came_etidomo_server import CameETIDomoServer

# Get the package version
try:
    __version__ = version(__name__)
except PackageNotFoundError:
    # package is not installed
    __version__ = "unknown"


# Create a logger for the package
_LOGGER = logging.getLogger(__package__)
_formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s - "
    "%(module)s:%(lineno)d (%(funcName)s)"
)
_console_handler = logging.StreamHandler(sys.stdout)
_console_handler.setFormatter(_formatter)
_LOGGER.addHandler(_console_handler)
_LOGGER.setLevel(logging.DEBUG)


def get_logger():
    """
    Allows to set the log level and other properties from the calling code.

    Returns:
        Logger: The package logger
    """
    return _LOGGER
