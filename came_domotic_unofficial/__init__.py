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

import json
import sys
import logging
from importlib.metadata import version, PackageNotFoundError
import requests

from came_domotic_unofficial.models import (
    CameDomoticServerNotFoundError,
    CameDomoticRequestError,
    CommandNotFound,
)

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


def get_logger():
    """
    Returns the package logger, allowing to reconfigure it
    from the main program.
    """
    return _LOGGER


class CameETIDomoServer:
    """
    Class that represents a Came ETI/Domo server.
    """

    # Header for every http request made to the server
    _HTTP_HEADERS = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Connection": "Keep-Alive",
    }

    _HTTP_TIMEOUT = 10  # seconds

    # Dictionary of available commands
    _available_commands = {
        "features": "feature_list_req",
        "lights": "light_list_req",  # "nested_light_list_req",
        # TODO Not tested features are below this line
        "update": "status_update_req",
        "relays": "relays_list_req",
        "cameras": "tvcc_cameras_list_req",
        "timers": "timers_list_req",
        "thermoregulation": "thermo_list_req",
        "analogin": "analogin_list_req",
        "digitalin": "digitalin_list_req",
        "scenarios": "scenarios_list_req",
        "openings": "openings_list_req",
        "energy": None,  # TODO "energy_stat_req",
        "loadsctrl": None,  # TODO "loadsctrl_meter_list_req", + others
        "users": "sl_users_list_req",
        "maps": "map_descr_req",
    }

    def __init__(self, host: str):
        """
        Instantiate a new :class:`Object` of type :class:`Domo`
        that communicates with an Eti/Domo server at the specified ip address

        :param host: A string representing the host/IP of the Eti/Domo server
        :raises :class:`ServerNotFound`: if the :param:`host` is not available
        """

        # Wrap the host ip in a http url
        self._host = "http://" + host + "/domo/"
        # The sequence start from 1
        self._cseq = 0
        # Session id for the client
        self.id = ""

        # List of items managed by the server
        self.entities = {}
        try:
            # Check if the host is available
            response = requests.get(
                self._host, headers=self._HTTP_HEADERS, timeout=10
            )
        except requests.exceptions.ConnectionError:
            self._host = ""
            raise CameDomoticServerNotFoundError

        # If not then raise an exception
        if not response.status_code == 200:
            self._host = ""
            raise CameDomoticServerNotFoundError

    def login(self, username: str, password: str) -> bool:
        """
        Method that takes in the username and password and attempt a login
        to the server. If the login is correct, then the ``id`` parameter
        of the object :class:`Domo` will be set to the session id
        given by the server.

        :param username: username of the user
        :param password: password of the user
        :return: ``<None>``
        """

        # Create the login request
        request_data = {
            "sl_cmd": "sl_registration_req",
            "sl_login": username,
            "sl_pwd": password,
        }

        # Send the post request with the login parameters
        response = requests.post(
            self._host,
            data={"command": json.dumps(request_data)},
            headers=self._HTTP_HEADERS,
            timeout=self._HTTP_TIMEOUT,
        )

        # Set the client id for the session
        self.id = response.json()["sl_client_id"]

        # Check if the user is authorized
        if not response.json()["sl_data_ack_reason"] == 0:
            return False

        return True

    def keep_alive(self) -> bool:
        """
        Method that send a keep alive request to the server
        """

        parameters = (
            'command={"sl_client_id":"'
            + self.id
            + '","sl_cmd":"sl_keep_alive_req"}'
        )

        # Send the post request with the login parameters
        response = requests.post(
            self._host,
            params=parameters,
            headers=self._HTTP_HEADERS,
            timeout=10,
        )

        return response.json()["sl_data_ack_reason"] == 0

    def update_lists(self) -> None:
        """
        Function that update the items dictionary containing all the items
        managed by the eti/domo server
        """

        # Get a list of available features for the user
        features_list = self.list_request(
            self._available_commands["features"]
        )["list"]
        # Populate the items dictionary containing every item of the server
        for feature in features_list:
            # Get the json response from the server
            tmp_list = self.list_request(self._available_commands[feature])
            # Parse the json into a more readable and useful structure
            self.entities[feature] = tmp_list

    def list_request(self, cmd_name) -> dict:
        """
        Method that send the server a request and retrieve a list of items
        identified by the :param:`cmd_name` parameter

        :return: a json dictionary representing the response of the server
        :raises RequestError: if the request is invalid
        :raises CommandNotFound: if the command requested does not exists
        """

        if cmd_name is None:  # TODO remove and fix energy stats case
            return {}

        # Check if the command exists
        if not cmd_name in self._available_commands.values():
            raise CommandNotFound

        # If the user requested the map,
        # then we don't need to pass the client id
        client_id = (
            ""
            if cmd_name == "map_descr_req"
            else '"client":"' + self.id + '",'
        )

        # If requesting a list of users, then the parameters are different
        sl_cmd = (
            '"sl_cmd":"sl_users_list_req"'
            if cmd_name == "sl_users_list_req"
            else '"sl_cmd":"sl_data_req"'
        )
        sl_appl_msg = (
            '"sl_appl_msg":{'
            "" + client_id + ""
            '"cmd_name":"' + cmd_name + '",'
            '"cseq":' + str(self._cseq) + ""
            "},"
            '"sl_appl_msg_type":"domo",'
            if not cmd_name == "sl_users_list_req"
            else ""
        )

        # Create the requests' parameters
        param = (
            "command={"
            "" + sl_appl_msg + ""
            '"sl_client_id":"' + self.id + '",'
            "" + sl_cmd + ""
            "}"
        )

        # Send the post request
        response = requests.post(
            self._host, params=param, headers=self._HTTP_HEADERS, timeout=10
        )

        # Get a json dictionary from the response
        response_json = response.json()

        # Increment the cseq counter
        self._cseq += 1

        # Check if the response is valid
        if not response_json["sl_data_ack_reason"] == 0:
            raise CameDomoticRequestError

        # Return the json of the response
        return response_json

    def switch(
        self, act_id: int, status: bool = True, is_light: bool = True
    ) -> dict:
        """
        Method to turn on or off a light switch or a relays

        :param act_id: id of the light/relay to be turned on or off
        :param status: True if the light/relay is to be turned on, False if off
        :param is_light: True if actin on a light, False if it is a relay
        :return: a json dictionary representing the response of the server
        :raises RequestError: Raise a RequestError if the request is invalid
        """

        # Check if the user wants the light to be turned on or off
        status = "1" if status else "0"

        # Check if the user want to switch a light or activate a relay
        cmd_name = "light_switch_req" if is_light else "relay_activation_req"

        # Create the requests' parameters
        param = (
            "command={"
            '"sl_appl_msg":{'
            '"act_id":' + str(act_id) + ","
            '"client":"' + self.id + '",'
            '"cmd_name":"' + cmd_name + '",'
            '"cseq":' + str(self._cseq) + ","
            '"wanted_status":' + status + ""
            "},"
            '"sl_appl_msg_type":"domo",'
            '"sl_client_id":"' + self.id + '",'
            '"sl_cmd":"sl_data_req"'
            "}"
        )

        # Send the post request
        response = requests.post(
            self._host, params=param, headers=self._HTTP_HEADERS, timeout=10
        )

        # Increment the cseq counter
        self._cseq += 1

        # Check if the response is valid
        if not response.json()["sl_data_ack_reason"] == 0:
            raise CameDomoticRequestError

        # After every action performed we update the list of items
        self.update_lists()

        # Return the json of the response
        return response.json()

    def thermo_mode(self, act_id: int, mode: int, temp: float) -> dict:
        """
        Method to change the operational mode of a thermo zone

        :param act_id: id of the thermo zone to be configured
        :param mode: 0 Turned off, 1 Manual mode, 2 Auto mode, 3 Jolly mode
        :param temp: Temperature to set
        :return: a json dictionary representing the response of the server
        :raises RequestError: Raise a RequestError if the request is invalid
        """

        # Check if the mode exists
        if mode not in [0, 1, 2, 3]:
            raise CameDomoticRequestError

        # Transform temperature from float to int,we need to pass the server
        # an integer value, which is in Celsius, but multiplied by 10
        # we also round the float value to only 1 digits
        value = int(round(temp * 10, 1))

        # Create the requests' parameters
        param = (
            "command={"
            '"sl_appl_msg":{'
            '"act_id":' + str(act_id) + ","
            '"client":"' + self.id + '",'
            '"cmd_name":"thermo_zone_config_req",'
            '"cseq":' + str(self._cseq) + ","
            '"extended_infos": 0,'
            '"mode":' + str(mode) + ","
            '"set_point":' + str(value) + ""
            "},"
            '"sl_appl_msg_type":"domo",'
            '"sl_client_id":"' + self.id + '",'
            '"sl_cmd":"sl_data_req"'
            "}"
        )

        # Send the post request
        response = requests.post(
            self._host, params=param, headers=self._HTTP_HEADERS, timeout=10
        )

        # Increment the cseq counter
        self._cseq += 1

        # Check if the response is valid
        if not response.json()["sl_data_ack_reason"] == 0:
            raise CameDomoticRequestError

        # After every action performed we update the list of items
        self.update_lists()

        # Return the json of the response
        return response.json()

    def change_season(self, season: str) -> dict:
        """
        Method that change the season of the entire thermo implant

        :param season: string defining the season
        :return: a json dictionary representing the response of the server
        :raises RequestError: Raise a RequestError if the request is invalid
        """

        # Check if the season exists
        if season not in ["plant_off", "summer", "winter"]:
            raise CameDomoticRequestError

        # Create the requests' parameters
        param = (
            "command={"
            '"sl_appl_msg":{'
            '"client":"' + self.id + '",'
            '"cmd_name":"thermo_season_req",'
            '"cseq":' + str(self._cseq) + ","
            '"season":"' + season + '"'
            "},"
            '"sl_appl_msg_type":"domo",'
            '"sl_client_id":"' + self.id + '",'
            '"sl_cmd":"sl_data_req"'
            "}"
        )

        # Send the post request
        response = requests.post(
            self._host, params=param, headers=self._HTTP_HEADERS, timeout=10
        )

        # Increment the cseq counter
        self._cseq += 1

        # Check if the response is valid
        if not response.json()["sl_data_ack_reason"] == 0:
            raise CameDomoticRequestError

        # After every action performed we update the list of items
        self.update_lists()

        # Return the json of the response
        return response.json()
