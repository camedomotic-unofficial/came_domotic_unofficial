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

# pylint: disable=protected-access
# pylint: disable=redefined-outer-name
# pylint: disable=no-name-in-module

"""Test the public methods of the CameETIDomoServer class."""

import copy
from datetime import datetime, timezone
import json
from unittest.mock import patch, Mock
import pytest
import requests
from mocked_responses import (
    FEATURE_LIST_RESP,
    GENERIC_REPLY,
    Command2MockedResponse,
    MockedEntities,
    MockedLights,
    MockedOpenings,
    MockedDigitalInputs,
    MockedScenarios,
)
from came_domotic_unofficial.came_etidomo_server import CameETIDomoServer
from came_domotic_unofficial.models import (
    FeatureSet,
    Feature,
    CameEntitySet,
    CameEntity,
    Light,
    Opening,
    DigitalInput,
    Scenario,
    EntityType,
    EntityStatus,
    CameDomoticRequestError,
    CameDomoticBadAckError,
)


# region Tests


@pytest.fixture
@patch("requests.Session.get")
def mocked_server_auth(mock_get) -> CameETIDomoServer:
    """
    Fixture that provides an authenticated instance of CameETIDomoServer.
    """
    with patch("requests.Session.get") as mock_get:
        mock_get.return_value.status_code = 200
        server = CameETIDomoServer("192.168.0.3", "user", "password")

        # Manually set session attributes to emulate the authentication
        server._session_id = "my_session_id"
        server._session_expiration_timestamp = datetime(3000, 1, 1, tzinfo=timezone.utc)
        server._cseq = 0
        server._keycode = FEATURE_LIST_RESP["keycode"]
        server._software_version = FEATURE_LIST_RESP["swver"]
        server._type = FEATURE_LIST_RESP["type"]
        server._board = FEATURE_LIST_RESP["board"]
        server._serial_number = FEATURE_LIST_RESP["serial"]

        server.dispose = lambda: None  # disable the dispose() method
        return server


@patch.object(requests, "post")
def test_get_features_with_cache(mock_post, mocked_server_auth):
    """
    Test the get_features() method ot the CameETIDomoServer class to ensure that,
    if the self._features attribute is not None or empty, the method returns the cached
    features list and does not submit any POST request to the server.
    """

    cached_features = FeatureSet(
        [
            Feature("A"),
            Feature("B"),
            Feature("C"),
            Feature("D"),
        ]
    )

    # Set the features cache
    mocked_server_auth._features = cached_features

    # Call the get_features method
    features = mocked_server_auth.get_features()

    # Check if the features list is correct and is retrieved from the cache
    assert features == cached_features
    mock_post.assert_not_called()

    # Emulate logout, to neutralize the call to the dispose() method
    # that would fail since it would try to call the remote server
    # mocked_server_auth._session_id = ""


@patch.object(requests.Session, "post")
def test_get_features_no_cache(mock_post, mocked_server_auth):
    """
    Test if the get_features method correctly fetches the features list
    when it is not cached.
    """

    # Create a mock response with status code 200 and some data
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = FEATURE_LIST_RESP
    mock_features = set([Feature(name) for name in FEATURE_LIST_RESP["list"]])

    mock_post.return_value = mock_response

    # Clear the features cache
    mocked_server_auth._features = None

    # Call the get_features method
    features = mocked_server_auth.get_features()

    assert mock_post.call_count == 1
    assert features == mock_features

    # Clear again the features cache
    mocked_server_auth._features = FeatureSet()

    # Call the get_features method
    features = mocked_server_auth.get_features()

    assert mock_post.call_count == 2
    assert features == mock_features

    # Emulate logout, to neutralize the call to the dispose() method
    # that would fail since it would try to call the remote server
    mocked_server_auth._session_id = ""


