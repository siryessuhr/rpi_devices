"""Device: MPL3115A2

See Datasheet: http://cdn.sparkfun.com/datasheets/Sensors/Pressure/MPL3115A2.pdf
"""
import logging
import time

import smbus2

from rpi_devices import constants

_log = logging.Logger(__name__)


class Mpl3115a2:
    def __init__(self, bus: smbus2.SMBus) -> None:
        self.bus = bus

        self.altitude_m = None
        self.altitude_ft = None
        self.pressure_kpa = None
        self.pressure_atm = None
        self.temp_c = None
        self.temp_f = None

    def _get_raw_sensor_status(self) -> list:
        """Get the raw data back from the sensor status register."""
        return self.bus.read_i2c_block_data(
            i2c_addr=constants.MPL3115A2_DEFAULT_ADDRESS,
            register=constants.MPL3115A2_REG_STATUS,
            length=6,
        )

    def _normalize_raw_data(self, sensor_data: list) -> float:
        """Method to normalize the raw data from the sensor registers.

        Raw value calculation:
            MSB * 2**16 + CSB * 2**8 + LSB * 2**0
            where the final four bits of the LSB are removed
        """
        return ((sensor_data[1] * 65536) + (sensor_data[2] * 256) + (sensor_data[3] & 0xF0)) / 16

    def get_altitude(self):
        """Get altitude data from the sensor."""
        self.set_altimeter_config()
        time.sleep(0.1)

        data = self._get_raw_sensor_status()
        _log.debug(f"Raw data from sensor: {data}")

        # Shift additional 4 bits to account for fractions of a meter in bits 7-4
        self.altitude_m = self._normalize_raw_data(data) / 16
        self.altitude_ft = self.altitude_m * 3.28084
        _log.info(f"Altitude: {self.altitude_m} m, {self.altitude_ft} ft")

    def get_device_id(self) -> int:
        """Get the device ID from the sensor."""
        return self.bus.read_i2c_block_data(
            i2c_addr=constants.MPL3115A2_DEFAULT_ADDRESS,
            register=constants.MPL3115A2_REG_WHO_AM_I,
            length=1,
        )[0]

    def get_pressure(self):
        """Get pressure data from the sensor."""
        self.set_barometer_config()

        data = self._get_raw_sensor_status()

        # Shift additional 2 bits to account for fractions of a Pascal in bits 5-4
        self.pressure_kpa = self._normalize_raw_data(data) / 4 / 1000
        self.pressure_atm = self.pressure_kpa / 101.325
        _log.info(f"Pressure: {self.pressure_kpa} kPa, {self.pressure_atm} atm")

    def get_temperature(self):
        """Get temperature data from the sensor."""
        data = self._get_raw_sensor_status()

        # Shift additional 4 bits to account for fractions of a degree in bits 7-4
        self.temp_c = ((data[4] * 256) + (data[5] & 0xF0)) / 16 / 16
        self.temp_f = self.temp_c * 1.8 + 32
        _log.info(f"Temperature: {self.temp_c} C, {self.temp_f} F")

    def measure(self):
        """Measure all available values from MPL3115A2 sensor."""
        self.set_pt_config()
        self.get_temperature()
        self.get_altitude()
        self.get_pressure()

    def set_altimeter_config(self):
        """Set the altimeter configuration on the sensor.

        This method sets a register value that will:
            1. Sets mode to active
            2. Initiates a measurement immediately
            3. Sets the sensor to Altimeter mode
        """
        register_val = (
            constants.MPL3115A2_CTRL_REG1_SBYB
            | constants.MPL3115A2_CTRL_REG1_OS128
            | constants.MPL3115A2_CTRL_REG1_ALT
        )
        self.bus.write_byte_data(
            i2c_addr=constants.MPL3115A2_DEFAULT_ADDRESS,
            register=constants.MPL3115A2_CTRL_REG1,
            value=register_val,
        )

    def set_barometer_config(self):
        """Set the barometer configuration on the sensor.

        This method sets a register value that will:
            1. Sets mode to active
            2. Initiates a measurement immediately
            3. Sets the sensor to Barometer mode
        """
        register_val = constants.MPL3115A2_CTRL_REG1_SBYB | constants.MPL3115A2_CTRL_REG1_OS128
        self.bus.write_byte_data(
            i2c_addr=constants.MPL3115A2_DEFAULT_ADDRESS,
            register=constants.MPL3115A2_CTRL_REG1,
            value=register_val,
        )

    def set_pt_config(self):
        """Set the pressure/temperature configuration on the sensor.

        This method sets a register value that will:
            1. Generate data ready event mode
            2. Enable data event flag on new pressure/altitude data
            3. Enable data event flag on new temperature data
        """
        register_val = (
            constants.MPL3115A2_PT_DATA_CFG_TDEFE
            | constants.MPL3115A2_PT_DATA_CFG_PDEFE
            | constants.MPL3115A2_PT_DATA_CFG_DREM
        )
        self.bus.write_byte_data(
            i2c_addr=constants.MPL3115A2_DEFAULT_ADDRESS,
            register=constants.MPL3115A2_PT_DATA_CFG,
            value=register_val,
        )
