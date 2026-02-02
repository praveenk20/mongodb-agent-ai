# How to Contribute

Thanks for your interest in contributing to MongoDB Agent! Here are a few
general guidelines on contributing and reporting bugs that we ask you to review.
Following these guidelines helps to communicate that you respect the time of the
contributors managing and developing this open source project. In return, they
should reciprocate that respect in addressing your issue, assessing changes, and
helping you finalize your pull requests. In that spirit of mutual respect, we
endeavor to review incoming issues and pull requests within 10 days, and will
close any lingering issues or pull requests after 60 days of inactivity.

Please note that all of your interactions in the project are subject to our
[Code of Conduct](/CODE_OF_CONDUCT.md). This includes creation of issues or pull
requests, commenting on issues or pull requests, and extends to all interactions
in any real-time space e.g., Slack, Discord, etc.

## How to Contribute

## Reporting Issues

Before reporting a new issue, please ensure that the issue was not already
reported or fixed by searching through our
[issues list](https://github.com/prakalam/mongodb-agent-public/issues).

When creating a new issue, please be sure to include a **title and clear
description**, as much relevant information as possible, and, if possible, a
test case.

**If you discover a security bug, please do not report it through GitHub.
Instead, please see security procedures in [SECURITY.md](/SECURITY.md).**

## Sending Pull Requests

Before sending a new pull request, take a look at existing pull requests and
issues to see if the proposed change or fix has been discussed in the past, or
if the change was already implemented but not yet released.

We expect new pull requests to include tests for any affected behavior, and, as
we follow semantic versioning, we may reserve breaking changes until the next
major version release.

### Pull Request Process

1. Ensure any install or build dependencies are removed before the end of the layer when doing a build
2. Update the README.md or documentation with details of changes if applicable
3. Follow the existing code style and conventions
4. Add tests for new functionality
5. Ensure all tests pass
6. Your PR will be reviewed by maintainers who may request changes

### Coding Standards

- Follow PEP 8 style guide for Python code
- Write clear, self-documenting code with appropriate comments
- Include docstrings for all functions, classes, and modules
- Keep functions focused and concise
- Write meaningful variable and function names

### Testing

We have a comprehensive test suite to ensure code quality and functionality. All contributions must include appropriate tests.

#### Test Requirements

Before submitting a pull request, ensure that:
1. All existing tests pass
2. New features include unit tests
3. Code coverage remains above 80%
4. Integration tests are added for new workflows

#### Running Tests

Install test dependencies:
```bash
pip install -e ".[dev]"
```

Run all tests:
```bash
pytest
```

Run tests with coverage:
```bash
pytest --cov=mongodb_agent --cov-report=html
```

Run specific test file:
```bash
pytest tests/test_agent.py
```

Run with verbose output:
```bash
pytest -v
```

Run only integration tests:
```bash
pytest -m integration
```

#### Test Structure

Our test suite is organized as follows:
- `tests/test_agent.py` - Core agent functionality tests
- `tests/test_query_executor.py` - Query execution tests
- `tests/test_router.py` - Routing logic tests
- `tests/test_selector.py` - Semantic model selection tests
- `tests/test_query_refiner.py` - Query refinement tests
- `tests/test_output_parser.py` - Output parsing tests
- `tests/test_integration.py` - End-to-end integration tests

#### Writing Tests

When writing tests:
- Use fixtures from `tests/conftest.py` for common test objects
- Mock external dependencies (MongoDB, LLM providers)
- Test both success and error cases
- Include docstrings explaining what each test validates
- Follow the naming convention: `test_<functionality>_<scenario>()`

Example:
```python
def test_query_executor_handles_timeout(mock_mongodb_client):
    """Test that query executor handles timeout gracefully."""
    # Test implementation
    pass
```

## Other Ways to Contribute

We welcome anyone that wants to contribute to MongoDB Agent to triage and
reply to open issues to help troubleshoot and fix existing bugs. Here is what
you can do:

- Help ensure that existing issues follows the recommendations from the
  _[Reporting Issues](#reporting-issues)_ section, providing feedback to the
  issue's author on what might be missing.
- Review and update the existing content of our documentation with up-to-date
  instructions and code samples.
- Review existing pull requests, and testing patches against real existing
  applications that use MongoDB Agent.
- Write a test, or add a missing test case to an existing test.

Thanks again for your interest on contributing to MongoDB Agent!

:heart:

