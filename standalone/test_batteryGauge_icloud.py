import unittest
from unittest.mock import patch, MagicMock
from batteryGauge import DeviceManager, login_to_icloud, get_battery_from_icloud

class TestiCloudBattery(unittest.TestCase):

    @patch('builtins.input', side_effect=['test_user', 'test_password'])
    @patch('batteryGauge.PyiCloudService')
    def test_login_to_icloud(self, MockPyiCloudService, mock_input):
        # Mock the PyiCloudService
        mock_api = MagicMock()
        MockPyiCloudService.return_value = mock_api

        # Call the login function
        api = login_to_icloud()

        # Check if the API was called with the correct credentials
        MockPyiCloudService.assert_called_with('test_user', 'test_password')
        self.assertEqual(api, mock_api)

    @patch('builtins.input', side_effect=['123456'])
    def test_get_battery_from_icloud_2fa(self, mock_input):
        # Create a mock API
        mock_api = MagicMock()
        mock_api.requires_2fa = True
        mock_api.validate_2fa_code.return_value = True

        # Mock device data
        mock_device = MagicMock()
        mock_device.status.return_value = {
            'deviceDisplayName': 'iPhone 12',
            'batteryLevel': 0.85
        }
        mock_api.devices = [mock_device]

        device_manager = DeviceManager()

        # Call the function to get battery levels
        battery_data = get_battery_from_icloud(mock_api, device_manager)

        # Ensure 2FA code validation was called
        mock_api.validate_2fa_code.assert_called_with('123456')

        # Check that battery data was retrieved
        self.assertEqual(len(battery_data), 1)
        self.assertEqual(battery_data[0]['name'], 'iPhone 12')
        self.assertEqual(battery_data[0]['battery_level'], 85)

    def test_get_battery_from_icloud_no_2fa(self):
        # Create a mock API without 2FA
        mock_api = MagicMock()
        mock_api.requires_2fa = False

        # Mock device data
        mock_device = MagicMock()
        mock_device.status.return_value = {
            'deviceDisplayName': 'iPhone 12',
            'batteryLevel': 0.85
        }
        mock_api.devices = [mock_device]

        device_manager = DeviceManager()

        # Call the function to get battery levels
        battery_data = get_battery_from_icloud(mock_api, device_manager)

        # Ensure 2FA was not required
        self.assertFalse(mock_api.validate_2fa_code.called)

        # Check the battery data
        self.assertEqual(len(battery_data), 1)
        self.assertEqual(battery_data[0]['name'], 'iPhone 12')
        self.assertEqual(battery_data[0]['battery_level'], 85)

    def test_get_battery_level_none(self):
        mock_api = MagicMock()
        mock_api.requires_2fa = False

        # Mock device data
        mock_device = MagicMock()
        mock_device.status.return_value = {
            'deviceDisplayName': 'Apple TV',
            'batteryLevel': None

        }

        mock_api.devices = [mock_device]

        device_manager = DeviceManager()

        # Call the function to get battery levels
        battery_data = get_battery_from_icloud(mock_api, device_manager)

        # Ensure 2FA was not required
        self.assertFalse(mock_api.validate_2fa_code.called)

        # Check the battery data
        self.assertEqual(len(battery_data), 1)
        self.assertEqual(battery_data[0]['name'], 'Apple TV')
        self.assertEqual(battery_data[0]['battery_level'], 'Unknown')

    def test_get_battery_level_missing(self):
        mock_api = MagicMock()
        mock_api.requires_2fa = False
        mock_device = MagicMock()
        mock_device.status.return_value = {
            'deviceDisplayName': 'HomePod'
            # 'batteryLevel' key is missing
        }
        mock_api.devices = [mock_device]
        device_manager = DeviceManager()
        battery_data = get_battery_from_icloud(mock_api, device_manager)
        self.assertEqual(len(battery_data), 1)
        self.assertEqual(battery_data[0]['name'], 'HomePod')
        self.assertEqual(battery_data[0]['battery_level'], 'Unknown')

    def test_multiple_devices(self):
        mock_api = MagicMock()
        mock_api.requires_2fa = False
        mock_device1 = MagicMock()
        mock_device1.status.return_value = {
            'deviceDisplayName': 'iPhone 12',
            'batteryLevel': 0.85
        }
        mock_device2 = MagicMock()
        mock_device2.status.return_value = {
            'deviceDisplayName': 'iPad Pro',
            'batteryLevel': 0.65
        }
        mock_api.devices = [mock_device1, mock_device2]
        device_manager = DeviceManager()
        battery_data = get_battery_from_icloud(mock_api, device_manager)
        self.assertEqual(len(battery_data), 2)
        self.assertEqual(battery_data[0]['name'], 'iPhone 12')
        self.assertEqual(battery_data[0]['battery_level'], 85)
        self.assertEqual(battery_data[1]['name'], 'iPad Pro')
        self.assertEqual(battery_data[1]['battery_level'], 65)


if __name__ == '__main__':
    unittest.main()
