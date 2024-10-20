import pytest
import unittest
from unittest.mock import patch, MagicMock
from batteryGauge import DeviceManager, login_to_icloud, get_battery_from_icloud


@pytest.fixture
def device_manager():
    return DeviceManager()
'''
@pytest.fixture
def mock_api():
    api = MagicMock()
    device1 = MagicMock()
    device1.status.return_value = {'deviceDisplayName': 'iPhone', 'batteryLevel': 0.75}
    device2 = MagicMock()
    device2.status.return_value = {'deviceDisplayName': 'iPad', 'batteryLevel': 0.5}
    api.devices = [device1, device2]
    return api
'''
def test_device_manager_initialization(device_manager):
    assert device_manager.devices == []

def test_add_device(device_manager):
    device_manager.add_device("iPhone", 85)
    assert len(device_manager.devices) == 1
    assert device_manager.devices[0] == {"name": "iPhone", "battery_level": 85}

def test_add_multiple_devices(device_manager):
    device_manager.add_device("iPhone", 85)
    device_manager.add_device("iPad", 70)
    assert len(device_manager.devices) == 2
    assert device_manager.devices[0] == {"name": "iPhone", "battery_level": 85}
    assert device_manager.devices[1] == {"name": "iPad", "battery_level": 70}

def test_get_all_devices(device_manager):
    device_manager.add_device("iPhone", 85)
    device_manager.add_device("iPad", 70)
    devices = device_manager.get_all_devices()
    assert len(devices) == 2
    assert devices[0] == {"name": "iPhone", "battery_level": 85}
    assert devices[1] == {"name": "iPad", "battery_level": 70}

class TestMixediCloudandOtherDevices(unittest.TestCase):
    def setUp(self):
        self.device_manager = DeviceManager()
        self.mock_api = MagicMock()
        self.mock_api = MagicMock()
        self.mock_api.requires_2fa = False
        self.mock_device1 = MagicMock()
        self.mock_device1.status.return_value = {
            'deviceDisplayName': 'iPhone 12',
            'batteryLevel': 0.85
        }
        self.mock_device2 = MagicMock()
        self.mock_device2.status.return_value = {
            'deviceDisplayName': 'iPad Pro',
            'batteryLevel': 0.65
        }
        self.mock_api.devices = [self.mock_device1, self.mock_device2]


    def test_add_local_and_icloud_devices(self):

        battery_data = get_battery_from_icloud(self.mock_api, self.device_manager)
        devices = self.device_manager.get_all_devices()
        self.device_manager.add_device('Car', 82)
        self.assertEqual(len(devices), 3)
        self.assertEqual(devices[0]['name'], 'iPhone 12')
        self.assertEqual(devices[0]['battery_level'], 85)
        self.assertEqual(devices[1]['name'], 'iPad Pro')
        self.assertEqual(devices[1]['battery_level'], 65)
        self.assertEqual(devices[2]['name'], 'Car')
        self.assertEqual(devices[2]['battery_level'], 82)
