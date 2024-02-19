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
Unit tests for the Light class.
"""

import pytest
from hypothesis import given
from hypothesis.strategies import integers, text, sampled_from
from came_domotic_unofficial.models import (
    CameEntity,
    Light,
    EntityStatus,
    LightType,
)


@given(
    entity_id=integers(),
    name=text(min_size=1),
    status=sampled_from(EntityStatus),
    light_type=sampled_from(LightType),
    brightness=integers(),
)
def test_light_constructor(entity_id, name, status, light_type, brightness):
    """
    Test if the Light constructor works correctly.
    """
    light = Light(
        entity_id,
        name,
        status=status,
        light_type=light_type,
        brightness=brightness,
    )

    assert isinstance(light, CameEntity)
    assert light.id == entity_id
    assert light.name == name
    assert light.status == status
    assert light.light_type == light_type
    assert light.brightness == min(max(0, brightness), 100)


def test_light_constructor_defaults():
    """
    Test if the Light constructor works correctly with default values.
    """
    light = Light(1)

    assert light.id == 1
    assert light.name == "Unknown"
    assert light.status == EntityStatus.UNKNOWN
    assert light.light_type == LightType.ON_OFF
    assert light.brightness == 100


def test_light_constructor_invalid_light_type():
    """
    Test if the Light constructor raises an error with an invalid light type.
    """
    with pytest.raises(TypeError) as exc_info:
        Light(1, "Test Light", light_type="Not a valid light type")

    assert str(exc_info.value) == "The light type must be a valid LightType"


def test_light_constructor_invalid_brightness():
    """
    Test if the Light constructor raises an error with an invalid brightness.
    """
    with pytest.raises(TypeError) as exc_info:
        Light(1, "Test Light", brightness="Invalid brightness")

    assert str(exc_info.value) == "The brightness value must be an integer"


def test_light_brightness_property():
    """
    Test if the Light brightness property works correctly.
    """
    light = Light(1, brightness=50)

    with pytest.raises(ValueError):
        light.brightness = -1

    with pytest.raises(ValueError):
        light.brightness = 101

    light.brightness = 0
    assert light.brightness == 0

    light.brightness = 100
    assert light.brightness == 100


def test_light_str_method():
    """
    Test if the Light __str__ method works correctly.
    """
    light = Light(
        1,
        "Test Light",
        status=EntityStatus.ON_OPEN,
        light_type=LightType.DIMMABLE,
        brightness=50,
    )

    assert str(light) == (
        "Light #1: Test Light - Type: (DIMMABLE) - "
        "Status: ON_OPEN - Brightness: 50"
    )


def test_light_repr_method():
    """
    Test if the Light __repr__ method works correctly.
    """
    light = Light(
        1,
        "Test Light",
        status=EntityStatus.ON_OPEN,
        light_type=LightType.DIMMABLE,
        brightness=50,
    )

    assert repr(light) == (
        'Light(1,"Test Light",status=EntityStatus.ON_OPEN,'
        "light_type=LightType.DIMMABLE,brightness=50)"
    )


def test_light_equality_hash_operators():
    """
    Test if the Light equality and hash operators work correctly.
    """
    light_name = "Test light"
    light1 = Light(1, light_name)
    light2 = Light(1, light_name)
    light3 = Light(1, light_name, status=EntityStatus.UNKNOWN)
    light4 = Light(2, light_name, status=EntityStatus.UNKNOWN)
    light5 = Light(1, light_name + "_", status=EntityStatus.UNKNOWN)
    light6 = Light(1, light_name, status=EntityStatus.ON_OPEN)
    other_type1 = CameEntity(1, light_name, status=EntityStatus.UNKNOWN)
    other_type2 = repr(light1)
    other_type3 = light_name

    assert light1 == light2
    assert light1 == light3
    assert light1 != light4
    assert light1 != light5
    assert light1 != light6
    assert light1 != other_type1
    assert light1 != other_type2
    assert light1 != other_type3
    assert hash(light1) == hash(light2)
    assert hash(light1) == hash(light3)
    assert hash(light1) != hash(light4)
    assert hash(light1) != hash(light5)
    assert hash(light1) != hash(light6)
    assert hash(light1) != hash(other_type1)
    assert hash(light1) != hash(other_type2)
    assert hash(light1) != hash(other_type3)


@given(
    entity_id=integers(),
    name=text(min_size=1),
    status=integers(min_value=0, max_value=2),
    light_type=sampled_from(["STEP_STEP", "DIMMER"]),
    brightness=integers(min_value=0, max_value=100),
)
def test_light_from_json_method(
    entity_id, name, status, light_type, brightness
):
    """
    Test if the Light from_json method works correctly.
    """

    json_data = {
        "act_id": entity_id,
        "name": name,
        "status": status,
        "type": light_type,
        "perc": brightness,
    }
    light = Light.from_json(json_data)

    assert light.id == entity_id
    assert light.name == name
    assert light.status == EntityStatus(status)

    assert light.light_type == LightType(light_type)
    assert light.brightness == brightness


def test_light_from_json_method_defaults():
    """
    Test if the Light from_json method works correctly when optional keys
    are missing.
    """

    json_data = {
        "act_id": 1,
    }
    light = Light.from_json(json_data)
    check_light = Light(1)

    assert light == check_light


def test_light_from_json_method_missing_required_keys():
    """
    Test if the Light from_json method raises an exception when the id
    is missing.
    """

    json_data = {
        "name": "Test",
        "status": 0,
        "type": "DIMMER",
        "perc": 100,
    }
    with pytest.raises(KeyError):
        Light.from_json(json_data)


@given(
    status=integers(min_value=100),
    light_type=text(min_size=1),
)
def test_light_from_json_unknown_status_and_light_type(status, light_type):
    """
    Test if the Light from_json method works correctly.
    """

    json_data = {
        "act_id": 1,
        "name": "Test",
        "status": status,
        "type": light_type,
    }
    light = Light.from_json(json_data)
    check_light = Light(1, "Test")

    assert light == check_light


def test_light_from_json_invalid_values():
    """
    Test if the Light from_json method raises an exception when the JSON
    data contains invalid values.
    """

    json_data = {
        "act_id": 1,  # Should be an integer
        "name": "Test",
        "status": "unexpected",  # Should be an EntityStatus value
        "type": "invalid",  # Should be a LightType value
        "perc": "unexpected",  # Should be an integer
    }
    light = Light.from_json(json_data)
    check_light = Light(1, "Test")

    assert light == check_light


def test_light_from_json_out_of_range_brightness():
    """
    Test if the Light from_json method works correctly.
    """

    json_data1 = {
        "act_id": 1,
        "type": "DIMMER",
        "perc": -1,
    }
    json_data2 = {
        "act_id": 1,
        "type": "DIMMER",
        "perc": 101,
    }
    light1 = Light.from_json(json_data1)
    light2 = Light.from_json(json_data2)

    assert light1.brightness == 0
    assert light2.brightness == 100


def test_light_from_json_method_unexpected_properties():
    """
    Test if the Light from_json method works correctly.
    """

    json_data = {
        "act_id": 1,
        "name": "Test",
        "status": 0,
        "type": "DIMMER",
        "perc": 50,
        "my_unexpected_key": "unexpected",
    }
    light = Light.from_json(json_data)
    check_light = Light(
        1,
        "Test",
        status=EntityStatus(0),
        light_type=LightType("DIMMER"),
        brightness=50,
    )

    assert light == check_light
