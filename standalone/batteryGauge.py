import random
from pyicloud import PyiCloudService

class DeviceManager:
    def __init__(self):
        self.devices = []

    def add_device(self, name, battery_level):
        self.devices.append({"name": name, "battery_level": battery_level})


    def add_devices_from_icloud(self, icloud_devices):
        for device in icloud_devices:
            self.add_device(device['name'], device['battery_level'])

    def get_all_devices(self):
        return self.devices

# Function to log in to iCloud
def login_to_icloud():
    apple_id = input("Enter your Apple ID: ")
    password = input("Enter your password: ")

    api = PyiCloudService(apple_id, password)
    return api

# Function to get battery level from iCloud devices
def get_battery_from_icloud(api, device_manager):
    if api.requires_2fa:
        print("Two-factor authentication required.")
        code = input("Enter the code you received on your device: ")
        result = api.validate_2fa_code(code)
        if not result:
            print("Failed to verify 2FA code.")
            return

    devices = api.devices
    battery_data = []

    for device in devices:
        device_status = device.status()
        battery_level = device_status.get('batteryLevel')

        if battery_level is not None and isinstance(battery_level, (int, float)):
            battery_percentage = battery_level * 100
        else:
            battery_percentage = "Unknown"

        battery_info = {
            'name': device_status['deviceDisplayName'],
            'battery_level': battery_percentage
        }
        device_manager.add_device(battery_info['name'], battery_info['battery_level'])
        # remove #### battery_data.append(battery_info)
        print(f"Device: {battery_info['name']}, Battery Level: {battery_info['battery_level']}%")

    return device_manager.get_all_devices()

# Mock function to simulate reading battery levels
def get_battery_level():
    return random.randint(20, 100)

# Devices "registered" in the family (for now, we fake the registration)
registered_devices = [
    {"name": "PHEV", "battery_level": get_battery_level()},
    {"name": "Camera 1", "battery_level": get_battery_level()}
]

def show_all_devices(device_manager):
    print("\nRegistered Devices:")
    for device in registered_devices:
        print(f"- {device['name']}: {device['battery_level']}% battery")

def main():
    device_manager = DeviceManager()
    print("Battery Status CLI")
    print("==================")
    show_all_devices(device_manager)
    api = login_to_icloud()
    get_battery_from_icloud(api, device_manager)

if __name__ == "__main__":
    main()
