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
Tests for all the CAME Domotic entities.
"""

import pytest
from hypothesis import given
from hypothesis.strategies import integers, text, sampled_from, lists
from came_domotic_unofficial.models import (
    CameEntitiesSet,
    CameEntity,
    Feature,
    Light,
    EntityStatus,
    LightType,
    Opening,
    OpeningType,
)

# region CameEntity


@given(
    input_id=integers(min_value=1),
    input_name=text(min_size=5, max_size=20),
    input_status=sampled_from(EntityStatus),
    input_status_new=sampled_from(EntityStatus),
)
def test_came_entity_initialization(
    input_id, input_name, input_status, input_status_new
):
    """
    Test the initialization and the properties of the CameEntity class.
    """
    entity = CameEntity(input_id, input_name, status=input_status)

    assert entity.id == input_id
    assert entity.name == input_name
    assert entity.status == input_status
    assert entity.type == CameEntity

    # Test changing status
    entity.status = input_status_new
    assert entity.status == input_status_new


@given(
    input_id=integers(min_value=1),
    input_name=text(min_size=5, max_size=20),
    input_status=sampled_from(EntityStatus),
)
def test_came_entity_initialization_no_status(
    input_id, input_name, input_status
):
    """
    Test the initialization and the properties of the CameEntity class
    when the status is not provided.
    """
    entity = CameEntity(input_id, input_name)

    assert entity.id == input_id
    assert entity.name == input_name
    assert entity.status is None
    assert entity.type == CameEntity

    # Test changing status
    entity.status = input_status
    assert entity.status == input_status


@given(
    input_status=sampled_from(EntityStatus),
)
def test_came_entity_initialization_no_name(input_status):
    """
    Test the initialization of the CameEntity class
    when the name is not provided.
    """
    entity = CameEntity(1, status=input_status)

    assert entity.id == 1
    assert entity.name == "Unknown"
    assert entity.status is input_status
    assert entity.type == CameEntity


def test_came_entity_initialization_no_name_nor_status():
    """
    Test the initialization of the CameEntity class
    when the name and status are not provided.
    """
    entity = CameEntity(1)

    assert entity.id == 1
    assert entity.name == "Unknown"
    assert entity.status is None
    assert entity.type == CameEntity

    # Test assigning status
    entity.status = EntityStatus.OFF_CLOSED
    assert entity.status == EntityStatus.OFF_CLOSED


@given(
    input_id1=integers(min_value=1, max_value=50),
    input_id2=integers(min_value=51),
)
def test_came_entity_equality(input_id1, input_id2):
    """
    Test the equality and inequality methods of the CameEntity class.
    """
    entity1 = CameEntity(input_id1, name="Test 1")
    entity2 = CameEntity(input_id1, name="Test 2")
    entity3 = CameEntity(input_id2, name="Test 3")

    assert entity1 == entity2
    assert entity1 != entity3


@given(
    input_id1=integers(min_value=1, max_value=50),
    input_id2=integers(min_value=51),
)
def test_came_entity_hash(input_id1, input_id2):
    """
    Test the __hash__ method of the CameEntity class.
    """
    entity1 = CameEntity(input_id1, name="Test 1")
    entity2 = CameEntity(input_id1, name="Test 2")
    entity3 = CameEntity(input_id2, name="Test 3")

    assert hash(entity1) == hash((CameEntity, input_id1))
    assert hash(entity1) == hash(entity2)
    assert hash(entity1) != hash(entity3)


# endregion

# region CameEntitiesSet


def test_came_entities_set_initialization():
    """
    Test the initialization of the CameEntitiesSet class.
    """
    entities_set = CameEntitiesSet()

    assert isinstance(entities_set, set)
    assert len(entities_set) == 0


def test_came_entities_set_add():
    """
    Test the add method of the CameEntitiesSet class.
    """
    entities_set = CameEntitiesSet()
    entity = CameEntity(
        entity_id=1, name="Test Entity", status=EntityStatus.ON_OPEN
    )

    entities_set.add(entity)

    assert len(entities_set) == 1
    assert entity in entities_set


def test_came_entities_set_add_type_check():
    """
    Test the type checking in the add method of the CameEntitiesSet class.
    """
    entities_set = CameEntitiesSet()

    with pytest.raises(TypeError):
        entities_set.add("Not a CameEntity")


# endregion

# region Feature


@given(
    input_name=text(min_size=5, max_size=20),
)
def test_feature_initialization(input_name):
    """
    Test the initialization of the Feature class.
    """
    feature = Feature(input_name)

    assert feature.id == hash(input_name)
    assert feature.name == input_name
    assert feature.type == Feature


# endregion

# region Light


@given(
    input_id=integers(min_value=1),
    input_name=text(min_size=5, max_size=20),
    input_status=sampled_from(EntityStatus),
    input_brightness=integers(min_value=0, max_value=100),
    input_brightness_new=integers(min_value=0, max_value=100),
)
def test_light_initialization(
    input_id, input_name, input_status, input_brightness, input_brightness_new
):
    """
    Test the initialization of the Light class.
    """
    light = Light(
        input_id,
        input_name,
        status=input_status,
        light_type=LightType.DIMMABLE,
        brightness=input_brightness,
    )

    assert light.id == input_id
    assert light.name == input_name
    assert light.status == input_status
    assert light.light_type == LightType.DIMMABLE
    assert light.brightness == input_brightness
    assert light.type == Light

    # Test properties
    light.brightness = input_brightness_new
    assert light.brightness == input_brightness_new


@given(
    input_brightness_low=integers(max_value=-1),
    input_brightness_high=integers(min_value=101),
)
def test_light_brightness_range(input_brightness_low, input_brightness_high):
    """
    Test the brightness range of the Light class.
    """
    light1 = Light(
        entity_id=1, name="Test Light", brightness=input_brightness_low
    )
    light2 = Light(
        entity_id=2, name="Test Light", brightness=input_brightness_high
    )

    # Test default brightness
    assert light1.brightness == 0
    assert light2.brightness == 100

    # Test lower limit
    with pytest.raises(ValueError):
        light1.brightness = -1

    # Test upper limit
    with pytest.raises(ValueError):
        light1.brightness = 101


@given(
    input_id=integers(min_value=1),
    input_name=text(min_size=5, max_size=20),
    input_status=sampled_from(EntityStatus),
    input_light_type=sampled_from(LightType),
)
def test_light_from_json_valid(
    input_id, input_name, input_status, input_light_type
):
    """
    Test the from_json method of the Light class with valid input.
    """
    data = {
        "act_id": input_id,
        "name": input_name,
        "status": input_status.value,
        "type": input_light_type.value,
    }
    light = Light.from_json(data)

    assert light.id == input_id
    assert light.name == input_name
    assert light.status == input_status
    assert light.light_type == input_light_type


def test_light_from_json_missing_optional_keys():
    """
    Test the from_json method of the Light class with missing keys in the JSON data.
    """
    json_data = {"act_id": 5}
    light = Light.from_json(json_data)

    assert light.id == 5
    assert light.name == "Unknown"
    assert light.status == EntityStatus.OFF_CLOSED
    assert light.light_type == LightType.ON_OFF


def test_light_from_json_missing_required_keys():
    """
    Test the from_json method of the Light class with missing keys in the JSON data.
    """
    json_data = {
        "name": "My light",
        "status": 0,
    }
    with pytest.raises(KeyError):
        Light.from_json(json_data)


def test_light_from_json_invalid_values():
    """
    Test the from_json method of the Light class with invalid JSON values
    """
    json_data = {
        "act_id": 5,
        "name": 8,  # Should be a string
        "status": "unexpected",  # Should be an EntityStatus value
        "type": 999,  # Should be a LightType value
    }
    with pytest.raises(ValueError):
        Light.from_json(json_data)


# endregion

# region Opening


@given(
    entity_id=integers(min_value=1),
    name=text(min_size=5, max_size=20),
    status=sampled_from(EntityStatus),
    cover_type=sampled_from(OpeningType),
)
def test_opening_initialization(entity_id, name, status, cover_type):
    """
    Test the initialization and the properties of the Opening class.
    """
    opening = Opening(
        entity_id,
        entity_id + 1,
        name,
        status=status,
        cover_type=cover_type,
    )

    assert opening.id == entity_id
    assert opening.close_entity_id == entity_id + 1
    assert opening.name == name
    assert opening.status == status
    assert opening.cover_type == cover_type
    assert not opening.partial_openings  # an empty list is falsey
    assert opening.type == Opening


@given(
    entity_id=integers(min_value=1),
)
def test_opening_initialization_defaults(entity_id):
    """
    Test the initialization and the properties of the Opening class
    with default values.
    """
    opening = Opening(entity_id)

    assert opening.id == entity_id
    assert opening.close_entity_id == entity_id
    assert opening.name == "Unknown"
    assert opening.status == EntityStatus.ON_OPEN
    assert opening.cover_type == OpeningType.OPEN_CLOSE
    assert not opening.partial_openings  # an empty list is falsey


@given(
    open_act_id=integers(min_value=1),
    name=text(min_size=5, max_size=20),
    status=sampled_from(EntityStatus),
    cover_type=sampled_from(OpeningType),
)
def test_opening_from_json_valid(open_act_id, name, status, cover_type):
    """
    Test the from_json method of the Opening class with valid input.
    """
    # Example of CAME opening entity:
    # {
    #    "open_act_id": 26,
    #    "close_act_id": 27,
    #    "name": "My opening",
    #    "floor_ind": 17,
    #    "room_ind": 48,
    #    "status": 0,
    #    "partial": [],
    #    "type": 0
    # }

    json_data = {
        "open_act_id": open_act_id,
        "close_act_id": open_act_id + 1,
        "name": name,
        "status": status.value,
        "partial": [],
        "type": cover_type.value,
    }
    opening = Opening.from_json(json_data)

    assert opening.id == open_act_id
    assert opening.close_entity_id == open_act_id + 1
    assert opening.name == name
    assert opening.status == status
    assert opening.cover_type == cover_type
    assert not opening.partial_openings  # an empty list is falsey
    assert opening.type == Opening


@given(
    open_act_id=integers(min_value=1),
)
def test_opening_from_json_missing_optional_key(open_act_id):
    """
    Test the from_json method of the Opening class
    with valid input (missing keys are optional).
    """

    json_data = {
        "open_act_id": open_act_id,
    }
    opening = Opening.from_json(json_data)

    assert opening.id == open_act_id
    assert opening.close_entity_id == open_act_id
    assert opening.name == "Unknown"
    assert opening.status == EntityStatus.ON_OPEN
    assert opening.cover_type == OpeningType.OPEN_CLOSE
    assert not opening.partial_openings  # an empty list is falsey
    assert opening.type == Opening


def test_opening_from_json_missing_required_keys():
    """
    Test the from_json method of the Opening class
    with missing keys in the JSON data.
    """
    json_data = {
        "name": "My opening",
        "status": 0,
    }
    with pytest.raises(KeyError):
        Opening.from_json(json_data)


def test_opening_from_json_invalid_values():
    """
    Test the from_json method of the Opening class with invalid values in the JSON data.
    """
    json_data = {
        "open_act_id": "unexpected",  # Should be an integer
        "close_act_id": 5,
        "name": "Test",
        "status": "unexpected",  # Should be an EntityStatus value
    }
    with pytest.raises(ValueError):
        Opening.from_json(json_data)


# endregion
