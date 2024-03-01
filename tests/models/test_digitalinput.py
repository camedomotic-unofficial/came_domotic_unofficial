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
Unit tests for the DigitalInput class.
"""

from datetime import datetime, UTC
import pytest
from hypothesis import given
from hypothesis.strategies import integers, text, sampled_from
from came_domotic_unofficial.models import (
    CameEntity,
    DigitalInputType,
    DigitalInput,
    EntityStatus,
)


@given(
    entity_id=integers(min_value=1),
    name=text(min_size=1),
    button_type=sampled_from(DigitalInputType),
    address=integers(),
    ack_code=integers(),
    radio_node_id=text(min_size=1),
    rf_radio_link_quality=integers(),
    utc_time=integers(min_value=0, max_value=int(datetime.now().timestamp())),
)
def test_digital_input_init(
    entity_id,
    name,
    button_type,
    address,
    ack_code,
    radio_node_id,
    rf_radio_link_quality,
    utc_time,
):
    """
    Test if the DigitalInput constructor works correctly.
    """
    digital_input = DigitalInput(
        entity_id,
        name,
        button_type=button_type,
        address=address,
        ack_code=ack_code,
        radio_node_id=radio_node_id,
        rf_radio_link_quality=rf_radio_link_quality,
        utc_time=utc_time,
    )

    assert isinstance(digital_input, CameEntity)
    assert digital_input.id == entity_id
    assert digital_input.name == name
    assert digital_input.button_type == button_type
    assert digital_input.address == address
    assert digital_input.ack_code == ack_code
    assert digital_input.radio_node_id == radio_node_id
    assert digital_input.rf_radio_link_quality == rf_radio_link_quality
    assert digital_input.last_pressed == datetime.fromtimestamp(utc_time, UTC)
    assert digital_input.status == EntityStatus.NOT_APPLICABLE


def test_digital_input_init_defaults():
    """
    Test if the DigitalInput constructor works correctly with default values.
    """
    digital_input = DigitalInput(1)

    assert digital_input.id == 1
    assert digital_input.name == "Unknown"
    assert digital_input.button_type == DigitalInputType.BUTTON
    assert digital_input.address == 0
    assert digital_input.ack_code == 1
    assert digital_input.radio_node_id == "00000000"
    assert digital_input.rf_radio_link_quality == 0
    assert digital_input.last_pressed == datetime.fromtimestamp(0, UTC)
    assert digital_input.status == EntityStatus.NOT_APPLICABLE


def tests_digital_input_init_invalid_button_type():
    """
    Test if the DigitalInput constructor raises an error with an invalid button
    """
    with pytest.raises(TypeError):
        DigitalInput(1, button_type="Invalid")


def test_digital_input_init_invalid_address():
    """
    Test if the DigitalInput constructor raises an error
    with an invalid address
    """
    with pytest.raises(TypeError):
        DigitalInput(1, address="Invalid")


def test_digital_input_init_invalid_ack_code():
    """
    Test if the DigitalInput constructor raises an error with an invalid ack
    """
    with pytest.raises(TypeError):
        DigitalInput(1, ack_code="Invalid")


def test_digital_input_init_invalid_radio_node_id():
    """
    Test if the DigitalInput constructor raises an error with an invalid radio
    """
    with pytest.raises(TypeError):
        DigitalInput(1, radio_node_id=1)


def test_digital_input_init_invalid_rf_radio_link_quality():
    """
    Test if the DigitalInput constructor raises an error with an invalid RF
    """
    with pytest.raises(TypeError):
        DigitalInput(1, rf_radio_link_quality="Invalid")


def test_digital_input_init_invalid_utc_time():
    """
    Test if the DigitalInput constructor raises an error with an invalid UTC
    """
    with pytest.raises(TypeError):
        DigitalInput(1, utc_time="Invalid")


def test_digital_input_str_method():
    """
    Test if the DigitalInput __str__ method works correctly.
    """
    digital_input = DigitalInput(
        1,
        "Test Digital Input",
        button_type=DigitalInputType.BUTTON,
        address=2,
        ack_code=3,
        radio_node_id="Test",
        rf_radio_link_quality=4,
        utc_time=5,
    )
    assert str(digital_input) == (
        'DigitalInput #1: "Test Digital Input" - Type: BUTTON - '
        'Address: 2 - Ack code: 3 - Radio node ID: "Test" - '
        "RF radio link quality: 4 - Last pressed: "
        f"{datetime.fromtimestamp(5, UTC)}"
    )


def test_digital_input_repr_method():
    """
    Test if the DigitalInput __repr__ method works correctly.
    """
    digital_input = DigitalInput(
        1,
        "Test Digital Input",
        button_type=DigitalInputType.BUTTON,
        address=2,
        ack_code=3,
        radio_node_id="Test",
        rf_radio_link_quality=4,
        utc_time=5,
    )
    assert repr(digital_input) == (
        'DigitalInput(1,"Test Digital Input",'
        "button_type=DigitalInputType.BUTTON,address=2,ack_code=3,"
        'radio_node_id="Test",rf_radio_link_quality=4,utc_time=5)'
    )


def test_digitalinput_equality_hash_operators():
    """
    Test if the DigitalInput equality and hash operators work correctly.
    """
    entity_name = "Test"
    entity1 = DigitalInput(1, entity_name)
    entity2 = DigitalInput(1, entity_name)
    entity3 = DigitalInput(1, entity_name, address=0)
    entity4 = DigitalInput(2, entity_name)
    entity5 = DigitalInput(1, entity_name + "_")
    entity6 = DigitalInput(1, entity_name, address=1)
    other_type1 = CameEntity(1, entity_name, status=EntityStatus.NOT_APPLICABLE)
    other_type2 = repr(entity1)
    other_type3 = entity_name

    assert entity1 == entity2
    assert entity1 == entity3
    assert entity1 != entity4
    assert entity1 != entity5
    assert entity1 != entity6
    assert entity1 != other_type1
    assert entity1 != other_type2
    assert entity1 != other_type3

    assert hash(entity1) == hash(entity2)
    assert hash(entity1) == hash(entity3)
    assert hash(entity1) != hash(entity4)
    assert hash(entity1) != hash(entity5)
    assert hash(entity1) != hash(entity6)
    assert hash(entity1) != hash(other_type1)
    assert hash(entity1) != hash(other_type2)
    assert hash(entity1) != hash(other_type3)


def test_digital_input_from_json():
    """
    Test if the DigitalInput from_json method works correctly.
    """
    json_data = {
        "name": "Test",
        "act_id": 11,
        "type": 1,
        "addr": 0,
        "ack": 1,
        "radio_node_id": "00000000",
        "rf_radio_link_quality": 0,
        "utc_time": 0,
    }
    digital_input = DigitalInput.from_json(json_data)

    assert digital_input.id == 11
    assert digital_input.name == "Test"
    assert digital_input.button_type == DigitalInputType(1)
    assert digital_input.address == 0
    assert digital_input.ack_code == 1
    assert digital_input.radio_node_id == "00000000"
    assert digital_input.rf_radio_link_quality == 0
    assert digital_input.last_pressed == datetime.fromtimestamp(0, UTC)


def test_digital_input_from_json_defaults():
    """
    Test if the DigitalInput from_json method works correctly when
    optional keys are missing.
    """
    json_data = {
        "act_id": 1,
    }
    digital_input = DigitalInput.from_json(json_data)
    check = DigitalInput(1)

    assert digital_input == check


def test_digital_input_from_json_invalid_values():
    """
    Test if the DigitalInput from_json method works correctly.
    """
    json_data = {
        "act_id": 1,
        "name": "Test",
        "type": "Invalid",
        "addr": "Invalid",
        "ack": "Invalid",
        "radio_node_id": 1,
        "rf_radio_link_quality": "Invalid",
        "utc_time": "Invalid",
    }
    digital_input = DigitalInput.from_json(json_data)
    check = DigitalInput(1, "Test")

    assert digital_input == check


def test_digital_input_from_json_missing_required_keys():
    """
    Test if the DigitalInput from_json method raises an exception when the id
    is missing.
    """

    json_data = {
        "name": "Test",
        "type": 1,
        "addr": 0,
        "ack": 1,
        "radio_node_id": "00000000",
        "rf_radio_link_quality": 0,
        "utc_time": 0,
    }
    with pytest.raises(KeyError):
        DigitalInput.from_json(json_data)


def test_digital_input_from_json_unexpected_properties():
    """
    Test if the DigitalInput from_json method works correctly.
    """
    json_data = {
        "act_id": 1,
        "name": "Test",
        "type": 1,
        "addr": 0,
        "ack": 1,
        "radio_node_id": "00000000",
        "rf_radio_link_quality": 0,
        "utc_time": 0,
        "unexpected": "unexpected",
    }
    digital_input = DigitalInput.from_json(json_data)
    check = DigitalInput(
        1,
        "Test",
        button_type=DigitalInputType(1),
        address=0,
        ack_code=1,
        radio_node_id="00000000",
        rf_radio_link_quality=0,
        utc_time=0,
    )

    assert digital_input == check
