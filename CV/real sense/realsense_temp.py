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

        # Example pixel coordinates (you can choose any pixel you're interested in)
        u, v = 320, 240  # Center pixel of the depth image

        # Get the depth value at the desired pixel
        depth = depth_image[v, u]

        # Get intrinsics for the depth sensor
        depth_intrinsics = depth_frame.profile.as_video_stream_profile().intrinsics

        # Deproject from pixel to 3D coordinates
        x, y, z = rs.rs2_deproject_pixel_to_point(depth_intrinsics, [u, v], depth)

        # Display the 3D coordinates on the color image
        cv2.circle(color_image, (u, v), 5, (0, 0, 255), -1)
        cv2.putText(color_image, f"3D: x={x:.2f}, y={y:.2f}, z={z:.2f}", (u, v - 10),
                    cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 255), 1)

        # Show images
        cv2.imshow('RealSense', color_image)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
finally:
    # Stop streaming
    pipeline.stop()
    cv2.destroyAllWindows()