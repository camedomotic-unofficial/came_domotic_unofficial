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
Unit tests for the Scenario class.
"""

from hypothesis import given
from hypothesis.strategies import integers, text, booleans, sampled_from
import pytest
from came_domotic_unofficial.models import (
    CameEntity,
    EntityStatus,
    Scenario,
    ScenarioStatus,
    ScenarioIcon,
)


@given(
    entity_id=integers(),
    name=text(min_size=1),
    status=sampled_from(EntityStatus),
    scenario_status=sampled_from(ScenarioStatus),
    icon=sampled_from(ScenarioIcon),
    is_user_defined=booleans(),
)
def test_scenario_constructor(
    entity_id, name, status, scenario_status, icon, is_user_defined
):
    """
    Test if the Scenario constructor works correctly.
    """
    scenario = Scenario(
        entity_id,
        name,
        status=status,
        scenario_status=scenario_status,
        icon=icon,
        is_user_defined=is_user_defined,
    )
    assert isinstance(scenario, CameEntity)
    assert scenario.id == entity_id
    assert scenario.name == name
    assert scenario.status == status
    assert scenario.scenario_status == scenario_status
    assert scenario.icon == icon
    assert scenario.is_user_defined == is_user_defined


def test_scenario_constructor_defaults():
    """
    Test if the Scenario constructor defaults work correctly.
    """
    scenario = Scenario(1)
    assert scenario.id == 1
    assert scenario.name == "Unknown"
    assert scenario.status == EntityStatus.UNKNOWN
    assert scenario.scenario_status == ScenarioStatus.NOT_APPLIED
    assert scenario.icon == ScenarioIcon.UNKNOWN
    assert not scenario.is_user_defined


def test_scenario_constructor_invalid_scenario_status():
    """
    Test if the Scenario constructor raises a TypeError with an invalid
    scenario_status.
    """
    with pytest.raises(TypeError):
        Scenario(1, scenario_status=100)


def test_scenario_constructor_invalid_icon():
    """
    Test if the Scenario constructor raises a TypeError with an invalid icon.
    """
    with pytest.raises(TypeError):
        Scenario(1, icon=100)


def test_scenario_constructor_invalid_is_user_defined():
    """
    Test if the Scenario constructor raises a TypeError with an invalid
    is_user_defined.
    """
    with pytest.raises(TypeError):
        Scenario(1, is_user_defined="invalid")


def test_scenario_scenario_status_setter():
    """
    Test if the Scenario scenario_status setter works correctly.
    """
    scenario = Scenario(1)
    assert scenario.status == EntityStatus.UNKNOWN

    scenario.scenario_status = ScenarioStatus.APPLIED
    assert scenario.scenario_status == ScenarioStatus.APPLIED


def test_scenario_scenario_status_setter_invalid():
    """
    Test if the Scenario scenario_status setter raises a TypeError with an
    invalid scenario_status.
    """
    scenario = Scenario(1)
    with pytest.raises(TypeError):
        scenario.scenario_status = 100


def test_scenario_str_method():
    """
    Test if the Scenario __str__ method works correctly.
    """
    scenario = Scenario(
        1,
        "Test Scenario",
        status=EntityStatus.OFF_STOPPED,
        scenario_status=ScenarioStatus.APPLIED,
        icon=ScenarioIcon.UNKNOWN,
        is_user_defined=True,
    )

    assert str(scenario) == (
        'Scenario #1: "Test Scenario" - Status: OFF_STOPPED - '
        "Scenario status: APPLIED - Icon: UNKNOWN - User defined: True"
    )


def test_scenario_repr_method():
    """
    Test if the Scenario __repr__ method works correctly.
    """
    scenario = Scenario(
        1,
        "Test Scenario",
        status=EntityStatus.OFF_STOPPED,
        scenario_status=ScenarioStatus.APPLIED,
        icon=ScenarioIcon.UNKNOWN,
        is_user_defined=True,
    )

    assert repr(scenario) == (
        'Scenario(1,"Test Scenario",status=EntityStatus.OFF_STOPPED,'
        "scenario_status=ScenarioStatus.APPLIED,icon=ScenarioIcon.UNKNOWN,"
        "is_user_defined=True)"
    )


def test_scenario_equality_hash_operators():
    """
    Test if the Opening equality and hash operators work correctly.
    """
    scenario_name = "Test"
    scenario1 = Scenario(1, scenario_name)
    scenario2 = Scenario(1, scenario_name)
    scenario3 = Scenario(
        1,
        scenario_name,
        status=EntityStatus.UNKNOWN,
        scenario_status=ScenarioStatus.NOT_APPLIED,
        icon=ScenarioIcon.UNKNOWN,
        is_user_defined=False,
    )
    scenario4 = Scenario(2, scenario_name)
    scenario5 = Scenario(1, scenario_name + "_")
    scenario6 = Scenario(1, scenario_name, status=EntityStatus.ON_OPEN_TRIGGERED)
    other_type1 = CameEntity(1, scenario_name, status=EntityStatus.UNKNOWN)
    other_type2 = repr(scenario1)
    other_type3 = scenario_name

    assert scenario1 == scenario2
    assert scenario1 == scenario3
    assert scenario1 != scenario4
    assert scenario1 != scenario5
    assert scenario1 != scenario6
    assert scenario1 != other_type1
    assert scenario1 != other_type2
    assert scenario1 != other_type3

    assert hash(scenario1) == hash(scenario2)
    assert hash(scenario1) == hash(scenario3)
    assert hash(scenario1) != hash(scenario4)
    assert hash(scenario1) != hash(scenario5)
    assert hash(scenario1) != hash(scenario6)
    assert hash(scenario1) != hash(other_type1)
    assert hash(scenario1) != hash(other_type2)
    assert hash(scenario1) != hash(other_type3)


def test_scenario_from_json():
    """
    Test if the Scenario from_json method works correctly.
    """
    json_data = {
        "icon_id": 14,
        "id": 5,
        "name": "My scenario",
        "scenario_status": 1,
        "status": 1,
        "user-defined": 1,
    }
    scenario = Scenario.from_json(json_data)
    assert scenario.id == 5
    assert scenario.name == "My scenario"
    assert scenario.status == EntityStatus.ON_OPEN_TRIGGERED
    assert scenario.scenario_status == ScenarioStatus.ONGOING
    assert scenario.icon == ScenarioIcon.LIGHTS
    assert scenario.is_user_defined


def test_scenario_from_json_defaults():
    """
    Test if the Scenario from_json defaults work correctly.
    """
    json_data = {
        "id": 3,
    }
    scenario = Scenario.from_json(json_data)
    assert scenario.id == 3
    assert scenario.name == "Unknown"
    assert scenario.status == EntityStatus.UNKNOWN
    assert scenario.scenario_status == ScenarioStatus.NOT_APPLIED
    assert scenario.icon == ScenarioIcon.UNKNOWN
    assert not scenario.is_user_defined


def test_scenario_from_json_invalid():
    """
    Test if the Scenario from_json method raises a TypeError with invalid
    JSON data.
    """
    json_data = {
        "id": 5,
        "icon_id": "invalid",
        "name": -1,
        "scenario_status": "invalid",
        "status": "invalid",
        "user-defined": "invalid",
    }
    scenario = Scenario.from_json(json_data)
    assert scenario.id == 5
    assert scenario.name == "Unknown"
    assert scenario.status == EntityStatus.UNKNOWN
    assert scenario.scenario_status == ScenarioStatus.NOT_APPLIED
    assert scenario.icon == ScenarioIcon.UNKNOWN
    assert not scenario.is_user_defined


def test_scenario_from_json_missing_required():
    """
    Test if the Scenario from_json method raises an exception when the JSON
    data is missing required keys.
    """
    json_data = {
        "icon_id": 14,
        "name": "My scenario",
        "scenario_status": 0,
        "status": 2,
        "user-defined": 1,
    }
    with pytest.raises(KeyError):
        Scenario.from_json(json_data)


def test_scenario_from_json_unexpected():
    """
    Test if the Scenario from_json method raises an exception when the JSON
    data contains unexpected keys.
    """
    json_data = {
        "unexpected": "unexpected",
        "icon_id": 14,
        "id": 5,
        "name": "My scenario",
        "scenario_status": 0,
        "status": 0,
        "user-defined": 1,
    }
    scenario = Scenario.from_json(json_data)
    assert scenario.id == 5
    assert scenario.name == "My scenario"
    assert scenario.status == EntityStatus.OFF_STOPPED
    assert scenario.scenario_status == ScenarioStatus.NOT_APPLIED
    assert scenario.icon == ScenarioIcon.LIGHTS
    assert scenario.is_user_defined
