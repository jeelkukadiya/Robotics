# import the necessary packages
from collections import deque
import numpy as np
import argparse
import cv2
import imutils
import time
import pyrealsense2 as rs  # Import the RealSense library
import serial

# Setup the serial connection
def setup_serial(port='COM8', baudrate=9600, timeout=1):
    """ Initialize serial connection """
    try:
        ser = serial.Serial(port, baudrate, timeout=timeout)
        if ser.is_open:
            print(f"Serial port {port} opened successfully.")
        return ser
    except Exception as e:
        print(f"Failed to connect to {port}: {str(e)}")
        return None

# Function to send coordinates
def send_coordinates(x, y, ser):
    """ Send coordinates over serial """
    if ser is not None:
        try:
            message = f"{x},{y}\n"
            ser.write(message.encode())
            print(f"Sent coordinates: {x}, {y}")
        except Exception as e:
            print(f"Failed to send data: {str(e)}")
    else:
        print("Serial connection not established.")

ser = setup_serial()  # Adjust the port and baudrate as needed
time.sleep(2)
# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video",
                help="path to the (optional) video file")
ap.add_argument("-b", "--buffer", type=int, default=64,
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
        nearest_blue_center = None
        nearest_blue_depth = float('inf')
        nearest_purple_center = None
        nearest_purple_depth = float('inf')

        # Process each mask
        for color, mask in [('blue', mask_blue), ('purple', mask_purple)]:
            # mask = cv2.erode(mask, None, iterations=2)
            mask = cv2.erode(mask_blue, None, iterations=2)
            mask = cv2.dilate(mask, None, iterations=2)
            cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            cnts = imutils.grab_contours(cnts)

            for c in cnts:
                ((x, y), radius) = cv2.minEnclosingCircle(c)
                M = cv2.moments(c)
                center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
                if radius > 30:
                    depth = depth_image[center[1], center[0]]
                    # if depth < nearest_blue_depth:
                    #     nearest_blue_depth = depth
                    #     nearest_blue_center = center
                    if color == 'blue' and depth < nearest_blue_depth:
                        nearest_ball_depth = depth
                        nearest_ball_center = center
                        cv2.circle(frame, (int(x), int(y)), int(radius), (255, 0, 0), 2)
                        cv2.circle(frame, center, 5, (0, 255, 255), -1)
                        # nearest_blue_depth = depth
                        # nearest_blue_center = center
                    elif color == 'purple' and depth < nearest_purple_depth:
                        cv2.circle(frame, (int(x), int(y)), int(radius), (128, 0, 128), 2)
                        cv2.circle(frame, center, 5, (255, 255, 0), -1)
                        # nearest_purple_depth = depth
                        # nearest_purple_center = center

        # Highlight the nearest ball
        # if nearest_blue_center:
        #     cv2.circle(frame, nearest_blue_center, 10, (0, 0, 255), -1)  # Green circle
        #     send_coordinates(nearest_blue_center[0], nearest_blue_center[1], ser)
        # if nearest_purple_center:
        #     cv2.circle(frame, nearest_purple_center, 10, (0, 0, 255), -1)  # Green circle
        #     send_coordinates(nearest_purple_center[0], nearest_purple_center[1], ser)   
        if nearest_ball_center:
            cv2.circle(frame, nearest_ball_center, 10, (0, 0, 255), -1)  # Green circle
            send_coordinates(nearest_ball_center[0], nearest_ball_center[1], ser)
        # send_coordinates(100, 150, ser)

        # Show the frame to our screen
        cv2.imshow("Frame", frame)
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break
finally:
    # Stop streaming
    pipeline.stop()
    cv2.destroyAllWindows()