import pytest
from io import StringIO
import sys
from batteryGauge import DeviceManager, get_battery_level, registered_devices, show_all_devices

def test_battery_level_range():
    for _ in range(100):  # Test multiple times for randomness
        battery_level = get_battery_level()
        assert 20 <= battery_level <= 100

def test_registered_devices():
    assert len(registered_devices) > 0, "No registered devices found"
    for device in registered_devices:
        assert 'name' in device
        assert 'battery_level' in device
        assert isinstance(device['name'], str)
        assert isinstance(device['battery_level'], int)
        assert 20 <= device['battery_level'] <= 100

@pytest.mark.parametrize('capsys', [()], indirect=True)
def test_show_all_devices_output(capsys):
    # Capture the output of the function using a StringIO
    #captured_output = StringIO()
    #sys.stdout = captured_output
    device_manager = DeviceManager()
    show_all_devices(device_manager)
    captured = capsys.readouterr()
    #sys.stdout = sys.__stdout__
    #output = captured_output.getvalue()

    # Ensure heading is correct
    assert "Registered Devices:" in captured.out

    # Ensure that device names and battery levels are displayed
    for device in registered_devices:
        assert device['name'] in captured.out
        assert f"{device['battery_level']}%" in captured.out
