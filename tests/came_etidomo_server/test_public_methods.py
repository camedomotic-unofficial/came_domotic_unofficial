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
from datetime import datetime, timezone, timedelta
import json
from unittest.mock import patch, Mock
import freezegun
import pytest
import requests
from mocked_responses import (
    FEATURE_LIST_RESP,
    GENERIC_REPLY,
    SL_LOGOUT_ACK,
    SL_KEEP_ALIVE_ACK,
    Command2MockedResponse,
    MockedEntities,
)
from utils import (
    mock_get_init,
    mock_post_method,
    mock_post_method_error_auth,
    mock_post_method_error_non_auth,
)
from came_domotic_unofficial.came_etidomo_server import CameETIDomoServer
from came_domotic_unofficial.models import (
    FeatureSet,
    Feature,
    CameEntitySet,
    CameEntity,
    Light,
    Opening,
    Scenario,
    EntityType,
    EntityStatus,
    CameDomoticRequestError,
    CameDomoticBadAckError,
)


# region Tests


@pytest.fixture
@patch("requests.Session.get", side_effect=mock_get_init)
def mocked_server_auth(mock_get) -> CameETIDomoServer:
    """
    Fixture that provides an authenticated instance of CameETIDomoServer.
    """
    server = CameETIDomoServer("192.168.0.3", "user", "password")
    # Override the dispose() method to avoid calling the remote server
    server.dispose = lambda: None  # type: ignore # pylint: disable=pointless-statement

    # Manually set session attributes to emulate the authentication
    server._session_id = "my_session_id"
    server._session_expiration_timestamp = datetime(3000, 1, 1, tzinfo=timezone.utc)
    server._session_keep_alive_timeout_sec = 900
    server._cseq = 0

    return server


@patch("requests.Session.post", side_effect=mock_post_method)
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


@patch("requests.Session.post", side_effect=mock_post_method)
def test_get_features_no_cache(mock_post, mocked_server_auth):
    """
    Test if the get_features method correctly fetches the features list
    when it is not cached.
    """
    mock_features = set([Feature(name) for name in FEATURE_LIST_RESP["list"]])

    # Call the get_features method
    features = mocked_server_auth.get_features()
    assert mock_post.call_count == 1
    assert features == mock_features

    # Clear the features cache
    mocked_server_auth._features = FeatureSet()

    # Call the get_features method
    features = mocked_server_auth.get_features()
    assert mock_post.call_count == 2
    assert features == mock_features


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
    mock_response.json.return_value = copy.deepcopy(
        GENERIC_REPLY  # Don't want to write on the original object
    )
    mock_response.json.return_value["sl_data_ack_reason"] = 1
    mock_post.return_value = mock_response

    with pytest.raises(CameDomoticBadAckError):
        # Call the function that sends the POST requests
        mocked_server_auth.get_features()


@patch("requests.Session.post", side_effect=mock_post_method)
def test_get_features_request(mock_post, mocked_server_auth):
    """
    Test if the get_features method sends a POST message compliant with the
    CAME server interface.
    """

    # Call the get_features method
    mocked_server_auth.get_features()

    request_data = json.loads(mock_post.call_args[1]["data"]["command"])
    application_data = request_data["sl_appl_msg"]

    expected_request_data = {
        "sl_client_id": "my_session_id",
        "sl_cmd": "sl_data_req",
    }
    expected_application_data = {
        "client": "my_session_id",
        "cmd_name": "feature_list_req",
    }

    assert set(expected_request_data).issubset(set(request_data))
    assert set(expected_application_data).issubset(set(application_data))


@patch("requests.Session.post", side_effect=mock_post_method)
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


@patch("requests.Session.post", side_effect=mock_post_method)
def test_get_entities_no_cache(mock_post, mocked_server_auth):
    """
    Test that an HTTP POST request returns the expected data.
    """
    entities = mocked_server_auth.get_entities()
    assert entities == MockedEntities
    assert mock_post.call_count > 0


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
    mock_response.json.return_value = copy.deepcopy(
        GENERIC_REPLY  # Don't want to write on the original object
    )
    mock_response.json.return_value["sl_data_ack_reason"] = 1
    mock_post.return_value = mock_response

    with pytest.raises(CameDomoticBadAckError):
        # Call the function that sends the POST requests
        mocked_server_auth.get_entities()


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


