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
Unit tests for the CameEntity and CameEntitiesSet classes.
"""

import pytest
from hypothesis import given
from hypothesis.strategies import integers, text, sampled_from
from came_domotic_unofficial.models import (
    CameEntitySet,
    CameEntity,
    EntityStatus,
)

# region CameEntity


@given(
    input_id=integers(),
    input_name=text(min_size=1),
    input_status=sampled_from(EntityStatus),
)
def test_came_entity_init_complete(input_id, input_name, input_status):
    """
    Test the initialization of the CameEntity class with all the parameters.
    """
    entity = CameEntity(input_id, input_name, status=input_status)

    assert entity.id == input_id
    assert entity.name == input_name
    assert entity.status == input_status


def test_came_entity_init_invalid_id():
    """
    Test the initialization of the CameEntity class with an invalid id.
    """
    with pytest.raises(TypeError):
        CameEntity("QAW")


def test_came_entity_init_invalid_name():
    """
    Test the initialization of the CameEntity class with an invalid name.
    """
    entity = CameEntity(1, 2)
    assert entity.name == "Unknown"


def test_came_entity_init_invalid_status():
    """
    Test the initialization of the CameEntity class with an invalid status.
    """
    entity = CameEntity(1, "Test", status="Not a valid status")
    assert entity.status == EntityStatus.UNKNOWN


def test_came_entity_init_no_status():
    """
    Test the initialization of the CameEntity class with only
    the id and name parameters.
    """
    entity = CameEntity(1, "Test")

    assert entity.id == 1
    assert entity.name == "Test"
    assert entity.status == EntityStatus.UNKNOWN


def test_came_entity_init_no_name():
    """
    Test the initialization of the CameEntity class with only the id parameter.
    """
    entity = CameEntity(1)

    assert entity.id == 1
    assert entity.name == "Unknown"
    assert entity.status == EntityStatus.UNKNOWN


@given(
    new_status=sampled_from(EntityStatus),
)
def test_came_entity_set_status(new_status):
    """
    Test if the status property of the CameEntity class can be set properly.
    """
    entity = CameEntity(1)

    entity.status = new_status
    assert entity.status == new_status


def test_came_entity_set_not_valid_status():
    """
    Test if the status property of the CameEntity class can be set to
    an invalid value.
    """
    entity = CameEntity(1)

    assert entity.status == EntityStatus.UNKNOWN

    with pytest.raises(TypeError):
        entity.status = "Not a valid status"

    assert entity.status == EntityStatus.UNKNOWN


@given(
    entity_id=integers(),
    name=text(min_size=1),
    status=sampled_from(EntityStatus),
)
def test_came_entity_str(entity_id, name, status: EntityStatus):
    """
    Test the string representation of the CameEntity class.
    """
    entity = CameEntity(entity_id, name, status=status)

    assert str(entity) == (
        f"CameEntity #{entity_id}: {name} - Status: " f"{status.name}"
    )


@given(
    entity_id=integers(),
    name=text(min_size=1),
    status=sampled_from(EntityStatus),
)
def test_came_entity_repr(entity_id, name, status: EntityStatus):
    """
    Test the string representation of the CameEntity class.
    """
    entity = CameEntity(entity_id, name, status=status)

    assert repr(entity) == f'CameEntity({entity_id},"{name}",status={status})'


@given(
    entity_id=integers(),
    name=text(min_size=1),
    status=sampled_from(EntityStatus),
)
def test_came_entity_eq(entity_id, name, status):
    """
    Test the equality operator for the CameEntity class.
    """

    came_entity1 = CameEntity(entity_id, name, status=status)
    came_entity2 = CameEntity(entity_id, name, status=status)
    came_entity3 = CameEntity(entity_id + 1, name, status=status)
    came_entity4 = CameEntity(entity_id, name + "_", status=status)
    other_type = repr(came_entity1)

    assert came_entity1 == came_entity2
    with pytest.raises(AssertionError):
        assert came_entity1 == came_entity3
    with pytest.raises(AssertionError):
        assert came_entity1 == came_entity4
    assert came_entity1 != other_type


@given(
    entity_id=integers(),
    name=text(min_size=1),
    status=sampled_from(EntityStatus),
)
def test_came_entity_ne(entity_id, name, status):
    """
    Test the inequality operator for the CameEntity class.
    """
    came_entity1 = CameEntity(entity_id, name, status=status)
    came_entity2 = CameEntity(entity_id + 1, name, status=status)
    came_entity3 = CameEntity(entity_id, name + "_", status=status)
    came_entity4 = CameEntity(
        entity_id,
        name,
        status=(
            EntityStatus.UNKNOWN
            if status != EntityStatus.UNKNOWN
            else EntityStatus.ON_OPEN_TRIGGERED
        ),
    )
    came_entity_identical = CameEntity(entity_id, name, status=status)

    assert came_entity1 != came_entity2
    assert came_entity1 != came_entity3
    assert came_entity1 != came_entity4
    with pytest.raises(AssertionError):
        assert came_entity1 != came_entity_identical


@given(
    entity_id=integers(),
    name=text(min_size=1),
    status=sampled_from(EntityStatus),
)
def test_came_entity_hash(entity_id, name, status):
    """
    Test the hash method of the CameEntity class.
    """
    came_entity1 = CameEntity(entity_id, name, status=status)
    came_entity2 = CameEntity(entity_id, name, status=status)
    came_entity3 = CameEntity(entity_id + 1, name, status=status)
    other_type = repr(came_entity1)

    assert hash(came_entity1) == hash(came_entity2)
    assert hash(came_entity1) != hash(came_entity3)
    assert hash(came_entity1) != hash(other_type)


@given(
    entity_id=integers(),
    name=text(min_size=1),
    status=sampled_from(EntityStatus),
)
def test_came_entity_from_json(entity_id, name, status):
    """
    Test the from_json method of the CameEntity class.
    """
    json_data = {
        "act_id": entity_id,
        "name": name,
        "status": status.value,
    }
    came_entity = CameEntity.from_json(json_data)

    assert came_entity.id == entity_id
    assert came_entity.name == name
    assert came_entity.status == status


@given(
    entity_id=integers(),
)
def test_came_entity_from_json_defaults(entity_id):
    """
    Test the from_json method of the CameEntity class.
    """
    json_data = {
        "act_id": entity_id,
    }
    came_entity = CameEntity.from_json(json_data)

    assert came_entity == CameEntity(entity_id)


@given(
    name=text(min_size=1),
    status=sampled_from(EntityStatus),
)
def test_came_entity_from_json_missing_required(name, status):
    """
    Test the from_json method of the CameEntity class.
    """
    json_data = {
        "name": name,
        "status": status.value,
    }

    with pytest.raises(KeyError):
        CameEntity.from_json(json_data)


def test_came_entity_from_json_unexpected_keys():
    """
    Test the from_json method of the CameEntity class.
    """
    json_data = {
        "act_id": 1,
        "name": "Test",
        "status": EntityStatus.UNKNOWN.value,
        "unknown_key": "Value",
    }
    came_entity = CameEntity.from_json(json_data)

    assert came_entity == CameEntity(1, "Test", status=EntityStatus.UNKNOWN)


def test_came_entity_from_json_unexpected_values():
    """
    Test the from_json method of the CameEntity class.
    """
    json_data = {
        "act_id": 1,
        "name": -1000,
        "status": "invalid",
    }
    came_entity = CameEntity.from_json(json_data)

    assert came_entity == CameEntity(1)


# endregion

# region CameEntitiesSet


def test_came_entitiesset_initialization():
    """
    Test the initialization of the CameEntitiesSet class.
    """
    entities_set = CameEntitySet()

    assert isinstance(entities_set, set)
    assert len(entities_set) == 0


def test_came_entitiesset_initialization_with_items():
    """
    Test the initialization of the CameEntitiesSet class with items.
    """
    entity1 = CameEntity(1, "Test Entity 1")
    entity2 = CameEntity(2, "Test Entity 2")
    entities_set = CameEntitySet([entity1, entity2])

    assert entity1 in entities_set
    assert entity2 in entities_set
    assert len(entities_set) == 2


def test_came_entitiesset_eq():
    """
    Test the equality operator for the CameEntitiesSet class.
    """
    entity1 = CameEntity(1, "Test Entity 1")
    entity2 = CameEntity(2, "Test Entity 2")
    entity3 = CameEntity(3, "Test Entity 3")
    entities_set1 = CameEntitySet([entity1, entity2])
    entities_set2 = CameEntitySet([entity1, entity2])
    entities_set3 = CameEntitySet([entity1, entity3])

    assert entities_set1 == entities_set2
    assert entities_set1 != entities_set3


def test_came_entitiesset_add_valid_item():
    """
    Test if a valid item can be added to the CameEntitiesSet.
    """
    entities_set = CameEntitySet()
    entity = CameEntity(1, "Test Entity")
    entities_set.add(entity)

    assert entity in entities_set


def test_came_entitiesset_add_invalid_item():
    """
    Test if an invalid item cannot be added to the CameEntitiesSet.
    """
    entities_set = CameEntitySet()

    with pytest.raises(TypeError) as exc_info:
        entities_set.add("Invalid Item")

    assert str(exc_info.value) == "Item must be of type 'CameEntity'"


def test_came_entitiesset_add_duplicate_item():
    """
    Test if a duplicate item can be added to the CameEntitiesSet.
    """
    entities_set = CameEntitySet()
    entity = CameEntity(1, "Test Entity")
    entities_set.add(entity)
    entities_set.add(entity)

    assert len(entities_set) == 1


# endregion
