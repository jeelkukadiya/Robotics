import cv2
import numpy as np
import serial
import time

def gstreamer_pipeline(
    sensor_id=0,
    capture_width=1920,
    capture_height=1080,
    display_width=640,
    display_height=480,
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

# Define the HSV range for white color
lower_white = np.array([3, 2, 116])
upper_white = np.array([178, 63, 174])

# Setup the serial connection
def setup_serial(port='/dev/ACM0', baudrate=9600, timeout=1):
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

# Initialize serial connection
ser = setup_serial(port='/dev/ACM0', baudrate=9600)

# Capture video from the CSI camera
cap = cv2.VideoCapture(gstreamer_pipeline(flip_method=0), cv2.CAP_GSTREAMER)

if not cap.isOpened():
    print("Error: Could not open video stream.")
    exit()
frame_count = 0
start_time = time.time()
while True:
    # Read a frame from the video stream
    ret, frame = cap.read()
    frame_count += 1
    
    if not ret:
        print("Error: Could not read frame.")
        break

    # Convert the frame to HSV color space
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Create a mask for the white color
    mask = cv2.inRange(hsv, lower_white, upper_white)

    # Find contours in the mask
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Filter out small contours
    min_contour_area = 500  # Adjust this value as needed
    large_contours = [cnt for cnt in contours if cv2.contourArea(cnt) > min_contour_area]

    # Find the largest contour which should be the white line
    if large_contours:
        largest_contour = max(large_contours, key=cv2.contourArea)
        
        # Calculate the moments of the largest contour
        M = cv2.moments(largest_contour)
        
        if M["m00"] != 0:
            # Calculate the center of the white line
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
            
            # Print the coordinates of the center
            print(f"Center of the line: ({cX}, {cY})")
            
            # Send the coordinates over serial
            send_coordinates(cX, cY, ser)
            
            # Draw the center on the frame
            cv2.circle(frame, (cX, cY), 5, (255, 0, 0), -1)
            
            # Optionally, draw the contour
            cv2.drawContours(frame, [largest_contour], -1, (0, 255, 0), 2)
        else:
            print("No white line detected.")
            if ser is not None:
                ser.write(b"no_line\n")
            else:
                print("Serial connection not established. Cannot send 'no_line' command.")
    else:
        print("No contours found.")
        if ser is not None:
            ser.write(b"no_line\n")
        else:
            print("Serial connection not established. Cannot send 'no_line' command.")

    # Calculate and display FPS every second
    if (time.time() - start_time) >= 1.0:
        fps = frame_count / (time.time() - start_time)
        frame_count = 0
        start_time = time.time()    
        
    cv2.putText(frame, f"FPS: {fps:.2f}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # Display the frame with the center of the white line
    cv2.imshow('Video Stream with Center of White Line', frame)

    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture object and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()
ser.close()