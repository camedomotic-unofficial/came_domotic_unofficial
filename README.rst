.. Copyright 2024 - GitHub user: fredericks1982

.. Licensed under the Apache License, Version 2.0 (the "License");
.. you may not use this file except in compliance with the License.
.. You may obtain a copy of the License at

..     http://www.apache.org/licenses/LICENSE-2.0

.. Unless required by applicable law or agreed to in writing, software
.. distributed under the License is distributed on an "AS IS" BASIS,
.. WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
.. See the License for the specific language governing permissions and
.. limitations under the License.

.. image:: https://badge.fury.io/py/came_domotic_unofficial.svg
   :target: https://pypi.org/project/came_domotic_unofficial/
   :alt: PyPI version

.. image:: https://img.shields.io/badge/python-3.12-417fb0.svg
    :target: https://www.python.org
    :alt: Python 3.12

.. .. image:: https://github.com/camedomotic-unofficial/came_domotic_unofficial/actions/workflows/code-quality.yml/badge.svg
..    :target: https://github.com/camedomotic-unofficial/came_domotic_unofficial/actions/workflows/code-quality.yml
..    :alt: Code quality check

.. .. image:: https://github.com/camedomotic-unofficial/came_domotic_unofficial/actions/workflows/github-code-scanning/codeql/badge.svg
..     :target: https://github.com/camedomotic-unofficial/came_domotic_unofficial/actions/workflows/github-code-scanning/codeql
..     :alt: CodeQL

.. image:: https://sonarcloud.io/api/project_badges/measure?project=camedomotic-unofficial_came_domotic_unofficial&metric=security_rating
   :target: https://sonarcloud.io/project/overview?id=camedomotic-unofficial_came_domotic_unofficial
   :alt: SonarCloud - Security Rating

.. .. image:: https://sonarcloud.io/api/project_badges/measure?project=camedomotic-unofficial_came_domotic_unofficial&metric=sqale_rating
..    :target: https://sonarcloud.io/project/overview?id=camedomotic-unofficial_came_domotic_unofficial
..    :alt: SonarCloud - Maintainability Rating

.. .. image:: https://codecov.io/gh/camedomotic-unofficial/came_domotic_unofficial/graph/badge.svg?token=0QSJYP7EP3 
..    :target: https://codecov.io/gh/camedomotic-unofficial/came_domotic_unofficial
..    :alt: Code coverage

.. image:: https://sonarcloud.io/api/project_badges/measure?project=camedomotic-unofficial_came_domotic_unofficial&metric=vulnerabilities
   :target: https://sonarcloud.io/project/overview?id=camedomotic-unofficial_came_domotic_unofficial
   :alt: SonarCloud - Vulnerabilities

.. image:: https://sonarcloud.io/api/project_badges/measure?project=camedomotic-unofficial_came_domotic_unofficial&metric=bugs
   :target: https://sonarcloud.io/project/overview?id=camedomotic-unofficial_came_domotic_unofficial
   :alt: SonarCloud - Bugs

.. image:: https://readthedocs.org/projects/came-domotic-unofficial/badge/?version=latest
   :target: https://came-domotic-unofficial.readthedocs.io/en/latest/?badge=latest
   :alt: Documentation status

.. .. image:: https://img.shields.io/badge/license-Apache%202.0-blue.svg
..    :target: https://opensource.org/licenses/Apache-2.0
..    :alt: License: Apache 2.0

.. .. image:: https://sonarcloud.io/api/project_badges/measure?project=camedomotic-unofficial_came_domotic_unofficial&metric=alert_status
..    :target: https://sonarcloud.io/project/overview?id=camedomotic-unofficial_came_domotic_unofficial
..    :alt: SonarCloud - Quality Gate Status

.. .. image:: https://img.shields.io/badge/typed-mypy-blue.svg
..    :target: http://mypy-lang.org/
..    :alt: Typed: mypy

.. .. image:: https://img.shields.io/badge/code%20style-black-000000.svg
..    :target: https://github.com/psf/black
..    :alt: Code style: black

.. .. image:: https://img.shields.io/badge/code%20style-flake8-green.svg
..    :target: https://flake8.pycqa.org/
..    :alt: Code style: flake8

.. .. image:: https://sonarcloud.io/api/project_badges/measure?project=camedomotic-unofficial_came_domotic_unofficial&metric=duplicated_lines_density
..    :target: https://sonarcloud.io/project/overview?id=camedomotic-unofficial_came_domotic_unofficial
..    :alt: SonarCloud - Duplicated Lines (%)

.. .. image:: https://sonarcloud.io/api/project_badges/measure?project=camedomotic-unofficial_came_domotic_unofficial&metric=reliability_rating
..    :target: https://sonarcloud.io/project/overview?id=camedomotic-unofficial_came_domotic_unofficial
..    :alt: SonarCloud - Reliability Rating

