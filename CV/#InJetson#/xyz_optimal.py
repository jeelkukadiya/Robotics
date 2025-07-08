# import the necessary packages
from collections import deque
import numpy as np
import argparse
import cv2
import imutils
import time
import pyrealsense2 as rs  # Import the RealSense library
import serial
from scipy.spatial import distance as dist
from collections import OrderedDict

# Define the port as a global variable
global_port = '/dev/ttyACM0'
#detect_color = 'red'
detect_color = 'blue'

def color_detect():
    # color_verify = "no"
    with open('ball_detected.txt', 'r') as file:
        color_verify = file.read()
    return color_verify

# Setup the serial connection
def setup_serial(port=global_port, baudrate=115200, timeout=1):
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
def send_coordinates(x, y,ser,verify="NULL"):
    """ Send coordinates over serial """
    if ser is not None:
        try:
            message = f"{x},{y},{verify}\n"
            ser.write(message.encode())
            print(f"Sent coordinates: {x}, {y},verification is : {verify}")
        except Exception as e:
            print(f"Failed to send data: {str(e)}")
    else:
        print("Serial connection not established.")

# ser = setup_serial()  # Adjust the port and baudrate as needed
# time.sleep(2)

# # construct the argument parse and parse the arguments
# ap = argparse.ArgumentParser()
# ap.add_argument("-v", "--video",
#                 help="path to the (optional) video file")
# ap.add_argument("-b", "--buffer", type=int, default=64,
#                 help="max buffer size")
# args = vars(ap.parse_args())

ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video",
    help="path to the (optional) video file")
ap.add_argument("-b", "--buffer", type=int, default=64,
    help="max buffer size") 
ap.add_argument("-p", "--port", default=global_port,
    help="serial port")
args = vars(ap.parse_args())

ser_port = setup_serial(args["port"], 115200)

# define the lower and upper boundaries of the "blue" and "purple" balls in the HSV color space
blueLower = (87, 125, 40)
blueUpper = (127, 255, 255)
purpleLower = (128, 42, 64)
purpleUpper = (170, 198, 198)
#RED: Upper HSV: [179, 255, 208] Lower HSV: [1, 22, 87]
#redLower = (175, 158, 204)
#redUpper = (179, 207, 236)

#redLower = (1, 22, 87)
#redUpper = (179, 255, 208)

#redLower = (177, 37, 72)
#redUpper = (179, 184, 197)

#redUpper = (173, 229, 159)
#redLower = (167, 73, 81)

redUpper = (175, 255, 189)
redLower = (162, 56, 90)

#Upper HSV: [172, 246, 213] Lower HSV: [165, 32, 89]
# redUpper = (172, 246, 213)
# redLower = (165, 32, 89)


#############################################################################
#BLUE: Upper HSV:  (126, 245, 212) Lower HSV:  (98, 172, 79)
# blueUpper = (126, 245, 212)
# blueLower = (98, 172, 79)

#PURPLE: Upper HSV:  (166, 221, 137) Lower HSV:  (107, 56, 43)
purpleUpper = (166, 221, 137)
purpleLower = (107, 56, 43)

#RED: Upper HSV: [179, 203, 134] Lower HSV: [1, 53, 61]
# redUpper = (179, 203, 134)
# redLower = (1, 53, 61)



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

frame_count = 0
start_time = time.time()
xx = 0
yy = 0
depth_in_mm = 0

