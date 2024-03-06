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

"""This module contains examples of responses from the CAME Domotic server.

These responses are used to test the CAME Domotic server client.
"""

# pylint: disable=import-error
# pylint: disable=no-name-in-module
# pylint: disable=unused-argument

import copy
import json
from unittest.mock import Mock
from mocked_responses import (
    SL_REGISTRATION_ACK,
    FEATURE_LIST_RESP,
    STATUS_UPDATE_RESP,
    LIGHT_LIST_RESP,
    OPENINGS_LIST_RESP,
    SCENARIOS_LIST_RESP,
    DIGITALIN_LIST_RESP,
    THERMO_LIST_RESP,
    ENERGY_STAT_RESP,
    METERS_LIST_RESP,
    LOADSCTRL_METER_LIST_RESP,
    TERMINALS_GROUPS_LIST_RESP,
    SL_USERS_LIST_RESP,
    SL_LOGOUT_ACK,
    SL_KEEP_ALIVE_ACK,
    GENERIC_REPLY,
)

COMMAND_TO_RESPONSE = {
    "sl_users_list_req": SL_USERS_LIST_RESP,
    "sl_registration_req": SL_REGISTRATION_ACK,
    "feature_list_req": FEATURE_LIST_RESP,
    "status_update_req": STATUS_UPDATE_RESP,
    "light_list_req": LIGHT_LIST_RESP,
    "openings_list_req": OPENINGS_LIST_RESP,
    "scenarios_list_req": SCENARIOS_LIST_RESP,
    "digitalin_list_req": DIGITALIN_LIST_RESP,
    "thermo_list_req": THERMO_LIST_RESP,
    "energy_stat_req": ENERGY_STAT_RESP,
    "meters_list_req": METERS_LIST_RESP,
    "loadsctrl_meter_list_req": LOADSCTRL_METER_LIST_RESP,
    "terminals_groups_list_req": TERMINALS_GROUPS_LIST_RESP,
    "sl_keep_alive_req": SL_KEEP_ALIVE_ACK,
    "sl_logout_req": SL_LOGOUT_ACK,
    # "light_switch_req": None,
    # "opening_move_req": None,
    # "scenario_activation_req": None,
    # "thermo_zone_config_req": None,
    # "thermo_season_req": None,
    # "loadsctrl_meter_set_req": None,
    # "loadsctrl_relay_set_req": None,
}


###################
#  USAGE EXAMPLE  #
###################
# from utils import mock_post_method
#
# @patch("requests.Session.get", side_effect=mock_get_init)
# def test_my_test(mock_get, mocked_server):
def mock_get_init(*args, **kwargs):
    """Mock the GET response when creating a CameETIDomoServer instance."""
    mock_response = Mock()
    mock_response.status_code = 200
    return mock_response


###################
#  USAGE EXAMPLE  #
###################
# from utils import mock_post_method
#
# @patch("requests.Session.post", side_effect=mock_post_method)
# def test_my_test(mock_post, mocked_server):
def mock_post_method(*args, **kwargs):
    """Mock the all the POST responses when sending a command to the server."""

    mock_response = Mock()
    mock_response.status_code = 200

    if "data" in kwargs and "command" in kwargs["data"]:
        request_data = json.loads(kwargs["data"]["command"])
    elif "json" in kwargs and "command" in kwargs["json"]:
        request_data = json.loads(kwargs["json"]["command"])

    if request_data:
        if "sl_appl_msg" in request_data and "cmd_name" in request_data["sl_appl_msg"]:
            came_cmd_name = request_data["sl_appl_msg"]["cmd_name"]
        elif "sl_cmd" in request_data:
            came_cmd_name = request_data["sl_cmd"]
        else:
            came_cmd_name = None

    if came_cmd_name:
        # Using copy.deepcopy to enable playing on the response object
        # without messing up the original COMMAND_TO_RESPONSE object
        mock_response.json.return_value = copy.deepcopy(
            (
                COMMAND_TO_RESPONSE[came_cmd_name]
                if came_cmd_name in COMMAND_TO_RESPONSE
                else GENERIC_REPLY
            )
        )

    return mock_response


def mock_post_method_error_auth(*args, **kwargs):
    """Mock the POST response simulating an authentication error.

    Every other POST request will work as expected, but the authentication
    request will return an error.
    """
    mock_response = mock_post_method(*args, **kwargs)
    response_data = mock_response.json.return_value

    if not response_data:
        sl_cmd = None
    elif "sl_cmd" in response_data:
        sl_cmd = response_data["sl_cmd"]
    elif "cmd_name" in response_data:
        sl_cmd = response_data["cmd_name"]
    else:
        sl_cmd = None

    if sl_cmd == "sl_registration_ack":
        mock_response.status_code = 403

    return mock_response


def mock_post_method_error_non_auth(*args, **kwargs):
    """Mock the POST response simulating a server error.

    Only the authentication requests will work, every other POST request will fail.
    """
    mock_response = mock_post_method(*args, **kwargs)
    response_data = mock_response.json.return_value

    if not response_data:
        sl_cmd = None
    elif "sl_cmd" in response_data:
        sl_cmd = response_data["sl_cmd"]
    elif "cmd_name" in response_data:
        sl_cmd = response_data["cmd_name"]
    else:
        sl_cmd = None

    if sl_cmd != "sl_registration_ack":
        mock_response.status_code = 500

    return mock_response
