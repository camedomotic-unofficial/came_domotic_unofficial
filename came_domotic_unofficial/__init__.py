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

"""
Library to exchange data with a CAME Domotic server (ETI/Domo).

This library provides a Python interface allowing to interact
with a CAME ETI/Domo server.

Disclaimer:
This library is not affiliated with or endorsed by CAME.
"""

import sys
import logging
from importlib.metadata import version, PackageNotFoundError

# Get the package version
try:
    __version__ = version(__name__)
except PackageNotFoundError:
    # package is not installed
    __version__ = "unknown"


# Create a logger for the package
_LOGGER = logging.getLogger(__package__)
formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s - %(module)s \
        - %(funcName)s (line %(lineno)d)"
)
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(formatter)
_LOGGER.addHandler(console_handler)
_LOGGER.setLevel(logging.DEBUG)

# Write the message "Initialization completed" to the log
_LOGGER.info("Package initialization completed")


def get_logger():
    """
    Returns the package logger, allowing to reconfigure it
    from the main program.
    """
    return _LOGGER
