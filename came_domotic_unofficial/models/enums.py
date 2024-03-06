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
This module contains all the enums used in the CAME Domotic Unofficial API.
"""

from enum import Enum


class CameEnum(Enum):
    """Base class for all the CAME-related enums."""


class EntityType(CameEnum):
    """Enum listing all the CAME entity types.

    The :name of each enum member maps to feature.name.upper(),
    where 'feature' is a Feature instance.

    The :value of each enum member is the command to send to the remote server
    if you want to retrieve the list of items related to that entity type.
    """

    FEATURES = "feature_list_req"
    LIGHTS = "light_list_req"  # "nested_light_list_req"
    OPENINGS = "openings_list_req"  # "nested_openings_list_req"
    DIGITALIN = "digitalin_list_req"
    SCENARIOS = "scenarios_list_req"
    # UPDATE = "status_update_req"
    # RELAYS = "relays_list_req"
    # CAMERAS = "tvcc_cameras_list_req"
    # TIMERS = "timers_list_req"
    # THERMOREGULATION = "thermo_list_req"
    # ANALOGIN = "analogin_list_req"
    # USERS = "sl_users_list_req"
    # MAPS = "map_descr_req"


class EntityStatus(CameEnum):
    """Enum listing all the status of the CAME entities."""

    OFF_STOPPED = 0
    ON_OPEN_TRIGGERED = 1
    CLOSED = 2
    UNKNOWN = -1
    NOT_APPLICABLE = -99


class LightType(CameEnum):
    """Enum listing the light types."""

    ON_OFF = "STEP_STEP"
    DIMMABLE = "DIMMER"


class OpeningType(CameEnum):
    """Enum listing the opening types."""

    OPEN_CLOSE = 0


class DigitalInputType(CameEnum):
    """Enum listing the digital input types."""

    BUTTON = 1


class ScenarioIcon(CameEnum):
    """Enum listing the scenario icons."""

    LIGHTS = 14
    OPENINGS_OPEN = 22
    OPENINGS_CLOSE = 23
    UNKNOWN = -1


class ScenarioStatus(CameEnum):
    """Enum listing the scenario status."""

    NOT_APPLIED = 0
    ONGOING = 1
    APPLIED = 2


class SeasonSetting(Enum):
    """Enum listing the available seasons settings."""

    PLANT_OFF = "off"
    WINTER = "winter"
    SUMMER = "summer"


class ThermoZoneStatus(Enum):
    """Enum listing the available thermostat zone status."""

    OFF = 0
    MANUAL = 1
    AUTO = 2
    JOLLY = 3
