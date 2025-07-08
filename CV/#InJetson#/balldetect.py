# MIT License
# Copyright (c) 2019-2022 JetsonHacks

# Using a CSI camera (such as the Raspberry Pi Version 2) connected to a
# NVIDIA Jetson Nano Developer Kit using OpenCV
# Drivers for the camera and OpenCV are included in the base image

import cv2
from collections import deque
import numpy as np
import argparse
import imutils
import time
import serial   

# Define the port as a global variableq
global_port = '/dev/ttyACM0'
detect_color = 'red'

def setup_serial(port=global_port, baudrate=9600, timeout=1):
    """ Initialize serial connection """
    try:
        ser = serial.Serial(port, baudrate, timeout=timeout)
        if ser.is_open:
            print(f"Serial port {port} opened successfully.")
        return ser
    except Exception as e:
        print(f"Failed to connect to {port}: {str(e)}")
        return None
    
# GStreamer pipeline for CSI camera
def gstreamer_pipeline(
    sensor_id=0,
    capture_width=1920,
    capture_height=1080,
    display_width=960,
    display_height=540,
    framerate=30,
    flip_method=0,
):
    return (
        "nvarguscamerasrc sensor-id=%d ! "
        "video/x-raw(memory:NVMM), width=(int)%d, height=(int)%d, framerate=(fraction)%d/1 ! "
        "nvvidconv flip-method=%d ! "
        "video/x-raw, width=(int)%d, height=(int)%d, format=(string)BGRx ! "
        "videoconvert ! "
        "video/x-raw, format=(string)BGR ! appsink"
        % (
            sensor_id,
            capture_width,
            capture_height,
            framerate,
            flip_method,
            display_width,
            display_height,
        )
    )

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video",
	help="path to the (optional) video file")
ap.add_argument("-b", "--buffer", type=int, default=64,
	help="max buffer size")
ap.add_argument("-p", "--port", default=global_port,
    help="serial port")
args = vars(ap.parse_args())

ser_port = setup_serial(args["port"], 9600)

# define the lower and upper boundaries of the "green"
# ball in the HSV color space, then initialize the
# list of tracked points
blueLower = (91, 126, 0)
blueUpper = (114, 254, 175)

#Upper HSV: [179, 247, 172] Lower HSV: [1, 5, 42]
# redUpper = (179, 247, 172)
# redLower = (1, 5, 42)

# redUpper = (175, 255, 189)
# redLower = (162, 56, 90)

#Upper HSV: [179, 241, 217] Lower HSV: [1, 4, 48]
redUpper = (179, 241, 217)
redLower = (1, 4, 48)

pts = deque(maxlen=args["buffer"])

# if a video path was not supplied, grab the reference to the CSI camera
if not args.get("video", False):
    print(gstreamer_pipeline(flip_method=0))
    vs = cv2.VideoCapture(gstreamer_pipeline(flip_method=0), cv2.CAP_GSTREAMER)
    if not vs.isOpened():
        print("Error: Unable to open camera")
        exit(1)
else:
    # otherwise, grab a reference to the video file
    vs = cv2.VideoCapture(args["video"])

# allow the camera or video file to warm up
time.sleep(2.0)

frame_count = 0
start_time = time.time()

# keep looping
while True:
    # grab the current frame
    ret, frame = vs.read()
    frame_count += 1
    # if we are viewing a video and we did not grab a frame, then we have reached the end of the video
    if frame is None:
        break
    # resize the frame, blur it, and convert it to the HSV color space
    frame = imutils.resize(frame, width=600)
    blurred = cv2.GaussianBlur(frame, (11, 11), 0)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
    # construct a mask for the color "green", then perform a series of dilations and erosions to remove any small blobs left in the mask
    mask_blue = cv2.inRange(hsv, blueLower, blueUpper)
    mask_red = cv2.inRange(hsv, redLower, redUpper)
    if detect_color == 'blue':
        mask = cv2.erode(mask_blue, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)
        cv2.imshow("mask",mask)
        cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)  
    else:
        mask = cv2.erode(mask_red, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)
        cv2.imshow("mask",mask)
        cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
    

    # find contours in the mask and initialize the current (x, y) center of the ball
    # cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # cnts = imutils.grab_contours(cnts)
    center = None
    # only proceed if at least one contour was found
    if len(cnts) > 0:
        # find the largest contour in the mask, then use it to compute the minimum enclosing circle and centroid
        c = max(cnts, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        M = cv2.moments(c)
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

        if center is not None:
            print("Ball Coordinates (x, y):", center)

        # only proceed if the radius meets a minimum size
        if radius > 10:
            # draw the circle and centroid on the frame, then update the list of tracked points
            cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 2)
            cv2.circle(frame, center, 5, (0, 0, 255), -1)
    # update the points queue
    # pts.appendleft(center)

    # # loop over the set of tracked points
    # for i in range(1, len(pts)):
    #     # if either of the tracked points are None, ignore them
    #     if pts[i - 1] is None or pts[i] is None:
    #         continue
    #     # otherwise, compute the thickness of the line and draw the connecting lines
    #     thickness = int(np.sqrt(args["buffer"] / float(i + 1)) * 2.5)
    #     #cv2.line(frame, pts[i - 1], pts[i], (0, 0, 255), thickness)

    elapsed_time = time.time() - start_time
    if elapsed_time > 0:
        fps = frame_count / elapsed_time
        cv2.putText(frame, f"FPS: {fps:.2f}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)    
    
    # show the frame to our screen
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF
    # if the 'q' key is pressed, stop the loop
    if key == ord("q"):
        break

# if we are not using a video file, stop the camera video stream
vs.release()
# close all windows
cv2.destroyAllWindows()