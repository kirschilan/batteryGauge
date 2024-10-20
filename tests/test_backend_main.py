from fastapi.testclient import TestClient
from batteryGaugeBackend import app

client = TestClient(app)

# Test login functionality
def test_login_success():
    response = client.post("/login", json={"username": "test", "password": "password"})
    assert response.status_code == 200
    assert "token" in response.json()

def test_login_failure():
    response = client.post("/login", json={"username": "wronguser", "password": "wrongpass"})
    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid credentials"}

# Test battery status functionality
def test_battery_status_success():
    # First login to get the token
    login_response = client.post("/login", json={"username": "test", "password": "password"})
    token = login_response.json()["token"]

    # Use the token to access the battery status
    response = client.get("/battery_status", params={"token": token})
    assert response.status_code == 200
    data = response.json()
    assert "devices" in data
    assert len(data["devices"]) == 2

def test_battery_status_invalid_token():
    response = client.get("/battery_status", params={"token": "invalid-token"})
    assert response.status_code == 403
    assert response.json() == {"detail": "Invalid token"}
