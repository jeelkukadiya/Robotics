# import the necessary packages
from collections import deque
import numpy as np
import argparse
import cv2
import imutils
import time
# import pyrealsense2 as rs  # Import the RealSense library
import serial

# Define the port as a global variableq
global_port = '/dev/ttyACM0'
#detect_color = 'red'
detect_color = 'blue'
# Setup the serial connection
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

ser_port = setup_serial(args["port"], 9600)

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


#RED: Upper HSV:  (179, 210, 172) Lower HSV:  (165, 77, 69)
# redUpper = (179, 210, 172)
# redLower = (165, 77, 69)

#Upper HSV:  (179, 190, 255)Lower HSV:  (168, 43, 5)
redUpper = (179, 190, 255)
redLower = (168, 43, 5)

#BLUE: Upper HSV:  (111, 252, 242)Lower HSV:  (103, 152, 89)
blueUpper = (111, 252, 242)
blueLower = (103, 152, 89)

# Initialize the list of tracked points
# pts_blue = deque(maxlen=args["buffer"])
# pts_purple = deque(maxlen=args["buffer"])

# Configure depth and color streams from the RealSense camera
# pipeline = rs.pipeline()
# config = rs.config()
# config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
# config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

# # Start streaming from RealSense
# pipeline.start(config)

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

frame_count = 0
start_time = time.time()
xx = 0
yy = 0
depth_in_mm = 0

try:
    while True:
        # Wait for a coherent pair of frames: depth and color
        # frames = pipeline.wait_for_frames()
        # depth_frame = frames.get_depth_frame()
        # color_frame = frames.get_color_frame()
        # if not color_frame or not depth_frame:
        #     continue

        # Convert images to numpy arrays
        # frame = np.asanyarray(color_frame.get_data())
        ret , frame = cap.read()
        # depth_image = np.asanyarray(depth_frame.get_data())

        # Process frame
        #frame = imutils.resize(frame, width=600)
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
        cv2.line(frame, (260, 0), (260, frame.shape[0]), (0, 255, 0), 2)  # Green vertical line at x=300
        cv2.line(frame, (380, 0), (380, frame.shape[0]), (0, 255, 0), 2)  # Green vertical line at x=340
        # cv2.line(frame, (0, 320), (frame.shape[1], 320), (0, 255, 0), 2)  # Green vertical line at x=340
        # cv2.line(frame, (280, 0), (280, frame.shape[0]), (0, 255, 0), 2)  # Green vertical line at x=300
        # cv2.line(frame, (360, 0), (360, frame.shape[0]), (0, 255, 0), 2)  # Green vertical line at x=340
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

        for c in cnts:
            ((x, y), radius) = cv2.minEnclosingCircle(c)
            M = cv2.moments(c)
            center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
            if radius > 20 :#and y > 100:

                # depth = depth_image[center[1], center[0]]

                if y > nearest_ball_depth:
                    nearest_ball_depth = y
                    nearest_ball_center = center
                    if detect_color == 'blue':
                        cv2.circle(frame, (int(x), int(y)), int(radius), (255, 0, 0), 2)
                        cv2.circle(frame, center, 5, (0, 255, 255), -1)
                    elif detect_color == 'red':
                        cv2.circle(frame, (int(x), int(y)), int(radius), (0, 0, 255), 2)
                        cv2.circle(frame, center, 5, (255, 0, 0), -1)
        # Process each mask
        # for color, mask in [('red', mask_red),('blue', mask_blue), ('purple', mask_purple)]:
        #     mask = cv2.erode(mask, None, iterations=2)
        #     mask = cv2.dilate(mask, None, iterations=2)
        #     if color == 'blue':
        #         cv2.imshow("mask",mask)
        #     cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        #     cnts = imutils.grab_contours(cnts)

        #     for c in cnts:
        #         #area = cv2.contourArea(c)
        #         ((x, y), radius) = cv2.minEnclosingCircle(c)
        #         # if y<350:
        #         #     continue
        #         M = cv2.moments(c)
        #         center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
        #         if radius > 6 and y>50:
        #             depth = depth_image[center[1], center[0]]
        #             # if depth < nearest_ball_depth:
        #             #     nearest_ball_depth = depthmi
        #             #     nearest_ball_center = center
        #             #     nearest_ball_color = color
        #             if color == 'blue' and y > nearest_ball_depth:# and depth < nearest_ball_depth:
        #                 #nearest_ball_depth = depth
        #                 nearest_ball_depth = y
        #                 nearest_ball_center = center
        #                 cv2.circle(frame, (int(x), int(y)), int(radius), (255, 0, 0), 2)
        #                 cv2.circle(frame, center, 5, (0, 255, 255), -1)
        #             elif color == 'red':
        #                 cv2.circle(frame, (int(x), int(y)), int(radius), (0, 0, 255), 2)
        #                 cv2.circle(frame, center, 5, (255, 0, 0), -1)
        #             elif color == 'purple':
        #                 cv2.circle(frame, (int(x), int(y)), int(radius), (128, 0, 128), 2)
        #                 cv2.circle(frame, center, 5, (255, 255, 0), -1)

                    
        # Highlight the nearest ball
        if nearest_ball_center:# and nearest_ball_depth > 0:
            #depth_in_mm = nearest_ball_depth+160
            xx = nearest_ball_center[0]
            yy = nearest_ball_center[1]
        else:
            xx = 0
            yy = 0
