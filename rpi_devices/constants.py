"""Ullr device constants."""
# MPL3115A2 constants
MPL3115A2_DEFAULT_ADDRESS = 0x60  # I2C address of the device

# MPL3115A2 Register Map
MPL3115A2_REG_STATUS = 0x00  # Sensor Status Register
MPL3115A2_REG_PRESSURE_MSB = 0x01  # Pressure Data Out MSB
MPL3115A2_REG_PRESSURE_CSB = 0x02  # Pressure Data Out CSB
MPL3115A2_REG_PRESSURE_LSB = 0x03  # Pressure Data Out LSB
MPL3115A2_REG_TEMP_MSB = 0x04  # Temperature Data Out MSB
MPL3115A2_REG_TEMP_LSB = 0x05  # Temperature Data Out LSB
MPL3115A2_REG_DR_STATUS = 0x06  # Data Ready status information
MPL3115A2_OUT_P_DELTA_MSB = 0x07  # Pressure Data Out Delta MSB
MPL3115A2_OUT_P_DELTA_CSB = 0x08  # Pressure Data Out Delta CSB
MPL3115A2_OUT_P_DELTA_LSB = 0x09  # Pressure Data Out Delta LSB
MPL3115A2_OUT_T_DELTA_MSB = 0x0A  # Temperature Data Out Delta MSB
MPL3115A2_OUT_T_DELTA_LSB = 0x0B  # Temperature Data Out Delta LSB
MPL3115A2_REG_WHO_AM_I = 0x0C  # Device Identification Register
MPL3115A2_PT_DATA_CFG = 0x13  # PT Data Configuration Register
MPL3115A2_CTRL_REG1 = 0x26  # Control Register 1
MPL3115A2_CTRL_REG2 = 0x27  # Control Register 2
MPL3115A2_CTRL_REG3 = 0x28  # Control Register 3
MPL3115A2_CTRL_REG4 = 0x29  # Control Register 4
MPL3115A2_CTRL_REG5 = 0x2A  # Control Register 5

# MPL3115A2 PT Data Configuration Registers
MPL3115A2_PT_DATA_CFG_TDEFE = 0x01  # Raise event flag on new temperature data
MPL3115A2_PT_DATA_CFG_PDEFE = 0x02  # Raise event flag on new pressure/altitude data
MPL3115A2_PT_DATA_CFG_DREM = 0x04  # Raise event flag on new temp or pressure/altitude data

# MPL3115A2 Control Register 1 Configuration
MPL3115A2_CTRL_REG1_SBYB = 0x01  # Set mode to ACTIVE
MPL3115A2_CTRL_REG1_OST = 0x02  # Set OST (one shot mode) to ACTIVE
MPL3115A2_CTRL_REG1_RST = 0x04  # Activate software reset
MPL3115A2_CTRL_REG1_OS1 = 0x00  # Set oversample ratio to 1
MPL3115A2_CTRL_REG1_OS2 = 0x08  # Set oversample ratio to 2
MPL3115A2_CTRL_REG1_OS4 = 0x10  # Set oversample ratio to 4
MPL3115A2_CTRL_REG1_OS8 = 0x18  # Set oversample ratio to 8
MPL3115A2_CTRL_REG1_OS16 = 0x20  # Set oversample ratio to 16
MPL3115A2_CTRL_REG1_OS32 = 0x28  # Set oversample ratio to 32
MPL3115A2_CTRL_REG1_OS64 = 0x30  # Set oversample ratio to 64
MPL3115A2_CTRL_REG1_OS128 = 0x38  # Set oversample ratio to 128
MPL3115A2_CTRL_REG1_RAW = 0x40  # Activate RAW output mode
MPL3115A2_CTRL_REG1_ALT = 0x80  # Part is in altimeter mod
MPL3115A2_CTRL_REG1_BAR = 0x00  # Part is in barometer mode
