import numpy as np
import cv2
import imutils
import time
import serial
import sys
import os
import serial.tools.list_ports
from MPU_RBC import get_z_angle

import Jetson.GPIO as GPIO

LED_PIN = 22
GPIO.setmode(GPIO.BOARD)
GPIO.setup(LED_PIN, GPIO.OUT)
GPIO.output(LED_PIN, GPIO.LOW)  # Turn LED off

# Define the lower and upper boundaries of the "blue" and "purple" balls in the HSV color space
# blueLower = (87, 125, 40)
# blueUpper = (127, 255, 255)
purpleLower = (128, 42, 64)
purpleUpper = (170, 198, 198)
# redUpper = (175, 255, 189)
# redLower = (162, 56, 90)

#Upper HSV:  (179, 190, 255)Lower HSV:  (168, 43, 5)
redUpper = (179, 190, 255)
redLower = (168, 43, 5)

#BLUE: Upper HSV:  (111, 252, 242)Lower HSV:  (103, 152, 89)
blueUpper = (111, 252, 242)
blueLower = (103, 152, 89)

# Define the port as a global variable
global_port = 'COM12'
detect_color = 'blue'
send_interval = 120  # 100 ms interval

cap = None

def restart_script(): 
    global cap
    print("releasing resources...")
    GPIO.output(LED_PIN, GPIO.LOW)  # Turn LED off
    GPIO.cleanup()    
    if cap is not None:
        cap.release()
    cv2.destroyAllWindows()
    print("restarting the script...")
    os.execv(sys.executable, ['python3'] + sys.argv)

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
            print("Serial port {} opened successfully.".format(port))
        return ser
    except Exception as e:
        print("Failed to connect to {}: {}".format(port, str(e)))
        # time.sleep(2)
        restart_script()

# Function to send coordinates
def send_coordinates(x,z, ser):
    """ Send coordinates over serial """
    if ser is not None:
        try:
            message = "{},{}\n".format(x, z)
            GPIO.output(LED_PIN, GPIO.HIGH)  # Turn LED on            
            ser.write(message.encode())
            print("Sent coordinates: {},ANGLE: {}".format(x, z))
        except Exception as e:
            print("Failed to send data: {}".format(str(e)))
            ser.close()  # Close the serial port
            # time.sleep(2)
            restart_script()
    else:
        print("Serial connection not established.")
        restart_script()

# Helper function to get current time in milliseconds
def millis():
    return int(round(time.time() * 1000))

# ap = argparse.ArgumentParser()
# ap.add_argument("-v", "--video",
#     help="path to the (optional) video file")
# ap.add_argument("-b", "--buffer", type=int, default=64,
#     help="max buffer size") 
# ap.add_argument("-p", "--port", default=global_port,
#     help="serial port")
# args = vars(ap.parse_args())

# ser_port = setup_serial(args["port"], 9600)
ser_port = find_and_setup_serial()



# Use OpenCV to capture from the USB camera
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH,640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT,480)

frame_count = 0
start_time = time.time()
xx = 0
yy = 0

last_send_time = millis()

try:
    while True:
        ret, frame = cap.read()
        if not ret:
            continue

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

        cv2.line(frame, (280, 0), (280, frame.shape[0]), (0, 255, 0), 2)  # Green vertical line at x=260
        cv2.line(frame, (360, 0), (360, frame.shape[0]), (0, 255, 0), 2)  # Green vertical line at x=380

        if detect_color == 'blue':
            mask = cv2.erode(mask_blue, None, iterations=2)
            mask = cv2.dilate(mask, None, iterations=2)
            cv2.imshow("mask", mask)
            cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            cnts = imutils.grab_contours(cnts)
        elif detect_color == 'red':
            mask = cv2.erode(mask_red, None, iterations=2)
            mask = cv2.dilate(mask, None, iterations=4)
            cv2.imshow("mask", mask)
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
                    if detect_color == 'blue':
                        cv2.circle(frame, (int(x), int(y)), int(radius), (255, 0, 0), 2)
                        cv2.circle(frame, center, 5, (0, 255, 255), -1)
                    elif detect_color == 'red':
                        cv2.circle(frame, (int(x), int(y)), int(radius), (0, 0, 255), 2)
                        cv2.circle(frame, center, 5, (255, 0, 0), -1)

        if nearest_ball_center:
            xx = nearest_ball_center[0]
            yy = nearest_ball_center[1]
        elif detect_color == 'red':
            xx = 0
            yy = 0
        elif detect_color == 'blue':
            xx = 640
            yy = 0

        roll, pitch, yaw = get_z_angle()

        if millis() - last_send_time >= send_interval:
            send_coordinates(xx, yaw, ser_port)
            last_send_time = millis()

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

except KeyboardInterrupt:
    print("Interrupted by user")

finally:
    GPIO.output(LED_PIN, GPIO.LOW)  # Turn LED off
    GPIO.cleanup()
    cap.release()
    cv2.destroyAllWindows()
    if ser_port is not None:
        ser_port.close()