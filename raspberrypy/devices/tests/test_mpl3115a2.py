import platform

import pytest
import smbus2

from devices import constants
from devices.mpl3115a2 import Mpl3115a2

raspberrypi = pytest.mark.skipif(
    platform.uname().node != "raspberrypi", reason="Only runs on Raspberry Pi."
)


@pytest.fixture
def device():
    bus = smbus2.SMBus(1)
    device = Mpl3115a2(bus=bus)
    try:
        if device.get_device_id() != 196:
            pytest.skip("MPL3115A2 sensor not connected.")
        else:
            return device
    except OSError:
        pytest.skip("MPL3115A2 sensor not connected.")


@pytest.fixture
def mock_device():
    bus = smbus2.SMBus()
    return Mpl3115a2(bus=bus)


def test_get_raw_sensor_status_mock(mock_device, mocker):
    mocker.patch.object(mock_device.bus, "read_i2c_block_data", return_value=[238, 81, 226, 208, 21, 64])
    assert mock_device._get_raw_sensor_status() == [238, 81, 226, 208, 21, 64]


@raspberrypi
def test_get_altitude(device):
    device.get_altitude()
    assert device.altitude_m is not None
    assert device.altitude_ft is not None


def test_get_altitude_mock(mock_device, mocker):
    mocker.patch.object(mock_device, "set_altimeter_config")
    mocker.patch.object(mock_device, "_get_raw_sensor_status", return_value=[238, 6, 73, 96, 0, 0])
    mock_device.get_altitude()
    assert mock_device.altitude_ft == 5280.101875
    assert mock_device.altitude_m == 1609.375


@raspberrypi
def test_get_device_id(device):
    assert device.get_device_id() == 196


def test_get_device_id_mock(mock_device, mocker):
    mocker.patch.object(mock_device.bus, "read_i2c_block_data", return_value=[196])
    assert mock_device.get_device_id() == 196


@raspberrypi
def test_get_pressure(device):
    device.get_pressure()
    assert device.pressure_kpa is not None
    assert device.pressure_atm is not None


def test_get_pressure_mock(mock_device, mocker):
    mocker.patch.object(mock_device, "set_barometer_config")
    mocker.patch.object(mock_device, "_get_raw_sensor_status", return_value=[238, 81, 226, 208, 21, 0])
    mock_device.get_pressure()
    assert mock_device.pressure_kpa == 83.85125
    assert mock_device.pressure_atm == 0.8275474956822106


@raspberrypi
def test_get_temperature(device):
    device.get_temperature()
    assert device.temp_c is not None
    assert device.temp_f is not None


def test_get_temperature_mock(mock_device, mocker):
    mocker.patch.object(mock_device, "_get_raw_sensor_status", return_value=[0, 0, 0, 0, 21, 64])
    mock_device.get_temperature()
    assert mock_device.temp_c == 21.25
    assert mock_device.temp_f == 70.25


@raspberrypi
def test_measure(device):
    device.measure()
    assert device.temp_c is not None
    assert device.temp_f is not None
    assert device.altitude_m is not None
    assert device.altitude_ft is not None
    assert device.pressure_kpa is not None
    assert device.pressure_atm is not None


def test_measure_mock(mock_device, mocker):
    mocker.patch.object(mock_device, "set_pt_config")
    mocker.patch.object(mock_device, "set_barometer_config")
    mocker.patch.object(mock_device, "set_altimeter_config")
    mocker.patch.object(mock_device, "_get_raw_sensor_status", return_value=[238, 81, 226, 208, 21, 64])
    mock_device.measure()
    assert mock_device.temp_c == 21.25
    assert mock_device.temp_f == 70.25
    assert mock_device.pressure_kpa == 83.85125
    assert mock_device.pressure_atm == 0.8275474956822106

    mocker.patch.object(mock_device, "_get_raw_sensor_status", return_value=[238, 6, 73, 96, 0, 0])
    mock_device.measure()
    assert mock_device.altitude_ft == 5280.101875
    assert mock_device.altitude_m == 1609.375


@raspberrypi
def test_set_altimeter_config(device):
    device.set_altimeter_config()
    assert (
        device.bus.read_byte_data(
            i2c_addr=constants.MPL3115A2_DEFAULT_ADDRESS,
            register=constants.MPL3115A2_CTRL_REG1,
        )
        == 0xB9  # 10111001
    )


def test_set_altimeter_config_mock(mock_device, mocker):
    mocker.patch.object(mock_device.bus, "write_byte_data")
    mock_device.set_altimeter_config()
    mock_device.bus.write_byte_data.assert_called_once_with(
        i2c_addr=constants.MPL3115A2_DEFAULT_ADDRESS,
        register=constants.MPL3115A2_CTRL_REG1,
        value=0xB9,
    )


@raspberrypi
def test_set_barometer_config(device):
    device.set_barometer_config()
    assert (
        device.bus.read_byte_data(
            i2c_addr=constants.MPL3115A2_DEFAULT_ADDRESS,
            register=constants.MPL3115A2_CTRL_REG1,
        )
        == 0x39  # 00111001
    )


def test_set_barometer_config_mock(mock_device, mocker):
    mocker.patch.object(mock_device.bus, "write_byte_data")
    mock_device.set_barometer_config()
    mock_device.bus.write_byte_data.assert_called_once_with(
        i2c_addr=constants.MPL3115A2_DEFAULT_ADDRESS,
        register=constants.MPL3115A2_CTRL_REG1,
        value=0x39,
    )


@raspberrypi
def test_set_pt_config(device):
    device.set_pt_config()
    assert (
        device.bus.read_byte_data(
            i2c_addr=constants.MPL3115A2_DEFAULT_ADDRESS,
            register=constants.MPL3115A2_PT_DATA_CFG,
        )
        == 0x07  # 00000111
    )


def test_set_pt_config_mock(mock_device, mocker):
    mocker.patch.object(mock_device.bus, "write_byte_data")
    mock_device.set_pt_config()
    mock_device.bus.write_byte_data.assert_called_once_with(
        i2c_addr=constants.MPL3115A2_DEFAULT_ADDRESS,
        register=constants.MPL3115A2_PT_DATA_CFG,
        value=0x07,
    )
