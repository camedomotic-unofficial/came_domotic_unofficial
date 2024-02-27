# Security Policy

## Supported Versions

Use this section to tell users about which versions of your project are currently being supported with security updates.

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | ✅                 |
| 0.x.    | ❌                 |

## Reporting a Vulnerability

The security of our project is a top priority. If you discover a security vulnerability within our project, we kindly ask you to follow these steps:

1. **Do Not Publicly Disclose**: Please do not open issues for vulnerabilities on GitHub or discuss them in public forums. Instead, contact us directly.
2. **Contact**: Send an email to the mantainers with a detailed description of the issue. Include steps to reproduce the vulnerability, its impact, and any other information that may help us understand the severity and urgency.
3. **Response Time**: We aim to respond to security reports as soon as possible, acknowledging receipt of your report, and will provide a timeline for the fix and disclosure process after initial investigation.

## Security Measures

Our project undergoes continuous integration and deployment (CI/CD), incorporating various security and code quality tools to ensure the safety and reliability of our codebase. Here are some of the measures and tools we use:

- **Static Code Analysis**: We use `mypy`, `pylint`, `flake8`, and `black` to enforce coding standards and identify potential issues.
- **Security Scanning**: `bandit` and `gitguardian` scan our code for security vulnerabilities and secrets, respectively.
- **Dependencies Security**: `Dependabot` scans our dependencies for known vulnerabilities and automatically creates pull requests to update them.
- **Automated Testing**: `pytest` ensures that our code behaves as expected and that new changes do not introduce regressions.

## External Audit

While we do our best to secure our project, we also believe in the power of community and external verification. We encourage security researchers and experts to audit our code and welcome any feedback or recommendations for improving our security posture.

## Acknowledgements

We appreciate the time and effort the community spends on helping us ensure the security of our project. Contributors who report vulnerabilities and help us improve our security will be acknowledged in our project's documentation (unless they prefer to remain anonymous).

Thank you for helping us keep our project safe.