class CentroidTracker():
    def __init__(self, maxDisappeared=50):
        self.nextObjectID = 0
        self.objects = OrderedDict()
        self.disappeared = OrderedDict()
        self.maxDisappeared = maxDisappeared

    def register(self, centroid):
        self.objects[self.nextObjectID] = centroid
        self.disappeared[self.nextObjectID] = 0
        self.nextObjectID += 1

    def deregister(self, objectID):
        del self.objects[objectID]
        del self.disappeared[objectID]

    def update(self, rects):
        if len(rects) == 0:
            for objectID in list(self.disappeared.keys()):
                self.disappeared[objectID] += 1
                if self.disappeared[objectID] > self.maxDisappeared:
                    self.deregister(objectID)
            return self.objects

        inputCentroids = np.zeros((len(rects), 2), dtype="int")
        for (i, (startX, startY, endX, endY)) in enumerate(rects):
            cX = int((startX + endX) / 2.0)
            cY = int((startY + endY) / 2.0)
            inputCentroids[i] = (cX, cY)

        if len(self.objects) == 0:
            for i in range(0, len(inputCentroids)):
                self.register(inputCentroids[i])
        else:
            objectIDs = list(self.objects.keys())
            objectCentroids = list(self.objects.values())

            D = dist.cdist(np.array(objectCentroids), inputCentroids)

            rows = D.min(axis=1).argsort()
            cols = D.argmin(axis=1)[rows]

            usedRows = set()
            usedCols = set()

            for (row, col) in zip(rows, cols):
                if row in usedRows or col in usedCols:
                    continue

                objectID = objectIDs[row]
                self.objects[objectID] = inputCentroids[col]
                self.disappeared[objectID] = 0

                usedRows.add(row)
                usedCols.add(col)

            unusedRows = set(range(0, D.shape[0])).difference(usedRows)
            unusedCols = set(range(0, D.shape[1])).difference(usedCols)

            if D.shape[0] >= D.shape[1]:
                for row in unusedRows:
                    objectID = objectIDs[row]
                    self.disappeared[objectID] += 1

                    if self.disappeared[objectID] > self.maxDisappeared:
                        self.deregister(objectID)
            else:
                for col in unusedCols:
                    self.register(inputCentroids[col])

        return self.objects

# Initialize tracker
ct = CentroidTracker(maxDisappeared=50)

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
        mask_red = cv2.inRange(hsv, redLower, redUpper)

        nearest_ball_depth = 0#float('inf')
        nearest_ball_center = None
        nearest_ball_color = None

        # Inside your main loop where you process each frame
        # Inside your main loop where you process each frame
        cv2.line(frame, (270, 0), (270, frame.shape[0]), (0, 255, 0), 2)  # Green vertical line at x=300
        cv2.line(frame, (370, 0), (370, frame.shape[0]), (0, 255, 0), 2)  # Green vertical line at x=340
        # cv2.line(frame, (0, 320), (frame.shape[1], 320), (0, 255, 0), 2)  # Green vertical line at x=340

        if detect_color == 'blue':
            mask = cv2.erode(mask_blue, None, iterations=2)
            mask = cv2.dilate(mask, None, iterations=2)
            cv2.imshow("mask",mask)
            cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            cnts = imutils.grab_contours(cnts)
        elif detect_color == 'red':
            mask = cv2.erode(mask_red, None, iterations=2)
            mask = cv2.dilate(mask, None, iterations=4)
            cv2.imshow("mask",mask)
            cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            cnts = imutils.grab_contours(cnts)

        rects = []
        for c in cnts:
            ((x, y), radius) = cv2.minEnclosingCircle(c)
            M = cv2.moments(c)
            center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
            if radius > 20:# and y > 100:
                depth = depth_image[center[1], center[0]]
                if y > nearest_ball_depth:
                    nearest_ball_depth = y
                    nearest_ball_center = center
                    if detect_color == 'blue':
                        cv2.circle(frame, (int(x), int(y)), int(radius), (255, 0, 0), 2)
                        cv2.circle(frame, center, 5, (0, 255, 255), -1)
                    elif detect_color == 'red':
                        cv2.circle(frame, (int(x), int(y)), int(radius), (0, 0, 255), 2)
                        cv2.circle(frame, center, 5, (255, 0, 0), -1)
                rects.append((center[0] - radius, center[1] - radius, center[0] + radius, center[1] + radius))

        objects = ct.update(rects)
        for (objectID, centroid) in objects.items():
            text = "ID {}".format(objectID)
            cv2.putText(frame, text, (centroid[0] - 10, centroid[1] - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            cv2.circle(frame, (centroid[0], centroid[1]), 4, (0, 255, 0), -1)

        send_coordinates(xx, yy, ser_port)
        cv2.circle(frame, nearest_ball_center, 10, (0,0,0), -1)  # Highlight with color-specific circle

        frame_count += 1
        elapsed_time = time.time() - start_time
        if elapsed_time > 0:
            fps = frame_count / elapsed_time
            cv2.putText(frame, f"FPS: {fps:.2f}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        
        
        # Show the frame to our screen
        cv2.imshow("Frame", frame)
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break
finally:
    # Stop streaming
    pipeline.stop()
    cv2.destroyAllWindows()