@patch.object(requests.Session, "post")
def test_get_features_errors(mock_post, mocked_server_auth):
    """
    Test that failures are managed as expected.
    """
    # Data preparation
    mock_post.return_value.status_code = 500
    mocked_server_auth._entities = None

    # Test HTTP error
    with pytest.raises(CameDomoticRequestError):
        # Call the function that sends the POST requests
        mocked_server_auth.get_features()

    # Test invalid response
    mock_post.return_value.status_code = 200
    mock_post.return_value = {"invalid_key": "invalid_value"}

    with pytest.raises(CameDomoticRequestError):
        # Call the function that sends the POST requests
        mocked_server_auth.get_features()

    # Test bad ACK
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = copy.deepcopy(GENERIC_REPLY)
    mock_response.json.return_value["sl_data_ack_reason"] = 1
    mock_post.return_value = mock_response

    with pytest.raises(CameDomoticBadAckError):
        # Call the function that sends the POST requests
        mocked_server_auth.get_features()

    # Emulate logout, to neutralize the call to the dispose() method
    # that would fail since it would try to call the remote server
    mocked_server_auth._session_id = ""


@patch.object(requests, "post")
def test_get_entities_with_cache(mock_post, mocked_server_auth):
    """
    Test the get_entities() method ot the CameETIDomoServer class to ensure that,
    if the self._entities attribute is not None or empty, the method returns the cached
    entities list and does not submit any POST request to the server.
    """

    cached_entities = CameEntitySet(
        [
            CameEntity(1),
            CameEntity(2),
            CameEntity(3),
            CameEntity(4),
        ]
    )

    # Set the features cache
    mocked_server_auth._entities = cached_entities

    # Call the get_features method
    entities = mocked_server_auth.get_entities()

    # Check if the features list is correct and is retrieved from the cache
    assert entities == cached_entities
    mock_post.assert_not_called()

    # Emulate logout, to neutralize the call to the dispose() method
    # that would fail since it would try to call the remote server
    mocked_server_auth._session_id = ""


@patch.object(requests.Session, "post")
def test_get_entities_no_cache(mock_post, mocked_server_auth):
    """
    Test that an HTTP POST request returns the expected data.
    """

    # Create mock responses for each command
    mock_responses = {command: Mock() for command in Command2MockedResponse}

    # Set the status code and data for each mock response
    for command, response in Command2MockedResponse.items():
        mock_responses[command].status_code = 200
        mock_responses[command].json.return_value = response

    # Set the side_effect of the post method to return the correct mock response based on the input
    def side_effect(*args, **kwargs):
        # Extract the command from the JSON data in the request
        data = kwargs.get("data", {})
        raw_input = data.get("command")
        json_input = json.loads(raw_input)
        command = json_input.get("sl_appl_msg").get("cmd_name")
        return mock_responses.get(command)

    mock_post.side_effect = side_effect

    # Clear the entities cache
    mocked_server_auth._entities = None

    # Call the function that sends the POST requests
    entities = mocked_server_auth.get_entities()
    assert entities == MockedEntities

    # Clear the entities cache
    mocked_server_auth._entities = CameEntitySet()
    entities = None

    # Call the function that sends the POST requests
    entities = mocked_server_auth.get_entities()
    assert entities == MockedEntities

    # Emulate logout, to neutralize the call to the dispose() method
    # that would fail since it would try to call the remote server
    mocked_server_auth._session_id = ""


@patch.object(requests.Session, "post")
def test_get_entities_errors(mock_post, mocked_server_auth):
    """
    Test that an HTTP POST request returns the expected data.
    """
    # Data preparation
    mock_post.return_value.status_code = 500
    mocked_server_auth._entities = None

    # Test HTTP error
    with pytest.raises(CameDomoticRequestError):
        # Call the function that sends the POST requests
        mocked_server_auth.get_entities()

    # Test invalid response
    mock_post.return_value.status_code = 200
    mock_post.return_value = {"invalid_key": "invalid_value"}

    with pytest.raises(CameDomoticRequestError):
        # Call the function that sends the POST requests
        mocked_server_auth.get_entities()

    # Test bad ACK
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = copy.deepcopy(GENERIC_REPLY)
    mock_response.json.return_value["sl_data_ack_reason"] = 1
    mock_post.return_value = mock_response

    with pytest.raises(CameDomoticBadAckError):
        # Call the function that sends the POST requests
        mocked_server_auth.get_entities()

    # Emulate logout, to neutralize the call to the dispose() method
    # that would fail since it would try to call the remote server
    mocked_server_auth._session_id = ""


