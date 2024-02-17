<!-- 
Copyright 2024 - GitHub user: fredericks1982

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License. 
-->

# "CAME Domotic unofficial" library

Library to interact with a CAME ETI/Domo domotic server.

## Currently supported entities

- **Lights**: get list, switch on/off, set brightness (if dimmable).
- **Openings**: get list, close, stop, open.
- **Scenarios**: get list, activate.

## Usage

This library manages the remote session automatically, so you don't need to perform an explicit login/logout or to manage the session expiration: just use the `CameETIDomoServer` object within a `with` statement, to ensure that the resources are properly disposed.

The library will login to the CAME server only when you actually need to interact with it, and manages automatically the session expiration/renewal. If you really need it, you can always check if there is an active session testing the attribute `is_authenticated`.

Here follow some tipical usage examples.

### Basic usage

Declare the server object within a `with` statement and perform some action, like getting the unique ID of the server.

```python
with CameETIDomoServer(
    "192.168.0.3", 
    "username", 
    "password"
    ) as domo:

    if not domo.is_authenticated:
        print("Not authenticated, I don't need it yet.")

    # Get the CAME server unique ID
    server_unique_id = domo.keycode

    if domo.is_authenticated:
        print("Now I am authenticated, since I needed to ask the server some info.")
```

### Retrieve some data from the server

```python
with CameETIDomoServer(
    "192.168.0.3", 
    "username", 
    "password"
    ) as domo:

    # Get the list of features supported by the CAME server
    features = domo.get_features()

    # Get the list of all the entities configured on the CAME server (lights, openings, scenarios, etc.)
    all_my_entites = domo.get_entities()

    # Get only a subset by entity type
    my_lights = domo.get_entities(EntityType.LIGHTS)
    my_openings = domo.get_entities(EntityType.OPENINGS)
    my_scenarios = domo.get_entities(EntityType.SCENARIOS)


    # Get a specific entity
    my_dimmable_lamp = my_lights[0]
    kitchen_opening = my_openings[0]
    close_all_openings = my_scenarios[0]
```

### Set the status of an entity

```python
    # Switch on a light and set its brightness
    if domo.set_entity_status(
        Light, 
        my_dimmable_lamp.id, 
        EntityStatus.ON_OPEN, 
        brightness=80
    ):
        print("Light switched on as expected.")
    else:
        print("Failure while trying to switch on the light.")

    # Close an opening
    if domo.set_entity_status(
        Opening, 
        kitchen_opening.id, 
        EntityStatus.CLOSED):
        print("Kitchen opening closed.")
    else:
        print("Failure while trying to close the opening.")

    # Activate a scenario
    if domo.set_entity_status(Scenario, close_all_openings.id):
        print("Scenario activated.")
    else:
        print("Failure while trying to activate the scenario.")
```

## Acknowledgments

Special thanks to Andrea Michielan for his [eti_domo](https://github.com/andrea-michielan/eti_domo) library,
which significantly facilitated the development process of this library.
His work was very helpful and greatly appreciated.

## Disclaimer

This library is not affiliated with or endorsed or supported
by [CAME](https://www.came.com/). Use at your own risk.

**Important:** This library is currently in a pre-alpha development state.
It is not yet stable and should be used only for studying purposes.
Please be aware that you cannot rely on it for any production use.
Use at your own risk.
