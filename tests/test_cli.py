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
This module contains the tests for the CLI.
"""

from came_domotic_unofficial import CameETIDomoServer


def test_main():
    """
    Test the main function of the CLI.
    """

    try:
        server = CameETIDomoServer("192.168.0.0")
        server.login("user", "pwd")
        server.update_lists()

        for feature in server.items:
            print(f'Feature "{feature}" has {len(feature)} elements.')

        return
    except Exception as e:
        print(f"Error: {e}")
        return

    # Perform actions on the server instance
    # For example, if CameETIDomoServer has a method named 'start':
    # server.start()
