# # Copyright 2024 - GitHub user: fredericks1982

# # Licensed under the Apache License, Version 2.0 (the "License");
# # you may not use this file except in compliance with the License.
# # You may obtain a copy of the License at

# #     http://www.apache.org/licenses/LICENSE-2.0

# # Unless required by applicable law or agreed to in writing, software
# # distributed under the License is distributed on an "AS IS" BASIS,
# # WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# # See the License for the specific language governing permissions and
# # limitations under the License.

# from enum import Enum

# # Enum listing all the CAME features
# Features:
#     LIGHTS = "lights"
#     OPENINGS = "openings",
#     THERMOREGULATION = "thermoregulation"
#     SCENES = "scenarios",
#     BUTTONS = "digitalin",
#     ENERGY_METERS="energy",
#     LOADS_CONTROL = "loadsctrl",
#     RELAY = "relay"
#     CAMERA = "tvcc"
#     TIMER = "timer"
#     ANALOGIN = "analogin"
#     USER = "user"
#     MAP = "map"
#     ALL = "all"

# # Enum listing all the CAME commands (strings)
# class Command(Enum):
#     UPDATE_STATUS = "status_update_req"
#     LIST_RELAYS = "relays_list_req"
#     LIST_CAMERAS = "tvcc_cameras_list_req"
#     LIST_TIMERS = "timers_list_req"
#     LIST_THERMOREGULATION = "thermo_list_req"
#     LIST_ANALOGIN = "analogin_list_req"
#     LIST_DIGITALIN = "digitalin_list_req"
#     LIST_LIGHTS = "light_list_req"
#     LIST_LIGHTS_NESTED = "nested_light_list_req"
#     LIST_FEATURES = "feature_list_req"
#     LIST_USERS = "sl_users_list_req"
#     GET_MAPS_DESCRIPTION = "map_descr_req"


# # Enum listing the available seasons
# class SeasonSetting(Enum):
#     OFF = "plant_off"
#     WINTER = "winter"
#     SUMMER = "summer"


# # Enum listing the available thermo zone status
# class ThermoZoneStatus(Enum):
#     OFF = 0
#     MANUAL = 1
#     AUTO = 2
#     JOLLY = 3


# # Enum listing all the CAME entity types
# class EntityType(Enum):
#     LIGHT = None
#     ALL = None
#     # RELAY = None
#     # CAMERA = None
#     # TIMER = None
#     # THERMOREGULATION = None
#     # ANALOGIN = None
#     # DIGITALIN = None
#     FEATURE = None
#     # USER = None
#     # MAP = None


# # Enum listing all the CAME entity status


# class EntityStatus(Enum):
#     ON = 1
#     OFF = 0
#     OPEN = 1
#     CLOSE = 0
#     TRIGGERED = 1
#     NONE = None


# class LightType(Enum):
#     ON_OFF = "STEP_STEP"
#     DIMMERABLE = "DIMMER"
#     UNKNOWN = None
