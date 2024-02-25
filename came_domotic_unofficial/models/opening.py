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

"""This module contains the class representing a CAME opening."""

from typing import Optional
from .came_entity import CameEntity
from .enums import EntityStatus, OpeningType


class Opening(CameEntity):
    """Represents a CAME opening.

    The Opening class is a subclass of the CameEntity class, and it's used to
    represent a CAME opening (e.g. a cover).

    :property id: the opening ID.
    :property name: the opening name.
    :property status: the opening status (OPEN, CLOSED or STOPPED).
    :property opening_type: the opening type (OPEN_CLOSE).
    :property close_entity_id: the closing entity ID.
    :property partial_openings: the list of partial openings.

    :method from_json: create an Opening object from a JSON dictionary.
    """

    _DEFAULT_STATUS = EntityStatus.UNKNOWN
    _DEFAULT_OPENING_TYPE = OpeningType.OPEN_CLOSE

    def __init__(
        self,
        entity_id: int,
        name: Optional[str] = CameEntity._DEFAULT_NAME,
        *,
        status: EntityStatus = _DEFAULT_STATUS,
        close_entity_id: Optional[int] = None,
        opening_type: OpeningType = _DEFAULT_OPENING_TYPE,
        partial_openings: Optional[list] = None,
    ):
        """
        Constructor for the Came Opening class.

        :param entity_id: the opening ID.
        :param close_entity_id: the closing ID (default: same as entity_id).
        :param name: the opening name.
        :param status: the opening status (default: UNKNOWN).
        :param opening_type: the opening type (default: OPEN_CLOSE).
        :param partial_openings: the list of partial openings (default: empty).
        """

        # Input validation
        if close_entity_id is not None and not isinstance(close_entity_id, int):
            raise TypeError("The closing entity ID must be an integer")
        if opening_type not in OpeningType:
            raise TypeError("The opening type must be a valid OpeningType")
        if partial_openings is not None and not isinstance(partial_openings, list):
            raise TypeError("The partial openings must be a list")

        self._close_entity_id = close_entity_id if close_entity_id else entity_id
        self._opening_type = (
            opening_type if opening_type else self._DEFAULT_OPENING_TYPE
        )
        self._partial_openings = partial_openings if partial_openings else []

        super().__init__(
            entity_id,
            name,
            status=status,
        )

    # Properties
    @property
    def opening_type(self) -> OpeningType:
        """Returns the cover type."""
        return self._opening_type

    @property
    def close_entity_id(self) -> int:
        """Returns the closing entity ID."""
        return self._close_entity_id

    @property
    def partial_openings(self) -> list:
        """Returns the list of partial openings."""
        return self._partial_openings

    # TODO Implement partial_openings management (once examples are available)
    # @partial_openings.setter
    # def partial_openings(self, value: list):
    #     """Sets the list of partial openings."""
    #     self._partial_openings = value

    def __str__(self) -> str:
        return (
            f"{type(self).__name__} #{self.id}/{self.close_entity_id}: "
            f'"{self.name}" - Type: {self.opening_type.name} - '
            f"Status: {self.status.name} - Partials: {self.partial_openings}"
        )

    def __repr__(self) -> str:
        return (
            f'{type(self).__name__}({self.id},"{self.name}",'
            f"close_entity_id={self.close_entity_id},status={self.status},"
            f"opening_type={self.opening_type},"
            f"partial_openings={self.partial_openings})"
        )

    @staticmethod
    def from_json(json_data: dict):
        """
        Creates an Opening object from a JSON dictionary.

        Example of JSON input:
        {
            "open_act_id": 26,
            "close_act_id": 27,
            "name": "My opening",
            "status": 0,
            "partial": [],
            "type": 0
        }

        All the properties except "open_act_id" are optional, and they are set
        to their default values (name="Unknown", status=OFF, type=OPEN_CLOSE).

        Any other JSON property (like floor_ind, room_ind) is ignored.

        :param json_data: the JSON dictionary representing the opening.

        :raises KeyError: if the JSON dictionary doesn't contain the "open_act_id".
        """

        return Opening(
            entity_id=json_data["open_act_id"],
            close_entity_id=(
                json_data["close_act_id"]
                if "close_act_id" in json_data
                and isinstance(json_data["close_act_id"], int)
                else json_data["open_act_id"]
            ),
            name=(
                json_data["name"]
                if "name" in json_data and isinstance(json_data["name"], str)
                else CameEntity._DEFAULT_NAME
            ),
            status=(
                EntityStatus(json_data["status"])
                if "status" in json_data
                and json_data["status"]
                in EntityStatus._value2member_map_  # pylint: disable=protected-access
                else Opening._DEFAULT_STATUS
            ),
            opening_type=(
                OpeningType(json_data["type"])
                if "type" in json_data
                and json_data["type"]
                in OpeningType._value2member_map_  # pylint: disable=protected-access
                else Opening._DEFAULT_OPENING_TYPE
            ),
            partial_openings=(
                json_data["partial"]
                if "partial" in json_data and isinstance(json_data["partial"], list)
                else None
            ),
        )