def test_get_entities_filtered(mocked_server_auth):
    """
    Test the get_entities() method ot the CameETIDomoServer class to ensure that,
    if the self._entities attribute is not None or empty, the method returns the cached
    entities list and does not submit any POST request to the server.
    """

    cached_entities = CameEntitySet(
        [
            Light(1),
            Light(2),
            Opening(3),
            Scenario(4),
        ]
    )

    filtered_entities = CameEntitySet(
        [item for item in cached_entities if isinstance(item, Light)]
    )

    # Set the features cache
    mocked_server_auth._entities = cached_entities

    # Call the get_features method
    entities = mocked_server_auth.get_entities(EntityType.LIGHTS)

    # Check if the features list is correct and is retrieved from the cache
    assert entities == filtered_entities

    # Emulate logout, to neutralize the call to the dispose() method
    # that would fail since it would try to call the remote server
    mocked_server_auth._session_id = ""


def test_get_entities_filtered_invalid_input(mocked_server_auth):
    """
    Test the get_entities() method ot the CameETIDomoServer class to ensure that,
    if the self._entities attribute is not None or empty, the method returns the cached
    entities list and does not submit any POST request to the server.
    """

    cached_entities = CameEntitySet(
        [
            Light(1),
            Light(2),
            Opening(3),
            Scenario(4),
        ]
    )
    mocked_server_auth._entities = cached_entities

    # Call the get_features method
    with pytest.raises(TypeError):
        mocked_server_auth.get_entities("invalid_type")

    # Emulate logout, to neutralize the call to the dispose() method
    # that would fail since it would try to call the remote server
    mocked_server_auth._session_id = ""


# Test the set_entity_status method
@patch.object(requests.Session, "post")
def test_set_entity_status(mock_post, mocked_server_auth):
    """
    Test that failures are managed as expected.
    """

    # Create a mock response with status code 200 and some data
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = GENERIC_REPLY

    mock_post.return_value = mock_response

    # Call the set_entity_status method
    result = mocked_server_auth.set_entity_status(
        Light, 1, EntityStatus.ON_OPEN_TRIGGERED
    )

    # Check if the post method was called
    mock_post.assert_called_once()
    assert result

    # Emulate logout, to neutralize the call to the dispose() method
    # that would fail since it would try to call the remote server
    mocked_server_auth._session_id = ""


# Test the set_entity_status method when http response has wrong format or there's an http error
@patch.object(requests.Session, "post")
def test_set_entity_status_errors(mock_post, mocked_server_auth):
    """
    Test that failures are managed as expected.
    """

    # Test bad ack
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = copy.deepcopy(GENERIC_REPLY)
    mock_response.json.return_value["sl_data_ack_reason"] = 1
    mock_post.return_value = mock_response
    assert not mocked_server_auth.set_entity_status(
        Light, 1, EntityStatus.ON_OPEN_TRIGGERED
    )
    mock_post.assert_called_once()

    # Test HTTP error
    mock_post.return_value.status_code = 500
    assert not mocked_server_auth.set_entity_status(
        Light, 1, EntityStatus.ON_OPEN_TRIGGERED
    )

    # Test invalid response
    mock_post.return_value.status_code = 200
    mock_post.return_value = {"invalid_key": "invalid_value"}
    assert not mocked_server_auth.set_entity_status(
        Light, 1, EntityStatus.ON_OPEN_TRIGGERED
    )

    # Emulate logout, to neutralize the call to the dispose() method
    # that would fail since it would try to call the remote server
    mocked_server_auth._session_id = ""


