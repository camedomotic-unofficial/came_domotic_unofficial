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
This module contains the class representing a CAME scenario.

Raises:
    TypeError: If not assigning to the scenario_status property a valid ScenarioStatus.
"""

from typing import Optional
from .came_entity import CameEntity
from .enums import EntityStatus, ScenarioStatus, ScenarioIcon


class Scenario(CameEntity):
    """Represents a CAME predefined scenario.

    The Scenario class is a subclass of the CameEntity class, and it's used to
    represent a CAME predefined scenario.

    :property id: the scenario ID
    :property name: the scenario name. Defaults to "Unknown" if None or empty.
    :property status: the scenario status (OFF, ON). Defaults to OFF.
    :property scenario_status: the scenario status (NOT_APPLIED, ONGOING, APPLIED). Defaults to NOT_APPLIED
    :property icon: the scenario icon type. Defaults to UNKNOWN.
    :property is_user_defined: the scenario is user defined. Defaults to False.

    :method from_json: create a Scenario object from a JSON dictionary.
    """

    _DEFAULT_STATUS = EntityStatus.UNKNOWN
    _DEFAULT_SCENARIO_STATUS = ScenarioStatus.NOT_APPLIED
    _DEFAULT_ICON_ID = ScenarioIcon.UNKNOWN

    def __init__(
        self,
        entity_id: int,
        name: Optional[str] = CameEntity._DEFAULT_NAME,
        *,
        status: EntityStatus = _DEFAULT_STATUS,
        scenario_status: ScenarioStatus = _DEFAULT_SCENARIO_STATUS,
        icon: ScenarioIcon = _DEFAULT_ICON_ID,
        is_user_defined: bool = False,
    ):
        """
        Constructor for the Came Scenario class.

        Args:
            entity_id (int): the scenario ID.
            name (str, optional): the scenario name. Default: "Unknown" if None/empty.
            status (EntityStatus, optional): the scenario status. Defaults to UNKNOWN.
            scenario_status (ScenarioStatus, optional): the scenario status. Defaults to NOT_APPLIED.
            icon (ScenarioIcon, optional): the scenario icon type. Defaults to UNKNOWN.
            is_user_defined (bool, optional): whether the scenario is user defined. Defaults to False.
        """

        # Validate the input
        if scenario_status not in ScenarioStatus:
            raise TypeError("The scenario status must be a valid ScenarioStatus")
        if icon not in ScenarioIcon:
            raise TypeError("The scenario icon must be a valid ScenarioIcon")
        if is_user_defined is not None and not isinstance(is_user_defined, bool):
            raise TypeError("The is_user_defined value must be a boolean")

        self._scenario_status = scenario_status
        self._icon = icon
        self._is_user_defined = is_user_defined

        super().__init__(
            entity_id,
            name,
            status=status,
        )

    # Properties
    @property
    def scenario_status(self) -> ScenarioStatus:
        """Returns the scenario status (NOT_APPLIED, ONGOING, APPLIED)."""
        return self._scenario_status

    @scenario_status.setter
    def scenario_status(self, value: ScenarioStatus):
        """Sets the scenario status.

        Args:
            value (ScenarioStatus): the scenario status.

        Raises:
            TypeError: if the value is not a valid ScenarioStatus.
        """
        if value not in ScenarioStatus:
            raise TypeError("The scenario status must be a valid ScenarioStatus")

        self._scenario_status = value

    @property
    def icon(self) -> ScenarioIcon:
        """Returns the scenario icon type."""
        return self._icon

    @property
    def is_user_defined(self) -> bool:
        """Returns whether the scenario is user defined or not."""
        return self._is_user_defined

    def __str__(self) -> str:
        return (
            f'{type(self).__name__} #{self.id}: "{self.name}" - '
            f"Status: {self.status.name} - "
            f"Scenario status: {self.scenario_status.name} - "
            f"Icon: {self.icon.name} - User defined: {self.is_user_defined}"
        )

    def __repr__(self) -> str:
        return (
            f'{type(self).__name__}({self.id},"{self.name}",'
            f"status={self.status},scenario_status={self.scenario_status},"
            f"icon={self.icon},is_user_defined={self.is_user_defined})"
        )

    @staticmethod
    def from_json(json_data: dict):
        """Creates a Scenario object from a JSON dictionary.

        Example of JSON input:
        {
            "name":	"Close all openings",
            "id":	6,
            "status":	0,
            "scenario_status":	0,
            "icon_id":	23,
            "user-defined":	0
        }

        All the properties except "id" are optional, and they are set
        to their default values (name="Unknown", status=OFF,
        scenario_status=NOT_APPLIED, icon=UNKNOWN, user-defined=False).

        Any other JSON property (like floor_ind, room_ind) is ignored.

        :param json_data: the JSON dictionary representing the scenario.

        :raises KeyError: if the JSON dictionary doesn't contain the "id".
        """

        return Scenario(
            entity_id=json_data["id"],
            name=(
                json_data["name"] if "name" in json_data else CameEntity._DEFAULT_NAME
            ),
            status=(
                EntityStatus(json_data["status"])
                if "status" in json_data and json_data["status"] in EntityStatus
                else Scenario._DEFAULT_STATUS
            ),
            scenario_status=(
                ScenarioStatus(json_data["scenario_status"])
                if "scenario_status" in json_data
                and json_data["scenario_status"] in ScenarioStatus
                else Scenario._DEFAULT_SCENARIO_STATUS
            ),
            icon=(
                ScenarioIcon(json_data["icon_id"])
                if "icon_id" in json_data and json_data["icon_id"] in ScenarioIcon
                else Scenario._DEFAULT_ICON_ID
            ),
            is_user_defined=(
                bool(json_data["user-defined"])
                if "user-defined" in json_data
                and isinstance(json_data["user-defined"], int)
                else False
            ),
        )
