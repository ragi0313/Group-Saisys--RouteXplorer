# Testing Strategy & Guide
## Group-Saisys Project

**Document Version**: 1.0  
**Last Updated**: December 7, 2025  
**Status**: ACTIVE

---

## Table of Contents

1. [Testing Overview](#testing-overview)
2. [Test Structure](#test-structure)
3. [Running Tests](#running-tests)
4. [Writing Tests](#writing-tests)
5. [Code Coverage](#code-coverage)
6. [Test Fixtures and Mocking](#test-fixtures-and-mocking)
7. [CI/CD Testing](#cicd-testing)
8. [Best Practices](#best-practices)

---

## Testing Overview

### Testing Pyramid

```
         /\
        /  \
       / E2E \        End-to-End Tests (5%)
      /______\       - Full application flow
      /      \
     / Integ \       Integration Tests (15%)
    /________\       - Component interactions
    /        \
   /  Unit   \       Unit Tests (80%)
  /__________\       - Individual functions
```

### Test Objectives

- ✅ **Prevent Regressions**: Catch breaking changes early
- ✅ **Document Behavior**: Tests show how functions should work
- ✅ **Enable Refactoring**: Safe to improve code without fear
- ✅ **Catch Edge Cases**: Test boundary conditions
- ✅ **Ensure Quality**: Maintain code standards
- ✅ **Reduce Bugs**: Find issues before production

### Coverage Goals

| Component | Target Coverage | Rationale |
|-----------|-----------------|-----------|
| Core Calculations | 95%+ | Critical for accuracy |
| API Functions | 85%+ | Mock external dependencies |
| UI Code | 60%+ | GUI testing difficult |
| Error Handlers | 90%+ | Must handle all failure modes |
| **Overall** | **80%+** | Industry standard |

---

## Test Structure

### Directory Layout

```
Group-Saisys/
├── tests/
│   ├── conftest.py                 # Fixtures & test config
│   ├── test_graphhopper.py         # Main test suite
│   ├── __init__.py                 # Package marker
│   └── fixtures/                   # Test data files
│       ├── mock_responses.json
│       └── sample_locations.json
├── graphhopper.py                  # Application code
├── pytest.ini                       # Pytest config
├── .flake8                          # Linting config
└── pyproject.toml                   # Tool config
```

### Test Module Organization

`tests/test_graphhopper.py` is organized by functionality:

```python
# Class-based organization for clarity

class TestKmToMiles:
    """Tests for distance conversion."""
    def test_km_to_miles_basic(self): ...
    def test_km_to_miles_zero(self): ...
    def test_km_to_miles_large_distance(self): ...

class TestFormatDuration:
    """Tests for duration formatting."""
    def test_format_duration_seconds_only(self): ...
    def test_format_duration_minutes_and_seconds(self): ...

class TestGeocoding:
    """Tests for location geocoding."""
    def test_geocode_successful_manila(self): ...
    def test_geocode_no_results(self): ...
    def test_geocode_connection_error(self): ...

class TestFuelCostCalculation:
    """Tests for fuel cost calculations."""
    def test_fuel_cost_basic(self): ...
    def test_fuel_cost_short_distance(self): ...

# ... more test classes
```

---

## Running Tests

### Basic Test Execution

```bash
# Run all tests
pytest tests/

# Run with verbose output
pytest tests/ -v

# Run specific test file
pytest tests/test_graphhopper.py

# Run specific test class
pytest tests/test_graphhopper.py::TestGeocoding

# Run specific test function
pytest tests/test_graphhopper.py::TestGeocoding::test_geocode_successful_manila
```

### Advanced Test Running

```bash
# Run tests matching a pattern
pytest tests/ -k "geocod"  # Runs all tests with 'geocod' in name

# Run tests with coverage
pytest tests/ --cov --cov-report=html --cov-report=term-missing

# Run tests in parallel (faster)
pytest tests/ -n auto  # Requires pytest-xdist

# Run with detailed output
pytest tests/ -vv --tb=long

# Run up to first 2 failures, then stop
pytest tests/ -x --maxfail=2

# Run only tests marked as 'slow'
pytest tests/ -m slow

# Run tests in random order (catch test dependencies)
pytest tests/ --random-order
```

### Coverage Reports

```bash
# Generate HTML coverage report
pytest tests/ --cov --cov-report=html
# Opens: htmlcov/index.html

# View coverage in terminal
pytest tests/ --cov --cov-report=term-missing
# Shows which lines aren't covered

# Coverage with percentage threshold
pytest tests/ --cov --cov-fail-under=80
# Fails if coverage < 80%
```

---

## Writing Tests

### Test Anatomy

Every test should follow AAA pattern:

```python
def test_feature_behavior():
    """Clear description of what is being tested."""
    # ARRANGE: Set up test data and conditions
    input_distance = 100
    expected_fuel = 7.0
    
    # ACT: Execute the function being tested
    actual_fuel = calculate_fuel_consumption(
        distance_km=input_distance,
        efficiency=7.0
    )
    
    # ASSERT: Verify the result
    assert actual_fuel == expected_fuel
```

### Naming Conventions

```python
# GOOD: Clear, descriptive names
def test_fuel_cost_calculation_returns_correct_value_for_100km():
    ...

def test_geocode_returns_error_for_invalid_location():
    ...

# ALSO GOOD: Shorter with docstring
def test_geocode_invalid_location(self):
    """Geocoding invalid location raises appropriate error."""
    ...

# AVOID: Unclear names
def test_1():  # What is being tested?
    ...

def test_function():  # Too generic
    ...
```

### Testing Different Scenarios

```python
class TestFuelCalculation:
    """Comprehensive tests for fuel calculation."""
    
    def test_zero_distance(self):
        """Test edge case: zero distance."""
        assert calculate_fuel(0) == 0
    
    def test_small_distance(self):
        """Test with small distance."""
        assert calculate_fuel(10) == 0.7
    
    def test_large_distance(self):
        """Test with large distance."""
        assert calculate_fuel(1000) == 70.0
    
    def test_negative_distance(self):
        """Test invalid input: negative distance."""
        with pytest.raises(ValueError):
            calculate_fuel(-10)
    
    def test_invalid_type(self):
        """Test invalid input: wrong type."""
        with pytest.raises(TypeError):
            calculate_fuel("100")
```

### Using Assertions Effectively

```python
# GOOD: Specific assertions
assert actual == expected
assert 99 < result < 101  # Allow for floating point error

# BETTER: Use approximation for floats
assert abs(result - 3.14159) < 0.0001

# BETTER: Explicit error message
assert fuel_cost > 0, "Fuel cost must be positive"

# AVOID: Vague assertions
assert fuel_cost  # Is this checking truthiness?

# AVOID: Multiple assertions in one test
assert geocode_result["lat"] == 14.5
assert geocode_result["lng"] == 120.9
# ↑ If first fails, second won't run
# ↑ Split into separate tests

# GOOD: One assertion concept per test
def test_geocode_returns_correct_latitude(self):
    result = geocode("Manila")
    assert abs(result["lat"] - 14.5994) < 0.001

def test_geocode_returns_correct_longitude(self):
    result = geocode("Manila")
    assert abs(result["lng"] - 120.9842) < 0.001
```

### Parametrized Tests

```python
import pytest

class TestDistanceConversion:
    """Test multiple inputs with parametrize."""
    
    @pytest.mark.parametrize("km,expected_miles", [
        (0, 0),
        (1, 0.621371),
        (10, 6.21371),
        (100, 62.1371),
        (1000, 621.371),
    ])
    def test_km_to_miles_conversions(self, km, expected_miles):
        result = km_to_miles(km)
        assert abs(result - expected_miles) < 0.001

# Benefits:
# - Test multiple inputs concisely
# - Each input runs as separate test
# - Easy to add new test cases
# - Better error reporting
```

---

## Code Coverage

### Understanding Coverage

```
Coverage = Lines of code executed during tests / Total lines of code
Target: 80%+ for production code

Types of coverage:
- Line coverage: Was line executed?
- Branch coverage: All if/else branches?
- Function coverage: All functions tested?
- Statement coverage: All statements executed?
```

### Viewing Coverage Reports

```bash
# Generate and open HTML report
pytest tests/ --cov --cov-report=html
open htmlcov/index.html  # or start htmlcov/index.html on Windows

# Terminal report
pytest tests/ --cov --cov-report=term-missing

# Example output:
# Name                        Stmts   Miss  Cover   Missing
# ────────────────────────────────────────────────────
# graphhopper.py               150     18    88%    45-52, 89, 102
# tests/conftest.py             60      0   100%
# tests/test_graphhopper.py    350      5    99%    456
# ────────────────────────────────────────────────────
# TOTAL                         560     23    96%
```

### Improving Coverage

1. **Identify uncovered lines**:
   ```bash
   pytest tests/ --cov --cov-report=term-missing
   # Look at "Missing" column
   ```

2. **Write tests for uncovered lines**:
   ```python
   def test_missing_error_handler(self):
       # Test the 45-52 lines that aren't covered
       with pytest.raises(APIError):
           geocode("")
   ```

3. **Use coverage pragmas for intentional exclusion**:
   ```python
   if __name__ == "__main__":  # pragma: no cover
       main()
   ```

---

## Test Fixtures and Mocking

### Using Fixtures from conftest.py

```python
# conftest.py provides pre-built fixtures

def test_geocoding_with_fixture(mock_geocode_response_valid):
    """Use mock response fixture."""
    data = mock_geocode_response_valid
    
    # Extract values
    lat = data["hits"][0]["point"]["lat"]
    lng = data["hits"][0]["point"]["lng"]
    
    assert lat == 14.5994
    assert lng == 120.9842

def test_route_with_fixture(mock_route_response):
    """Use route response fixture."""
    path = mock_route_response["paths"][0]
    
    distance_m = path["distance"]
    instructions = path["instructions"]
    
    assert distance_m == 15000.5
    assert len(instructions) == 3
```

### Creating New Fixtures

```python
# In conftest.py or test file

import pytest

@pytest.fixture
def custom_location_data():
    """Fixture that provides test location data."""
    return {
        "origin": "Makati, Philippines",
        "destination": "Bonifacio, Philippines",
        "distance_km": 15,
    }

# Use in tests
def test_with_custom_data(custom_location_data):
    assert custom_location_data["distance_km"] > 0
```

### Mocking External Dependencies

```python
from unittest.mock import patch, Mock

def test_geocode_with_mock(self):
    """Mock API call instead of making real request."""
    with patch("requests.get") as mock_get:
        # Set up mock response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "hits": [{"point": {"lat": 14.5, "lng": 120.9}}]
        }
        mock_get.return_value = mock_response
        
        # Call function (will use mock)
        result = geocode("Manila")
        
        # Verify mock was called
        mock_get.assert_called_once()
        assert result["lat"] == 14.5
```

### Fixture Scopes

```python
@pytest.fixture(scope="function")  # Default: recreated for each test
def small_fixture():
    return setup()

@pytest.fixture(scope="class")     # Recreated for each test class
def medium_fixture():
    return setup()

@pytest.fixture(scope="module")    # Recreated for each test module
def large_fixture():
    return setup()

@pytest.fixture(scope="session")   # Recreated once per test session
def huge_fixture():
    return setup()
```

---

## CI/CD Testing

### Automated Testing on GitHub

The `.github/workflows/ci-cd.yml` runs tests automatically:

1. **When**: Every push and pull request
2. **Python Versions**: 3.8, 3.9, 3.10, 3.11
3. **Coverage**: Uploaded to Codecov
4. **Results**: Posted to PR

### Local Testing Before Push

```bash
# Run full test suite locally first
pytest tests/ -v --cov

# Or use pre-commit to catch issues before commit
pre-commit run --all-files

# Review output for any failures
# Fix any issues before pushing
git push origin feature-branch
```

### Interpreting CI Results

**All Green ✅**: All tests passed, code ready to merge

**Red ❌ Test Failed**: 
```
1. Pull latest code: git pull origin main
2. Run tests locally: pytest tests/ -v
3. Fix failing test or code
4. Push fix: git push origin feature-branch
```

**Orange ⚠️ Coverage Below Threshold**:
```
1. Generate coverage report: pytest tests/ --cov-report=html
2. Open htmlcov/index.html
3. Add tests for uncovered lines
4. Re-run tests to verify
```

---

## Best Practices

### DO ✅

- ✅ Write tests **before** or **while** writing code (TDD)
- ✅ Test behavior, not implementation
- ✅ Use descriptive test names
- ✅ Keep tests simple and focused
- ✅ Mock external dependencies (APIs, databases)
- ✅ Test both happy path and error cases
- ✅ Use fixtures for shared test data
- ✅ Maintain 80%+ code coverage
- ✅ Run tests locally before pushing
- ✅ Review test coverage reports regularly

### DON'T ❌

- ❌ Skip testing because "it's too much work"
- ❌ Write tests that depend on each other
- ❌ Make actual API calls in tests (use mocks)
- ❌ Use sleep() to wait for things
- ❌ Test implementation details, test behavior
- ❌ Write overly complex tests
- ❌ Leave skipped tests without explanation
- ❌ Commit code with failing tests
- ❌ Ignore coverage reports
- ❌ Test the framework (pytest, requests, etc.)

### Test-Driven Development (TDD) Workflow

```
1. Write failing test
   pytest tests/ -v  # Red ❌

2. Write minimal code to pass test
   pytest tests/ -v  # Green ✅

3. Refactor code while keeping tests passing
   pytest tests/ -v  # Still Green ✅

4. Repeat until feature complete
```

---

## Example: Complete Test Suite

```python
# tests/test_feature.py
import pytest
from unittest.mock import patch, Mock

class TestNewFeature:
    """Test suite for new feature."""
    
    @pytest.fixture
    def setup_data(self):
        """Set up test data."""
        return {
            "input": 100,
            "expected": 50,
        }
    
    def test_basic_functionality(self, setup_data):
        """Test basic feature behavior."""
        result = new_feature(setup_data["input"])
        assert result == setup_data["expected"]
    
    def test_zero_input(self):
        """Test edge case: zero input."""
        assert new_feature(0) == 0
    
    def test_negative_input(self):
        """Test invalid input: negative."""
        with pytest.raises(ValueError):
            new_feature(-10)
    
    def test_with_external_api(self):
        """Test interaction with external API."""
        with patch("requests.get") as mock_get:
            mock_get.return_value.json.return_value = {"result": 42}
            
            result = new_feature_with_api(100)
            
            assert result == 42
            mock_get.assert_called_once()
    
    @pytest.mark.parametrize("input,expected", [
        (10, 5),
        (100, 50),
        (1000, 500),
    ])
    def test_multiple_inputs(self, input, expected):
        """Test multiple input/output combinations."""
        assert new_feature(input) == expected
```

---

## Resources

- [pytest Documentation](https://docs.pytest.org/)
- [unittest.mock Guide](https://docs.python.org/3/library/unittest.mock.html)
- [pytest Fixtures](https://docs.pytest.org/how-to/fixture.html)
- [pytest Parametrize](https://docs.pytest.org/how-to/parametrize.html)
- [Code Coverage Best Practices](https://martinfowler.com/bliki/TestCoverage.html)

---

**End of Testing Strategy Document**

For questions, consult the team QA lead or review test examples in `tests/test_graphhopper.py`.