# Test the set_entity_status method when the input is invalid
def test_set_entity_status_invalid_inputs(mocked_server_auth):
    """
    Test that failures are managed as expected.
    """
    # Test invalid input
    with pytest.raises(TypeError):
        mocked_server_auth.set_entity_status(
            "invalid_type", 1, EntityStatus.OFF_STOPPED
        )

    with pytest.raises(TypeError):
        mocked_server_auth.set_entity_status(
            Light, "invalid_id", EntityStatus.OFF_STOPPED
        )

    with pytest.raises(TypeError):
        mocked_server_auth.set_entity_status(Light, 1, "invalid_status")

    with pytest.raises(TypeError):
        mocked_server_auth.set_entity_status(
            Light, 1, EntityStatus.OFF_STOPPED, brightness="invalid_brightness"
        )

    # Emulate logout, to neutralize the call to the dispose() method
    # that would fail since it would try to call the remote server
    mocked_server_auth._session_id = ""


# @patch.object(CameETIDomoServer, "_fetch_entities_list")
# def test_get_entities_no_cache(mock_fetch_entities, mocked_server_auth):
#     """
#     Test if the get_entities method correctly fetches the entities list when it is not cached.
#     """
#     # Clear the entities cache
#     mocked_server_auth._entities = None

#     # Call the get_entities method
#     entities = mocked_server_auth.get_entities()

#     # Check if the _fetch_entities_list method was called
#     mock_fetch_entities.assert_called_once()

#     # Check if the entities list is correct
#     # Replace ENTITY_LIST_RESP with the expected entities list
#     assert entities == ENTITY_LIST_RESP

#     # Emulate logout, to neutralize the call to the dispose() method
#     # that would fail since it would try to call the remote server
#     mocked_server_auth._session_id = ""


# @patch.object(CameETIDomoServer, "_fetch_entities_list")
# def test_get_entities_with_cache(mock_fetch_entities, mocked_server_auth):
#     """
#     Test if the get_entities method correctly returns the cached entities list.
#     """
#     # Set the entities cache
#     # Replace ENTITY_LIST_RESP with the expected entities list
#     mocked_server_auth._entities = ENTITY_LIST_RESP

#     # Call the get_entities method
#     entities = mocked_server_auth.get_entities()

#     # Check if the _fetch_entities_list method was not called
#     mock_fetch_entities.assert_not_called()

#     # Check if the entities list is correct
#     assert entities == ENTITY_LIST_RESP

#     # Emulate logout, to neutralize the call to the dispose() method
#     # that would fail since it would try to call the remote server
#     mocked_server_auth._session_id = ""


# @patch.object(CameETIDomoServer, "_fetch_entities_list")
# def test_get_entities_with_filter(mock_fetch_entities, mocked_server_auth):
#     """
#     Test if the get_entities method correctly filters the entities by type.
#     """
#     # Set the entities cache
#     # Replace ENTITY_LIST_RESP with the expected entities list
#     mocked_server_auth._entities = ENTITY_LIST_RESP

#     # Call the get_entities method with a filter
#     # Replace EntityType.SOME_TYPE with the entity type to filter by
#     entities = mocked_server_auth.get_entities(EntityType.SOME_TYPE)

#     # Check if the _fetch_entities_list method was not called
#     mock_fetch_entities.assert_not_called()

#     # Check if the entities list is correct
#     # Replace FILTERED_ENTITY_LIST_RESP with the expected filtered entities list
#     assert entities == FILTERED_ENTITY_LIST_RESP

#     # Emulate logout, to neutralize the call to the dispose() method
#     # that would fail since it would try to call the remote server
#     mocked_server_auth._session_id = ""

# endregion
