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
Tests of real usage of the library
"""

# from datetime import datetime

# from freezegun import freeze_time
# import requests
# import pytest
# from hypothesis import given
# from hypothesis.strategies import integers, text, sampled_from, lists

import time
from came_domotic_unofficial import (
    CameETIDomoServer,
    # CameDomoticServerNotFoundError,
)
from came_domotic_unofficial.models import (
    EntityStatus,
    EntityType,
    Light,
)


# region check standard usage


def test_check_standard_usage():
    """
    Test that the _send_command method raises a CameDomoticRequestError
    when the request raises an exception.
    """
    with CameETIDomoServer("192.168.1.3", "admin", "admin") as domo:

        assert domo.is_authenticated is False
        assert domo.keep_alive() is False

        assert len(domo.keycode) > 0
        # print(domo.keycode)

        assert domo.is_authenticated is True
        assert domo.keep_alive() is True

        features = domo.get_features()
        assert len(features) > 0
        print(features)

        entites = domo.get_entities()
        assert len(entites) > 0

        entities = domo.get_entities(EntityType.OPENINGS)
        assert len(entities) == 9
        # print(entities)

        entities = domo.get_entities(EntityType.DIGITALIN)
        assert len(entities) == 71
        # print(len(entities))
        # print(entities)

        entities = domo.get_entities(EntityType.SCENARIOS)
        assert len(entities) == 8
        # print(len(entities))

        entities = domo.get_entities(EntityType.LIGHTS)
        assert len(entities) == 29
        # print(entities)
        # print(entities[0].name)

        assert domo.set_entity_status(
            Light, 13, EntityStatus.ON_OPEN, brightness=40
        )

        time.sleep(1)

        assert domo.set_entity_status(
            Light, 13, EntityStatus.OFF_STOPPED, brightness=12
        )

        # assert domo.set_entity_status(Opening, 73, EntityStatus.CLOSED)
        # assert domo.set_entity_status(Scenario, 1)

        # time.sleep(2)

        # assert domo.set_entity_status(
        #     Light, 13, EntityStatus.OFF_STOPPED, brightness=12
        # )
        # assert domo.set_entity_status(Opening, 73, EntityStatus.OFF_STOPPED)

        # time.sleep(2)

        # assert domo.set_entity_status(Opening, 73, EntityStatus.ON_OPEN)

        # time.sleep(2)

        # assert domo.set_entity_status(Scenario, 2)

        # if domo.logout():
        #     print("Logout completed.")
        #     print(domo.is_authenticated)
        #     assert domo.is_authenticated is False
        # else:
        #     print("Logout failed!")
        #     print(domo.is_authenticated)
        #     assert domo.is_authenticated is False


# endregion