def test_get_entities_filtered_invalid_input(mocked_server_auth):
    """
    Test the get_entities() method ot the CameETIDomoServer class to ensure that,
    if the self._entities attribute is not None or empty, the method returns the cached
    entities list and does not submit any POST request to the server.
    """

    # Call the get_features method
    with pytest.raises(TypeError):
        mocked_server_auth.get_entities("invalid_type")


@patch.object(requests.Session, "post")
def test_get_entities_request(mock_post, mocked_server_auth):
    """
    Test if the get_entities method sends a POST message compliant with the
    CAME server interface.
    """
    pass  # TODO implement actual checks on request format


# Test the set_entity_status method
@patch("requests.Session.post", side_effect=mock_post_method)
def test_set_entity_status(mock_post, mocked_server_auth):
    """
    Test that failures are managed as expected.
    """
    # Call the set_entity_status method
    result = mocked_server_auth.set_entity_status(
        Light, 1, EntityStatus.ON_OPEN_TRIGGERED
    )

    # Check if the post method was called
    mock_post.assert_called_once()
    assert result


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


@patch("requests.Session.post", side_effect=mock_post_method)
def test_set_entity_status_request_light(mock_post, mocked_server_auth):
    """
    Test that the POST request is compliant with the CAME server interface.
    """
    # Call the set_entity_status method
    mocked_server_auth.set_entity_status(
        Light,
        999,
        EntityStatus.ON_OPEN_TRIGGERED,
        brightness=87,
    )

    request_data = json.loads(mock_post.call_args[1]["data"]["command"])
    application_data = request_data["sl_appl_msg"]

    expected_request_data = {
        "sl_client_id": "my_session_id",
        "sl_cmd": "sl_data_req",
    }
    expected_application_data = {
        "act_id": 999,
        "client": "my_session_id",
        "cmd_name": "light_switch_req",
        "wanted_status": EntityStatus.ON_OPEN_TRIGGERED.value,
        "perc": 87,
    }

    assert set(expected_request_data).issubset(set(request_data))
    assert set(expected_application_data).issubset(set(application_data))


@patch("requests.Session.post", side_effect=mock_post_method)
def test_set_entity_status_request_opening(mock_post, mocked_server_auth):
    """
    Test that the POST request is compliant with the CAME server interface.
    """
    # Call the set_entity_status method
    mocked_server_auth.set_entity_status(
        Opening,
        999,
        EntityStatus.ON_OPEN_TRIGGERED,
    )

    request_data = json.loads(mock_post.call_args[1]["data"]["command"])
    application_data = request_data["sl_appl_msg"]

    expected_request_data = {
        "sl_client_id": "my_session_id",
        "sl_cmd": "sl_data_req",
    }
    expected_application_data = {
        "act_id": 999,
        "client": "my_session_id",
        "cmd_name": "opening_move_req",
        "wanted_status": EntityStatus.ON_OPEN_TRIGGERED.value,
    }

    assert set(expected_request_data).issubset(set(request_data))
    assert set(expected_application_data).issubset(set(application_data))


@patch("requests.Session.post", side_effect=mock_post_method)
def test_set_entity_status_request_scenario(mock_post, mocked_server_auth):
    """
    Test that the POST request is compliant with the CAME server interface.
    """
    # Call the set_entity_status method
    mocked_server_auth.set_entity_status(
        Scenario,
        999,
        EntityStatus.ON_OPEN_TRIGGERED,
    )

    request_data = json.loads(mock_post.call_args[1]["data"]["command"])
    application_data = request_data["sl_appl_msg"]

    expected_request_data = {
        "sl_client_id": "my_session_id",
        "sl_cmd": "sl_data_req",
    }
    expected_application_data = {
        "id": 999,
        "client": "my_session_id",
        "cmd_name": "opening_move_req",
    }

    assert set(expected_request_data).issubset(set(request_data))
    assert set(expected_application_data).issubset(set(application_data))


@patch("requests.Session.get", side_effect=mock_get_init)
@patch.object(requests.Session, "close")
def test_dispose_close_http_session(mock_close, mock_get):
    """
    Test that the dispose method closes the http session.
    """
    server = CameETIDomoServer("192.168.0.3", "user", "password")

    # Call the dispose method
    server.dispose()
    mock_close.assert_called_once()


