import pyrealsense2 as rs

# Configure streams
pipeline = rs.pipeline()
config = rs.config()

# Enable IMU data
config.enable_stream(rs.stream.accel, rs.format.motion_xyz32f, 200)
config.enable_stream(rs.stream.gyro, rs.format.motion_xyz32f, 200)

# Start streaming
pipeline.start(config)

try:
    while True:
        # Wait for a coherent pair of frames: one set for gyro and one for accelerometer
        frames = pipeline.wait_for_frames()
        accel_frame = frames.first_or_default(rs.stream.accel)
        gyro_frame = frames.first_or_default(rs.stream.gyro)
        
        if accel_frame and gyro_frame:
            # Get motion data
            accel_data = accel_frame.as_motion_frame().get_motion_data()
            gyro_data = gyro_frame.as_motion_frame().get_motion_data()
            
            print("Accel data: x={:.3f}, y={:.3f}, z={:.3f}".format(accel_data.x, accel_data.y, accel_data.z))
            print("Gyro data: x={:.3f}, y={:.3f}, z={:.3f}".format(gyro_data.x, gyro_data.y, gyro_data.z))

except Exception as e:
    print(e)
finally:
    pipeline.stop()