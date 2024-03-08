<!-- Copyright 2024 - GitHub user: fredericks1982

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.  -->

![Code formatter: black](https://img.shields.io/badge/code%20style-black-000000.svg)
[![Linter: pylint](https://img.shields.io/badge/linting-pylint-yellowgreen)](https://github.com/pylint-dev/pylint)
![Type checker: mypy](https://img.shields.io/badge/type%20checking-mypy-yellowgreen.svg)
![Security: Bandit](https://img.shields.io/badge/security-bandit-0cc.svg)
![Unit testing: pytest](https://img.shields.io/badge/testing-pytest-0A0.svg)
![Code quality checks](https://github.com/camedomotic-unofficial/came_domotic_unofficial/actions/workflows/code-quality.yml/badge.svg)
[![Code coverage: codecov](https://codecov.io/gh/camedomotic-unofficial/came_domotic_unofficial/graph/badge.svg?token=0QSJYP7EP3)](https://codecov.io/gh/camedomotic-unofficial/came_domotic_unofficial)
[![SonarCloud - Maintainability Rating](https://sonarcloud.io/api/project_badges/measure?project=camedomotic-unofficial_came_domotic_unofficial&metric=sqale_rating)](https://sonarcloud.io/summary/new_code?id=camedomotic-unofficial_came_domotic_unofficial)
[![SonarCloud - Technical Debt](https://sonarcloud.io/api/project_badges/measure?project=camedomotic-unofficial_came_domotic_unofficial&metric=sqale_index)](https://sonarcloud.io/summary/new_code?id=camedomotic-unofficial_came_domotic_unofficial)

# Contributing to Our Project

Thank you for your interest in contributing to our project! We welcome contributions from everyone. This document provides some guidelines for contributing.

## Development Environment

We use 4 spaces for indentation. Our code is formatted with [Black](https://black.readthedocs.io/en/stable/), linted with [Pylint](https://www.pylint.org/), and type-checked with [Mypy](http://mypy-lang.org/). We write tests with [pytest](https://docs.pytest.org/en/latest/).

Before submitting a pull request, please make sure your code is formatted, linted, type-checked, and all tests pass.

## Branch Naming Convention

To allow proper autolabeling of changes, please name your branches as follows:

- `feature/*` or `features/*`: for feature enhancements or new features
- `fix/*`: for fixes to existing features
- `test/*` or `tests/*`: for changes to the unit tests or their configuration
- `doc/*` or `docs/*`: for changes to the documentation
- `action/*` or `actions/*`: for changes to the CI/CD pipelines
- `chore/*`: for any other change not directly related to a user feature

## Submitting a Pull Request

1. Fork the repository and create your branch from `main`.
2. If you've added code, add tests. Make sure all tests pass.
3. If you've changed the public interface of this library, update the documentation.
4. Ensure your code is formatted with Black, linted with Pylint, and type-checked with Mypy.
5. Issue your pull request!

## Reporting a Bug

We use GitHub issues to track bugs. Report a bug by [opening a new issue](https://github.com/camedomotic-unofficial/came_domotic_unofficial/issues); it's that easy!

## License

By contributing, you agree that your contributions will be licensed under the same license as the project.

## Code of Conduct

In the interest of fostering an open and welcoming environment, we as contributors and maintainers pledge to making participation in our project and our community a harassment-free experience for everyone. Please refer to our [Code of Conduct](CODE_OF_CONDUCT.md) for details.

## Contact

If you have any questions or concerns, please feel free to contact the maintainers.

Thank you for contributing!