@patch("requests.Session.get", side_effect=mock_get_init)
@patch("requests.Session.post", side_effect=requests.exceptions.RequestException)
@patch.object(requests.Session, "close")
def test_dispose_post_with_exception(mock_close, mock_post, mock_get):
    """
    Test that the dispose method closes the http session even if an exception is raised
    while sending the logout POST request.
    """
    server = CameETIDomoServer("192.168.0.3", "user", "password")
    server._session_id = "my_session_id"
    server._session_expiration_timestamp = datetime(3000, 1, 1, tzinfo=timezone.utc)

    # Call the dispose method
    server.dispose()
    assert mock_close.call_count >= 1

    # Trick to kill some sort of circular reference happening at the end of this test
    server.dispose = lambda: None  # type: ignore


@patch("requests.Session.get", side_effect=mock_get_init)
@patch("requests.Session.post", side_effect=mock_post_method)
def test_dispose_post_request(mock_post, mock_get):
    """
    Test that the dispose method sends a POST request to the server
    and that the request is compliant with the CAME server interface.
    """
    server = CameETIDomoServer("192.168.0.3", "user", "password")
    server._session_id = "my_session_id"
    server._session_expiration_timestamp = datetime(3000, 1, 1, tzinfo=timezone.utc)

    # Call the dispose method
    server.dispose()

    request_data = json.loads(mock_post.call_args[1]["data"]["command"])

    expected_request_data = {"sl_client_id": "my_session_id", "sl_cmd": "sl_logout_req"}

    mock_post.assert_called_once()
    assert set(expected_request_data).issubset(set(request_data))


@freezegun.freeze_time("2020-01-01")
@patch("requests.Session.post", side_effect=mock_post_method)
def test_keep_alive_success(mock_post, mocked_server_auth):
    """
    Test that the keep_alive method returns True when the server responds with a
    status code of 200 and the expected data.
    """
    # Set the session expiration timestamp to a value close to now
    mocked_server_auth._session_expiration_timestamp = datetime.now(
        timezone.utc
    ) + timedelta(seconds=30)

    # Call the set_entity_status method
    successful = mocked_server_auth.keep_alive()

    # Check if the post method was called and the session expiration have been
    # extended as expected
    mock_post.assert_called_once()
    assert successful
    assert mocked_server_auth._session_expiration_timestamp == datetime.now(
        timezone.utc
    ) + timedelta(seconds=mocked_server_auth._session_keep_alive_timeout_sec)


@patch("requests.Session.post")
def test_keep_alive_bad_ack(mock_post, mocked_server_auth):
    """
    Test that the keep_alive method returns False when the server responds with a
    non-zero ack code.
    """
    # Create a mock response with status code 200 and some data
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = copy.deepcopy(SL_KEEP_ALIVE_ACK)
    mock_response.json.return_value["sl_data_ack_reason"] = 1

    mock_post.return_value = mock_response

    # Call the set_entity_status method
    successful = mocked_server_auth.keep_alive()

    # Check if the post method was called
    mock_post.assert_called_once()
    assert not successful


@patch.object(requests.Session, "post")
def test_keep_alive_exceptions(mock_post, mocked_server_auth):
    """
    Test that the keep_alive method returns False when the server responds with a
    non-zero ack code.
    """
    # Create a mock response with status code 200 and some data
    mock_post.side_effect = CameDomoticRequestError()

    # Call the set_entity_status method
    successful = mocked_server_auth.keep_alive()
    mock_post.assert_called_once()
    assert not successful

    # Create a mock response with status code 200 and some data
    mock_post.side_effect = requests.exceptions.RequestException()

    # Call the set_entity_status method
    successful = mocked_server_auth.keep_alive()
    assert mock_post.call_count == 2
    assert not successful


@patch("requests.Session.post", side_effect=mock_post_method)
def test_keep_alive_request(mock_post, mocked_server_auth):
    """
    Test that the POST request is compliant with the CAME server interface.
    """
    # Call the set_entity_status method
    mocked_server_auth.keep_alive()

    request_data = json.loads(mock_post.call_args[1]["data"]["command"])

    expected_request_data = {
        "sl_client_id": "my_session_id",
        "sl_cmd": "sl_keep_alive_req",
    }

    assert set(expected_request_data).issubset(set(request_data))


# endregion