########################################################################
        # if ser_port.in_waiting > 0:
        #         # ser_port.flushInput()
        #         line = ser_port.readline().decode('utf-8').rstrip()
        #         print(f"received from Arduino: {line}")
        #         if line == 'done':
        #             print("BOOM BOOM")
                    
        #             time.sleep(2)
        #             color_verify = color_detect()
        #             # color_verification = color_detect()
        #             # temp_color = f"{color_verification}\n"
        #             # ser_port.write(temp_color.encode())
        #             # print(f"Color verification: {color_verification}")
        #             #color_verify = "yes"
        #             print("verify is:",color_verify)

        #             #time.sleep(0.5)
                    
        #             # send_coordinates(nearest_ball_center[0], nearest_ball_center[1],depth_in_mm, ser_port,color_verify)

        #             x_time = time.time()
        #             while time.time() - x_time < 2:
        #                 send_coordinates(xx, yy,ser_port,color_verify)
        #                 time.sleep(0.5)
                        
        #         else:
        #             #color_detect
        #             print("No data received from Arduino")
        # else:
            # print("No data received from Arduino")
########################################################################            
        send_coordinates(xx, yy, ser_port)

            #color_detect
            
            # if nearest_ball_color == 'blue':
            #     highlight_color = (255, 0, 0)
            # elif nearest_ball_color == 'purple':
            #     highlight_color = (128, 0, 128)
        cv2.circle(frame, nearest_ball_center, 10, (0,0,0), -1)  # Highlight with color-specific circle

        frame_count += 1
        elapsed_time = time.time() - start_time
        if elapsed_time > 0:
            fps = frame_count / elapsed_time
            print(fps)
            cv2.putText(frame, f"FPS: {fps:.2f}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)
        
        
        # Show the frame to our screen
        cv2.imshow("Frame", frame)
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break
finally:
    # Stop streaming
    #pipeline.stop()
    cap.release()
    cv2.destroyAllWindows()
    # ser_port.close()

# # import the necessary packages
# from collections import deque
# import numpy as np
# import argparse
# import cv2
# import imutils
# import time
# import pyrealsense2 as rs  # Import the RealSense library
# import serial

# # Setup the serial connection
# def setup_serial(port='COM5', baudrate=9600, timeout=1):
#     """ Initialize serial connection """
#     try:
#         ser = serial.Serial(port, baudrate, timeout=timeout)
#         if ser.is_open:
#             print(f"Serial port {port} opened successfully.")
#         return ser
#     except Exception as e:
#         print(f"Failed to connect to {port}: {str(e)}")
#         return None

# # Function to send coordinates
# def send_coordinates(x, y, ser):
#     """ Send coordinates over serial """
#     if ser is not None:
#         try:
#             message = f"{x},{y}\n"
#             ser.write(message.encode())
#             print(f"Sent coordinates: {x}, {y}")
#         except Exception as e:
#             print(f"Failed to send data: {str(e)}")
#     else:
#         print("Serial connection not established.")

# ser = setup_serial()  # Adjust the port and baudrate as needed
# time.sleep(2)
# # construct the argument parse and parse the arguments
# ap = argparse.ArgumentParser()
# ap.add_argument("-v", "--video",
#                 help="path to the (optional) video file")
# ap.add_argument("-b", "--buffer", type=int, default=64,
#                 help="max buffer size")
# args = vars(ap.parse_args())

# # define the lower and upper boundaries of the "blue" and "purple" balls in the HSV color space
# blueLower = (87, 125, 40)
# blueUpper = (127, 255, 255)
# purpleLower = (128, 42, 64)
# purpleUpper = (170, 198, 198)

# # Initialize the list of tracked points
# pts_blue = deque(maxlen=args["buffer"])
# pts_purple = deque(maxlen=args["buffer"])

# # Configure depth and color streams from the RealSense camera
# pipeline = rs.pipeline()
# config = rs.config()
# config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
# config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

# # Start streaming from RealSense
# pipeline.start(config)

# try:
#     while True:
#         # Wait for a coherent pair of frames: depth and color
#         frames = pipeline.wait_for_frames()
#         depth_frame = frames.get_depth_frame()
#         color_frame = frames.get_color_frame()
#         if not color_frame or not depth_frame:
#             continue

#         # Convert images to numpy arrays
#         frame = np.asanyarray(color_frame.get_data())
#         depth_image = np.asanyarray(depth_frame.get_data())

#         # Process frame
#         frame = imutils.resize(frame, width=600)
#         blurred = cv2.GaussianBlur(frame, (11, 11), 0)
#         hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

#         # Create masks for blue and purple
#         mask_blue = cv2.inRange(hsv, blueLower, blueUpper)
#         mask_purple = cv2.inRange(hsv, purpleLower, purpleUpper)

#         nearest_ball_depth = float('inf')
#         nearest_ball_center = None
#         nearest_blue_center = None
#         nearest_blue_depth = float('inf')
#         nearest_purple_center = None
#         nearest_purple_depth = float('inf')

#         # Process each mask
#         for color, mask in [('blue', mask_blue), ('purple', mask_purple)]:
#             # mask = cv2.erode(mask, None, iterations=2)
#             mask = cv2.erode(mask, None, iterations=2)
#             mask = cv2.dilate(mask, None, iterations=2)
#             cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
#             cnts = imutils.grab_contours(cnts)

#             for c in cnts:
#                 ((x, y), radius) = cv2.minEnclosingCircle(c)
#                 M = cv2.moments(c)
#                 center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
#                 if radius > 30:
#                     depth = depth_image[center[1], center[0]]
#                     # if depth < nearest_blue_depth:
#                     #     nearest_blue_depth = depth
#                     #     nearest_blue_center = center
#                     if color == 'blue' and depth < nearest_blue_depth:
#                         nearest_ball_depth = depth
#                         nearest_ball_center = center
#                         cv2.circle(frame, (int(x), int(y)), int(radius), (255, 0, 0), 2)
#                         cv2.circle(frame, center, 5, (0, 255, 255), -1)
#                         # nearest_blue_depth = depth
#                         # nearest_blue_center = center
#                     elif color == 'purple' and depth < nearest_purple_depth:
#                         cv2.circle(frame, (int(x), int(y)), int(radius), (128, 0, 128), 2)
#                         cv2.circle(frame, center, 5, (255, 255, 0), -1)
#                         # nearest_purple_depth = depth
#                         # nearest_purple_center = center

#         # Highlight the nearest ball
#         # if nearest_blue_center:
#         #     cv2.circle(frame, nearest_blue_center, 10, (0, 0, 255), -1)  # Green circle
#         #     send_coordinates(nearest_blue_center[0], nearest_blue_center[1], ser)
#         # if nearest_purple_center:
#         #     cv2.circle(frame, nearest_purple_center, 10, (0, 0, 255), -1)  # Green circle
#         #     send_coordinates(nearest_purple_center[0], nearest_purple_center[1], ser)   
#         if nearest_ball_center:
#             cv2.circle(frame, nearest_ball_center, 10, (0, 0, 255), -1)  # Green circle
#             send_coordinates(nearest_ball_center[0], nearest_ball_center[1], ser)
#         # send_coordinates(100, 150, ser)

#         # Show the frame to our screen
#         cv2.imshow("Frame", frame)
#         key = cv2.waitKey(1) & 0xFF
#         if key == ord("q"):
#             break
# finally:
#     # Stop streaming
#     pipeline.stop()
#     cv2.destroyAllWindows()
