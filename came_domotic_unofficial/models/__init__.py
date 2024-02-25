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

# pylint: disable=unused-import

"""This module contains the classes representing the CAME Domotic entities."""

from .exceptions import (
    CameDomoticError,
    CameDomoticServerNotFoundError,
    CameDomoticAuthError,
    CameDomoticRemoteServerError,
    CameDomoticRequestError,
    CameDomoticBadAckError,
)
from .enums import (
    EntityType,
    EntityStatus,
    LightType,
    OpeningType,
    DigitalInputType,
    ScenarioStatus,
    ScenarioIcon,
)
from .came_entity import CameEntity, CameEntitySet
from .feature import Feature, FeatureSet
from .light import Light
from .opening import Opening
from .scenario import Scenario
from .digital_input import DigitalInput
