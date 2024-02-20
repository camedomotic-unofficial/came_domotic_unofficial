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
Unit tests for the Opening class.
"""

import pytest
from hypothesis import given
from hypothesis.strategies import integers, text, sampled_from
from came_domotic_unofficial.models import (
    CameEntity,
    EntityStatus,
    Opening,
    OpeningType,
)


@given(
    entity_id=integers(min_value=1),
    close_entity_id=integers(min_value=1),
    name=text(min_size=1),
    status=sampled_from(EntityStatus),
    opening_type=sampled_from(OpeningType),
)
def test_opening_constructor(
    entity_id, close_entity_id, name, status, opening_type
):
    """
    Test if the Opening constructor works correctly.
    """
    opening = Opening(
        entity_id,
        close_entity_id=close_entity_id,
        name=name,
        status=status,
        opening_type=opening_type,
    )
    assert isinstance(opening, CameEntity)
    assert opening.id == entity_id
    assert opening.close_entity_id == close_entity_id
    assert opening.name == name
    assert opening.status == status
    assert opening.opening_type == opening_type
    assert not opening.partial_openings


@given(
    entity_id=integers(min_value=1),
)
def test_opening_init_defaults(entity_id):
    """
    Test if the Opening constructor works correctly with default values.
    """
    opening = Opening(entity_id)
    assert opening.id == entity_id
    assert opening.close_entity_id == opening.id
    assert opening.name == "Unknown"
    assert opening.status == EntityStatus.UNKNOWN
    assert opening.opening_type == OpeningType.OPEN_CLOSE
    assert not opening.partial_openings


def test_opening_init_invalid_close_entity_id():
    """
    Test if the Opening constructor raises an error with an invalid
    close entity id.
    """
    with pytest.raises(TypeError):
        Opening(1, close_entity_id="invalid")


def test_opening_init_invalid_opening_type():
    """
    Test if the Opening constructor raises an error with an invalid
    opening type.
    """
    with pytest.raises(TypeError):
        Opening(1, opening_type="invalid")


def test_opening_init_invalid_partial_openings():
    """
    Test if the Opening constructor raises an error with
    an invalid partial openings.
    """
    with pytest.raises(TypeError):
        Opening(1, partial_openings="invalid")


def test_opening_str_method():
    """
    Test if the Opening __str__ method works correctly.
    """
    opening = Opening(
        1,
        "Test Opening",
        close_entity_id=2,
        status=EntityStatus.ON_OPEN_TRIGGERED,
        opening_type=OpeningType.OPEN_CLOSE,
    )

    assert str(opening) == (
        'Opening #1/2: "Test Opening" - Type: OPEN_CLOSE - '
        "Status: ON_OPEN_TRIGGERED - Partials: []"
    )


def test_opening_repr_method():
    """
    Test if the Opening __repr__ method works correctly.
    """
    opening = Opening(
        1,
        "Test Opening",
        close_entity_id=2,
        status=EntityStatus.ON_OPEN_TRIGGERED,
        opening_type=OpeningType.OPEN_CLOSE,
    )

    assert repr(opening) == (
        'Opening(1,2,"Test Opening",status=EntityStatus.ON_OPEN_TRIGGERED,'
        "opening_type=OpeningType.OPEN_CLOSE,partial_openings=[])"
    )


def test_opening_equality_hash_operators():
    """
    Test if the Opening equality and hash operators work correctly.
    """
    opening_name = "Test"
    opening1 = Opening(1, opening_name)
    opening2 = Opening(1, opening_name)
    opening3 = Opening(
        1,
        opening_name,
        close_entity_id=1,
        opening_type=OpeningType.OPEN_CLOSE,
        status=EntityStatus.UNKNOWN,
    )
    opening4 = Opening(2, opening_name)
    opening5 = Opening(1, opening_name + "_")
    opening6 = Opening(1, opening_name, status=EntityStatus.ON_OPEN_TRIGGERED)
    other_type1 = CameEntity(1, opening_name, status=EntityStatus.UNKNOWN)
    other_type2 = repr(opening1)
    other_type3 = opening_name

    assert opening1 == opening2
    assert opening1 == opening3
    assert opening1 != opening4
    assert opening1 != opening5
    assert opening1 != opening6
    assert opening1 != other_type1
    assert opening1 != other_type2
    assert opening1 != other_type3

    assert hash(opening1) == hash(opening2)
    assert hash(opening1) == hash(opening3)
    assert hash(opening1) != hash(opening4)
    assert hash(opening1) != hash(opening5)
    assert hash(opening1) != hash(opening6)
    assert hash(opening1) != hash(other_type1)
    assert hash(opening1) != hash(other_type2)
    assert hash(opening1) != hash(other_type3)


@given(
    entity_id=integers(min_value=1),
    close_entity_id=integers(min_value=1),
    name=text(min_size=1),
    status=sampled_from(EntityStatus),
    opening_type=sampled_from(OpeningType),
)
def test_opening_from_json(
    entity_id, close_entity_id, name, status, opening_type
):
    """
    Test if the Opening from_json method works correctly.
    """
    json_data = {
        "open_act_id": entity_id,
        "close_act_id": close_entity_id,
        "name": name,
        "status": status.value,
        "partial": [],
        "type": opening_type.value,
    }
    opening = Opening.from_json(json_data)
    assert opening.id == entity_id
    assert opening.close_entity_id == close_entity_id
    assert opening.name == name
    assert opening.status == status
    assert opening.opening_type == opening_type
    assert not opening.partial_openings


@given(
    entity_id=integers(min_value=1),
)
def test_opening_from_json_defaults(entity_id):
    """
    Test if the Opening from_json method works correctly when optional keys
    """
    json_data = {
        "open_act_id": entity_id,
    }
    opening = Opening.from_json(json_data)
    check_opening = Opening(entity_id)

    assert opening == check_opening


def test_opening_from_json_invalid_values():
    """
    Test if the Opening from_json method raises an exception when the JSON
    """
    json_data = {
        "open_act_id": 1,
        "close_act_id": 2,
        "name": "Test",
        "status": "Invalid",
        "partial": [],
        "type": "Invalid",
    }
    opening = Opening.from_json(json_data)
    check_opening = Opening(1, "Test", close_entity_id=2)

    assert opening == check_opening


def test_opening_from_json_missing_required_keys():
    """
    Test if the Opening from_json method raises an exception when the JSON
    """
    json_data = {
        "close_act_id": 2,
        "name": "Test",
        "status": 0,
        "partial": [],
        "type": 0,
    }
    with pytest.raises(KeyError):
        Opening.from_json(json_data)


def test_opening_from_json_unexpected_properties():
    """Test if the Opening from_json method works correctly."""
    json_data = {
        "open_act_id": 1,
        "close_act_id": 2,
        "name": "Test",
        "status": 0,
        "partial": [],
        "type": 0,
        "unexpected": "unexpected",
    }
    opening = Opening.from_json(json_data)
    check_opening = Opening(
        1,
        "Test",
        close_entity_id=2,
        status=EntityStatus(0),
        partial_openings=[],
        opening_type=OpeningType(0),
    )

    assert opening == check_opening
