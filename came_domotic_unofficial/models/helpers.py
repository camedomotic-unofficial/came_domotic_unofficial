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
CAME Domotic helpers (enums, mappers, etc.)
"""

from typing import Type
from .came_entity import CameEntity
from .feature import Feature
from .light import Light
from .opening import Opening
from .digital_input import DigitalInput
from .scenario import Scenario
from .enums import EntityType


# region Mappers

_EntityType2Class: dict[EntityType, Type[CameEntity]] = {
    EntityType.FEATURES: Feature,
    EntityType.LIGHTS: Light,
    EntityType.OPENINGS: Opening,
    EntityType.DIGITALIN: DigitalInput,
    EntityType.SCENARIOS: Scenario,
    # EntityType.UPDATE:
    # EntityType.RELAYS:
    # EntityType.CAMERAS:
    # EntityType.TIMERS:
    # EntityType.THERMOREGULATION:
    # EntityType.ANALOGIN:
    # EntityType.USERS:
    # EntityType.MAPS:
}

_Class2SwitchCommand = {
    Light: "light_switch_req",
    Opening: "opening_move_req",
    Scenario: "scenario_activation_req",
}

# endregion
