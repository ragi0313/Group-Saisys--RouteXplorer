"""
Test configuration and shared fixtures for GraphHopper project.
Location: tests/conftest.py
"""

import pytest
import json
from unittest.mock import Mock, patch
from datetime import timedelta


# ===== MOCK DATA AND FIXTURES =====

@pytest.fixture
def mock_api_key():
    """Provide a test API key."""
    return "test-api-key-12345"


@pytest.fixture
def mock_geocode_response_valid():
    """Mock response for successful geocoding."""
    return {
        "hits": [
            {
                "point": {"lat": 14.5994, "lng": 120.9842},
                "name": "Manila",
                "state": "NCR",
                "country": "Philippines",
                "osm_value": "Manila",
            }
        ]
    }


@pytest.fixture
def mock_geocode_response_empty():
    """Mock response for geocoding with no results."""
    return {"hits": []}


@pytest.fixture
def mock_geocode_response_quezon():
    """Mock response for Quezon City geocoding."""
    return {
        "hits": [
            {
                "point": {"lat": 14.6349, "lng": 121.0388},
                "name": "Quezon City",
                "state": "NCR",
                "country": "Philippines",
                "osm_value": "Quezon City",
            }
        ]
    }


@pytest.fixture
def mock_route_response():
    """Mock response for route calculation."""
    return {
        "paths": [
            {
                "distance": 15000.5,  # meters
                "time": 1800000,  # milliseconds
                "instructions": [
                    {
                        "distance": 500,
                        "heading": 45,
                        "sign": 0,
                        "interval": [0, 1],
                        "text": "Head northeast on Roxas Boulevard",
                        "time": 30000,
                    },
                    {
                        "distance": 1200,
                        "heading": 90,
                        "sign": 2,  # Turn right
                        "interval": [1, 15],
                        "text": "Turn right onto Makati Avenue",
                        "time": 120000,
                    },
                    {
                        "distance": 13300.5,
                        "heading": 180,
                        "sign": 0,
                        "interval": [15, 45],
                        "text": "Continue straight",
                        "time": 1650000,
                    },
                ],
                "bbox": [120.9842, 14.5994, 121.0388, 14.6349],
                "snapped_waypoints": "test",
                "ascend": 50.0,
                "descend": 45.0,
                "details": {},
            }
        ]
    }


@pytest.fixture
def mock_route_response_error():
    """Mock error response for route calculation."""
    return {
        "message": "Path not found",
        "hints": ["No route found"],
    }


@pytest.fixture
def sample_location_pair():
    """Provide sample origin and destination."""
    return {
        "origin": "Manila, Philippines",
        "destination": "Quezon City, Philippines",
    }


@pytest.fixture
def expected_route_data():
    """Expected data structure after processing route response."""
    return {
        "distance_km": 15.0005,
        "distance_miles": 9.32,
        "duration_ms": 1800000,
        "duration_formatted": "00:30:00",
        "waypoints": 3,
        "origin": "Manila, NCR, Philippines",
        "destination": "Quezon City, NCR, Philippines",
    }


@pytest.fixture
def fuel_cost_params():
    """Parameters for fuel cost calculation."""
    return {
        "distance_km": 100,
        "fuel_efficiency": 7.0,  # L/100km
        "fuel_price_per_liter": 57.20,  # PHP
    }


@pytest.fixture
def expected_fuel_costs():
    """Expected fuel cost calculations."""
    return {
        "fuel_consumed_liters": 7.0,
        "fuel_cost_php": 399.4,
        "fuel_cost_per_km": 3.994,
    }


@pytest.fixture
def calorie_params():
    """Parameters for calorie calculation."""
    return {
        "distance_km": 10,
        "weight_kg": 70,
        "activity": "walking",  # or 'cycling', 'running'
    }


# ===== MOCKING UTILITIES =====

@pytest.fixture
def mock_requests_get(mock_geocode_response_valid, mock_route_response):
    """Mock requests.get for API calls."""
    with patch("requests.get") as mock_get:
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.headers = {"content-type": "application/json"}
        mock_response.json.return_value = mock_geocode_response_valid
        mock_get.return_value = mock_response
        yield mock_get


@pytest.fixture
def mock_requests_get_multiple(
    mock_geocode_response_valid,
    mock_geocode_response_quezon,
    mock_route_response,
):
    """Mock requests.get for multiple sequential calls."""
    with patch("requests.get") as mock_get:
        # Create different responses for different calls
        geocode_response = Mock()
        geocode_response.status_code = 200
        geocode_response.headers = {"content-type": "application/json"}
        geocode_response.json.return_value = mock_geocode_response_valid

        quezon_response = Mock()
        quezon_response.status_code = 200
        quezon_response.headers = {"content-type": "application/json"}
        quezon_response.json.return_value = mock_geocode_response_quezon

        route_response = Mock()
        route_response.status_code = 200
        route_response.headers = {"content-type": "application/json"}
        route_response.json.return_value = mock_route_response

        # Set up side_effect to return different values on each call
        mock_get.side_effect = [
            geocode_response,
            quezon_response,
            route_response,
        ]
        yield mock_get


@pytest.fixture
def mock_requests_get_error():
    """Mock requests.get that returns an error."""
    with patch("requests.get") as mock_get:
        mock_response = Mock()
        mock_response.status_code = 400
        mock_response.headers = {"content-type": "application/json"}
        mock_response.json.return_value = {"message": "Bad request"}
        mock_get.return_value = mock_response
        yield mock_get


@pytest.fixture
def mock_requests_timeout():
    """Mock requests.get that times out."""
    with patch("requests.get") as mock_get:
        mock_get.side_effect = Exception("Connection timeout")
        yield mock_get


# ===== CONSTANTS FOR TESTING =====

CONSTANTS = {
    "DEFAULT_GASOLINE_PHP_PER_L": 57.20,
    "DEFAULT_DIESEL_PHP_PER_L": 55.45,
    "DEFAULT_FUEL_EFF_L100": 7.0,
    "DEFAULT_WEIGHT_KG": 70.0,
    "KM_TO_MILES_FACTOR": 1.60934,
    "CALORIE_FACTORS": {
        "walking": 0.83,
        "cycling": 0.49,
        "running": 1.0,
    },
}


@pytest.fixture
def constants():
    """Provide application constants for testing."""
    return CONSTANTS
