import json
import pytest
from click.testing import CliRunner
from batteryGaugeRESTCLI import cli  # Adjust this import based on your directory structure
import requests
from unittest.mock import patch

API_URL = "http://localhost:8000"

@pytest.fixture
def runner():
    """Create a Click test runner."""
    return CliRunner()

def test_create_token_success(runner, requests_mock):
    """Test the create_token command for successful token generation."""
    # Mock the API response
    mock_data = {"user": "test_user"}
    token = "test_token"
    requests_mock.post(f"{API_URL}/token", json={"token": token}, status_code=200)

    result = runner.invoke(cli, ['create-token', json.dumps(mock_data)])

    assert result.exit_code == 0
    assert "Token: test_token" in result.output

def test_create_token_failure(runner, requests_mock):
    """Test the create_token command for failed token generation."""
    mock_data = {"user": "test_user"}
    requests_mock.post(f"{API_URL}/token", json={"detail": "Invalid data"}, status_code=400)

    result = runner.invoke(cli, ['create-token', json.dumps(mock_data)])

    assert result.exit_code != 0
    assert "Error: Invalid data" in result.output

def test_verify_token_success(runner, requests_mock):
    """Test the verify_token command for successful token verification."""
    token = "test_token"
    mock_payload = {"user": "test_user", "exp": "some_expiration"}
    requests_mock.post(f"{API_URL}/verify", json=mock_payload, status_code=200)

    result = runner.invoke(cli, ['verify-token', token])

    assert result.exit_code == 0
    assert f"Payload: {mock_payload}" in result.output

def test_verify_token_failure(runner, requests_mock):
    """Test the verify_token command for failed token verification."""
    token = "invalid_token"
    requests_mock.post(f"{API_URL}/verify", json={"detail": "Invalid token"}, status_code=401)

    result = runner.invoke(cli, ['verify-token', token])

    assert result.exit_code != 0
    assert "Error: Invalid token" in result.output
