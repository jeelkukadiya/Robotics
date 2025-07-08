import cv2
import numpy as np
import pyrealsense2 as rs

def create_trackbar(window_name, color):
    # Create trackbars for adjusting the lower and upper HSV range
    cv2.createTrackbar(f'Low H {color}', window_name, 0, 179, lambda x: None)
    cv2.createTrackbar(f'Low S {color}', window_name, 0, 255, lambda x: None)
    cv2.createTrackbar(f'Low V {color}', window_name, 0, 255, lambda x: None)
    cv2.createTrackbar(f'High H {color}', window_name, 0, 179, lambda x: None)
    cv2.createTrackbar(f'High S {color}', window_name, 0, 255, lambda x: None)
    cv2.createTrackbar(f'High V {color}', window_name, 0, 255, lambda x: None)

def get_trackbar_values(window_name, color):
    lower = np.array([
        cv2.getTrackbarPos(f'Low H {color}', window_name),
        cv2.getTrackbarPos(f'Low S {color}', window_name),
        cv2.getTrackbarPos(f'Low V {color}', window_name)
    ])
    upper = np.array([
        cv2.getTrackbarPos(f'High H {color}', window_name),
        cv2.getTrackbarPos(f'High S {color}', window_name),
        cv2.getTrackbarPos(f'High V {color}', window_name)
    ])
    return (lower, upper)


# Initialize RealSense pipeline
pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
pipeline.start(config)

# Create windows for the masks
cv2.namedWindow('Red Mask')
cv2.namedWindow('Purple Mask')
cv2.namedWindow('Blue Mask')

# Create trackbars for each color
create_trackbar('Red Mask', 'red')
create_trackbar('Purple Mask', 'purple')
create_trackbar('Blue Mask', 'blue')

try:
    while True:
        frames = pipeline.wait_for_frames()
        color_frame = frames.get_color_frame()
        if not color_frame:
            continue

        color_image = np.asanyarray(color_frame.get_data())
        hsv_frame = cv2.cvtColor(color_image, cv2.COLOR_BGR2HSV)

        # Get trackbar values for each color
        red_range = get_trackbar_values('Red Mask', 'red')
        purple_range = get_trackbar_values('Purple Mask', 'purple')
        blue_range = get_trackbar_values('Blue Mask', 'blue')

        # Create masks based on trackbar values
        red_mask = cv2.inRange(hsv_frame, *red_range)
        purple_mask = cv2.inRange(hsv_frame, *purple_range)
        blue_mask = cv2.inRange(hsv_frame, *blue_range)

        # Show the masks
        cv2.imshow('Red Mask', red_mask)
        cv2.imshow('Purple Mask', purple_mask)
        cv2.imshow('Blue Mask', blue_mask)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
finally:
    pipeline.stop()
    cv2.destroyAllWindows()