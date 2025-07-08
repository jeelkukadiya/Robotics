import smbus
import time

# MPU6050 Registers and their addresses
MPU6050_ADDR = 0x68
PWR_MGMT_1 = 0x6B
GYRO_ZOUT_H = 0x47
RESET_BIT = 0x80

def MPU6050_init():
    bus.write_byte_data(MPU6050_ADDR, PWR_MGMT_1, RESET_BIT)
    time.sleep(0.1)
    bus.write_byte_data(MPU6050_ADDR, PWR_MGMT_1, 0)

def read_raw_data(addr):
    high = bus.read_byte_data(MPU6050_ADDR, addr)
    low = bus.read_byte_data(MPU6050_ADDR, addr + 1)
    value = (high << 8) | low
    if value > 32768:
        value = value - 65536
    return value

def calibrate_gyro():
    num_samples = 1000
    gyro_z_offset = 0
    for _ in range(num_samples):
        gyro_z_offset += read_raw_data(GYRO_ZOUT_H)
        time.sleep(0.001)
    return gyro_z_offset / num_samples

bus = smbus.SMBus(1)  # or smbus.SMBus(0) for older Jetson Nano versions
MPU6050_init()

# Calibrate gyro
gyro_z_offset = calibrate_gyro()

# Initial angle (considered as origin)
angle_z = 0

# Time tracking
previous_time = time.time()

def get_z_angle():
    global angle_z, previous_time
    current_time = time.time()
    dt = current_time - previous_time
    previous_time = current_time

    gyro_z = (read_raw_data(GYRO_ZOUT_H) - gyro_z_offset) / 131.0  # convert to deg/s
    x = 0
    y = 0    
        # Integrate the angular velocity to get the angle
    angle_z += gyro_z * dt

    return x,y,angle_z

# while True:
#     angle = get_z_angle()
#     print(f"Angle from initial position: {angle:.2f} degrees")
#     time.sleep(0.1)