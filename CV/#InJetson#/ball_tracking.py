# import the necessary packages
from collections import deque
import numpy as np
import argparse
import cv2
import imutils
import time
import pyrealsense2 as rs  # Import the RealSense library

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video",
                help="path to the (optional) video file")
ap.add_argument("-b", "--buffer", type=int,default=64,
                help="max buffer size")
args = vars(ap.parse_args())

# define the lower and upper boundaries of the "blue" and "purple" balls in the HSV color space
blueLower = (87, 125, 40)
blueUpper = (127, 255, 255)
purpleLower = (128, 42, 64)
purpleUpper = (170, 198, 198)

# Initialize the list of tracked points
pts_blue = deque(maxlen=args["buffer"])
pts_purple = deque(maxlen=args["buffer"])

# Configure depth and color streams from the RealSense camera
pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

# Start streaming from RealSense
pipeline.start(config)

try:
    while True:
        # Wait for a coherent pair of frames: depth and color
        frames = pipeline.wait_for_frames()
        depth_frame = frames.get_depth_frame()
        color_frame = frames.get_color_frame()
        if not color_frame or not depth_frame:
            continue

        # Convert images to numpy arrays
        frame = np.asanyarray(color_frame.get_data())
        depth_image = np.asanyarray(depth_frame.get_data())

        # Process frame
        frame = imutils.resize(frame, width=600)
        blurred = cv2.GaussianBlur(frame, (11, 11), 0)
        hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

        # Create masks for blue and purple
        mask_blue = cv2.inRange(hsv, blueLower, blueUpper)
        mask_purple = cv2.inRange(hsv, purpleLower, purpleUpper)

        nearest_ball_depth = float('inf')
        nearest_ball_center = None

        # Process each mask
        for color, mask in [('blue', mask_blue), ('purple', mask_purple)]:
            mask = cv2.erode(mask, None, iterations=2)
            mask = cv2.dilate(mask, None, iterations=2)
            cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            cnts = imutils.grab_contours(cnts)

            for c in cnts:
                ((x, y), radius) = cv2.minEnclosingCircle(c)
                M = cv2.moments(c)
                center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
                if radius > 10:
                    depth = depth_image[center[1], center[0]]
                    if depth < nearest_ball_depth:
                        nearest_ball_depth = depth
                        nearest_ball_center = center
                    if color == 'blue':
                        cv2.circle(frame, (int(x), int(y)), int(radius), (255, 0, 0), 2)
                        cv2.circle(frame, center, 5, (0, 255, 255), -1)
                    elif color == 'purple':
                        cv2.circle(frame, (int(x), int(y)), int(radius), (128, 0, 128), 2)
                        cv2.circle(frame, center, 5, (255, 255, 0), -1)

        # Highlight the nearest ball
        if nearest_ball_center:
            cv2.circle(frame, nearest_ball_center, 10, (0, 255, 0), -1)  # Green circle

        # Show the frame to our screen
        cv2.imshow("Frame", frame)
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break
finally:
    # Stop streaming
    pipeline.stop()
    cv2.destroyAllWindows()