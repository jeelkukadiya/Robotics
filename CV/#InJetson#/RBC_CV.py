import numpy as np
import cv2
import imutils
import time
import pyrealsense2 as rs  # Import the RealSense library
import serial
import sys
import os
import serial.tools.list_ports
# from MPU_RBC import get_z_angle

# import Jetson.GPIO as GPIO

# Define the port as a global variable
global_port = 'COM12'
detect_color = 'blue'
send_interval = 120  # 100 ms interval

# LED_PIN = 22
# GPIO.setmode(GPIO.BOARD)
# GPIO.setup(LED_PIN, GPIO.OUT)
# GPIO.output(LED_PIN, GPIO.LOW)  # Turn LED off

# Define the lower and upper boundaries of the "blue" and "purple" balls in the HSV color space

# PURPLE:
# Upper HSV:  (128, 144, 214)
# Lower HSV:  (115, 38, 65)
# BLUE:
# Upper HSV:  (112, 190, 168)
# Lower HSV:  (101, 40, 3)
# RED:
# Upper HSV:  (4, 255, 255)
# Lower HSV:  (0, 94, 130)

#BLUE
blueUpper = (112, 190, 168)
blueLower = (101, 40, 3)

#RED
#Upper HSV: [179, 255, 255] Lower HSV: [5, 2, 62]
# redUpper = (179, 224, 255)
# redLower = (162, 161, 0)

#Upper HSV:  (179, 187, 255) Lower HSV:  (165, 108, 120)
redUpper = (179, 187, 255)
redLower = (165, 108, 120)


#PURPLE
purpleUpper = (128, 144, 214)
purpleLower = (115, 38, 65)


def restart_script(): 
    print("releasing resources...")
    # GPIO.output(LED_PIN, GPIO.LOW)  # Turn LED off
    # GPIO.cleanup()
    pipeline.stop()
    cv2.destroyAllWindows()
    print("restarting the script...")
    os.execv(sys.executable, ['python'] + sys.argv)

def find_and_setup_serial(baudrate=9600,timeout=1):
    """ Find the port of the Arduino """
    ports = list(serial.tools.list_ports.comports())
    for port in ports:
        ser = setup_serial(port.device,baudrate,timeout)
        if ser is not None:
            return ser
    print("Failed to find and setup serial connection.")
    return None

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
        # time.sleep(1)
        restart_script()

# Function to send coordinates
def send_coordinates(x,z, ser):
    """ Send coordinates over serial """
    if ser is not None:
        try:
            message = f"{x},{z}\n"
            # GPIO.output(LED_PIN, GPIO.HIGH)  # Turn LED on
            ser.write(message.encode())
            print(f"Sent coordinates: {x},ANGLE: {z}")
        except Exception as e:
            print(f"Failed to send data: {str(e)}")
            ser.close()
            # time.sleep(1)
            restart_script()
    else:
        print("Serial connection not established.")
        restart_script()

# Helper function to get current time in milliseconds
def millis():
    return int(round(time.time() * 1000))


# ser_port = find_and_setup_serial()


# Configure depth and color streams from the RealSense camera
pipeline = rs.pipeline()
config = rs.config()
# config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

# Start streaming from RealSense
pipeline.start(config)

frame_count = 0
start_time = time.time()
xx = 0
yy = 0

last_send_time = millis()

# angle_z = 0
# previous_time = time.time()

try:
    while True:

        # Wait for a coherent pair of frames: depth and color
        frames = pipeline.wait_for_frames()
        # depth_frame = frames.get_depth_frame()
        color_frame = frames.get_color_frame()

        if not color_frame:# or not depth_frame:
            continue

        # Convert images to numpy arrays
        frame = np.asanyarray(color_frame.get_data())
        # depth_image = np.asanyarray(depth_frame.get_data())

        # Process frame
        blurred = cv2.GaussianBlur(frame, (11, 11), 0)
        hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

        # Create masks for blue and purple
        mask_blue = cv2.inRange(hsv, blueLower, blueUpper)
        mask_purple = cv2.inRange(hsv, purpleLower, purpleUpper)
        mask_red = cv2.inRange(hsv, redLower, redUpper)

        nearest_ball_depth = float('inf')
        nearest_ball_y = float('inf')
        nearest_ball_center = None

###########################################################################################################################<           
        cv2.line(frame, (280, 0), (280, frame.shape[0]), (0, 255, 0), 2)  # Green vertical line at x=260
        cv2.line(frame, (360, 0), (360, frame.shape[0]), (0, 255, 0), 2)  # Green vertical line at x=380
###########################################################################################################################>            

        if detect_color == 'blue':
            mask = cv2.erode(mask_blue, None, iterations=4)
            mask = cv2.dilate(mask, None, iterations=3)
###########################################################################################################################<           
            cv2.imshow("mask", mask)
###########################################################################################################################>           
            cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            cnts = imutils.grab_contours(cnts)
        elif detect_color == 'red':
            mask = cv2.erode(mask_red, None, iterations=2)
            mask = cv2.dilate(mask, None, iterations=2)
###########################################################################################################################<           
            cv2.imshow("mask", mask)
###########################################################################################################################>           
            cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            cnts = imutils.grab_contours(cnts)

        for c in cnts:
            ((x, y), radius) = cv2.minEnclosingCircle(c)
            M = cv2.moments(c)
            center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
            if radius > 20:
                distance = ((x - 320)**2 + (y - 240)**2)**0.5
                if distance < nearest_ball_depth and y < nearest_ball_y:
                    nearest_ball_depth = distance
                    nearest_ball_y = y
                    nearest_ball_center = center
###########################################################################################################################<           
                    if detect_color == 'blue':
                        cv2.circle(frame, (int(x), int(y)), int(radius), (255, 0, 0), 2)
                        cv2.circle(frame, center, 5, (0, 255, 255), -1)
                    elif detect_color == 'red':
                        cv2.circle(frame, (int(x), int(y)), int(radius), (0, 0, 255), 2)
                        cv2.circle(frame, center, 5, (255, 0, 0), -1)
###########################################################################################################################>           

        if nearest_ball_center:
            xx = nearest_ball_center[0]
            yy = nearest_ball_center[1]
        elif detect_color == 'red':
            xx = 0
            yy = 0
        elif detect_color == 'blue':
            xx = 640
            yy = 0

        # roll,pitch,yaw = get_z_angle()

        current_time = millis()
        if current_time - last_send_time >= send_interval:
            # send_coordinates(xx, yaw, ser_port)
            last_send_time = current_time

###########################################################################################################################<           
        if nearest_ball_center:
            cv2.circle(frame, nearest_ball_center, 10, (0, 0, 0), -1)  # Highlight with color-specific circle
            cv2.line(frame, (320, 480), nearest_ball_center, (255, 255, 255), 2)          
###########################################################################################################################>           

###########################################################################################################################<           
        cv2.circle(frame, (320, 480), 10, (0, 0, 0), -1)
###########################################################################################################################>           

        frame_count += 1
        elapsed_time = time.time() - start_time
        if elapsed_time > 0:
            fps = frame_count / elapsed_time
###########################################################################################################################<           
            cv2.putText(frame, f"FPS: {fps:.2f}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
###########################################################################################################################>           

        cv2.imshow("Frame", frame)
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break
finally:
    # GPIO.output(LED_PIN, GPIO.LOW)  # Turn LED off
    # GPIO.cleanup()
    pipeline.stop()
    cv2.destroyAllWindows()
    # if ser_port is not None:
    #     ser_port.close()