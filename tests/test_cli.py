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

from came_domotic_unofficial import _LOGGER
from came_domotic_unofficial.client import CameDomoticServer
from came_domotic_unofficial.const import EntityType


def test_real_authenticate():
    """
    Entry point for the CLI.
    """
    server = CameDomoticServer("192.168.1.3", "my_user", "my_pwd")
    server._ensure_authentication()
    print(server._session_id)
    print(server._session_expiration_datetime)


def test_real_get_lights_list():
    """
    Entry point for the CLI.
    """
    server = CameDomoticServer("192.168.1.3", "my_user", "my_pwd")
    server._ensure_authentication()

    entities = server.get_entities(EntityType.LIGHT)

    # Print each entity
    _LOGGER.info("Printing all the entitie")

    for entity in entities:
        _LOGGER.info(entity)

    print(server._session_id)
    print(server._session_expiration_datetime)
