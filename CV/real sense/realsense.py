import pyrealsense2 as rs
import numpy as np
import cv2

# Configure depth and color streams
pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

# Start the pipeline
pipeline.start(config)

# Function to show distance and coordinates when a point in the color image is clicked
def show_distance_and_coordinates(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        # Ensure that the coordinates are within the dimensions of the depth image
        if x < depth_image.shape[1] and y < depth_image.shape[0]:
            # Get the depth value at the clicked coordinates
            depth = depth_image[y, x]
            # Convert depth from uint16 to meters
            depth_in_meters = depth * depth_scale
            
            # Deproject from pixel to point in 3D
            intrinsics = profile.as_video_stream_profile().get_intrinsics()
            point = rs.rs2_deproject_pixel_to_point(intrinsics, [x, y], depth_in_meters)
            
            print(f"3D coordinates at point ({x}, {y}): X={point[0]:.3f}m, Y={point[1]:.3f}m, Z={point[2]:.3f}m")
            # print(point)

try:
    while True:
        # Wait for a coherent pair of frames: depth and color
        frames = pipeline.wait_for_frames()

        depth_frame = frames.get_depth_frame()
        color_frame = frames.get_color_frame()
        if not depth_frame or not color_frame:
            continue

        # Convert images to numpy arrays
        depth_image = np.asanyarray(depth_frame.get_data())
        color_image = np.asanyarray(color_frame.get_data())

        # Show the color image
        cv2.imshow('RealSense Color', color_image)
        cv2.imshow('black depth',depth_image)
        #cv2.imshow('depth ',depth_frame)
        # Set mouse callback function for the color image window
        cv2.setMouseCallback('RealSense Color', show_distance_and_coordinates)

        # Get depth scale for converting depth from units to meters
        depth_sensor = pipeline.get_active_profile().get_device().first_depth_sensor()
        depth_scale = depth_sensor.get_depth_scale()
        
        # Get the profile for intrinsic parameters
        profile = pipeline.get_active_profile().get_stream(rs.stream.depth).as_video_stream_profile()

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
finally:
    # Stop streaming
    pipeline.stop()