.. .. image:: https://sonarcloud.io/api/project_badges/measure?project=camedomotic-unofficial_came_domotic_unofficial&metric=sqale_index
..    :target: https://sonarcloud.io/project/overview?id=camedomotic-unofficial_came_domotic_unofficial
..    :alt: SonarCloud - Technical Debt

.. .. image:: https://pepy.tech/badge/came_domotic_unofficial
..    :target: https://pepy.tech/project/came_domotic_unofficial
..    :alt: Downloads

Welcome!
========


The **CAME Domotic unofficial library** offers a streamlined Python interface for 
interacting with CAME ETI/Domo servers. Designed for both **developers and home automation 
enthusiasts**, it simplifies managing domotic devices by abstracting the complexities 
of the CAME Domotic API.

This tool is ideal for those looking to integrate CAME Domotic technology into 
`Home Assistant <https://www.home-assistant.io/>`_ or other systems, making device control 
like **lights**, **openings**, and **scenarios** straightforward and accessible, 
enabling broader integration possibilities for domotic systems.

.. warning:: 
    This library is currently in **beta development status**.
    It is not yet stable and should be used only for studying purposes.
    Please be aware that you cannot rely on it for any production use.
    Use at your own risk.

.. note:: 
    This library is independently developed and is not affiliated with, endorsed by,
    or supported by `CAME <https://www.came.com/>`_. It may not be compatible with all
    CAME Domotic systems. Use at your own risk.   

.. danger:: 

    This library is not intended for use in critical systems, such as security or 
    life-support systems. Always use official and supported tools for such applications.

Key Features
------------
- **Simplicity**: Easy interaction with domotic entities.
- **Automatic session management**: No need for manual login or session handling.
- **First of its kind**: Unique in providing integration with CAME Domotic systems.
- **Open source**: Freely available under the Apache 2.0 license, inviting
  contributions and adaptations.

Quick Start
-----------
To get started with the CAME Domotic unofficial library, install it using pip:

.. code-block:: bash

    pip install came-domotic-unofficial

Here's a quick example to show how simple it is to use:

.. code-block:: python

    from came_domotic_unofficial import CameETIDomoServer, EntityType, EntityStatus

    # Just declare the server: login and session management are automatic
    with CameETIDomoServer("192.168.x.x", "username", "password") as domo:
        
        # Get the list of all the lights configured on the CAME server
        my_lights = domo.get_entities(EntityType.LIGHTS)

        if my_lights:
            # Get a specific light by display name
            my_favourite_light = next(
                (light for light in my_lights if light.name == "My favourite light"),
                None
            )
            if my_favourite_light:
                # Turn the light on
                domo.set_entity_status(
                    Light, my_favourite_light.id, EntityStatus.ON_OPEN_TRIGGERED
                )

For **more detailed usage examples**, see 
`Usage examples <https://came-domotic-unofficial.readthedocs.io/en/latest/usage_examples.html>`_.

What's New
----------
To keep up with the latest improvements and updates, visit our 
`GitHub Releases <https://github.com/camedomotic-unofficial/came_domotic_unofficial/releases>`_
page. The release notes are updated with each new version, ensuring you're always
informed about new features and fixes.

Versioning Strategy
-------------------

Our project adheres to `Semantic Versioning (SemVer) <https://semver.org/>`_ to ensure
clarity and predictability in our release process. Our version numbers are structured
as MAJOR.MINOR.PATCH, incrementing:

- The MAJOR version when making incompatible API changes,
- The MINOR version when adding functionality in a backward-compatible manner, and
- The PATCH version when making backward-compatible bug fixes.

Post Releases
^^^^^^^^^^^^^

In addition to the standard SemVer approach, we utilize post-release versions for
immediate fixes or minor changes that do not warrant a full version increment, denoted
as `1.2.3post1`. This allows us to rapidly deploy necessary fixes or adjustments.

For more details on our versioning strategy and how contributions are managed, please
see our `Contribute to the Project <https://came-domotic-unofficial.readthedocs.io/en/latest/contributing.html>`_
page.

Contributing
------------
We welcome contributions! For guidelines on how to help, see
`Contribute to the Project <https://came-domotic-unofficial.readthedocs.io/en/latest/contributing.html>`_.

Acknowledgments
---------------
Special thanks to Andrea Michielan for his foundational work with the 
`eti_domo <https://github.com/andrea-michielan/eti_domo>`_ library, which greatly
facilitated the development of this library.

License
-------
This project is licensed under the Apache License 2.0. For more details, see the
`LICENSE <https://github.com/camedomotic-unofficial/came_domotic_unofficial/blob/main/LICENSE>`_
file.
