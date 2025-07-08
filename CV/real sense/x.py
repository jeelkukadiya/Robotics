import numpy as np
import cv2 as cv

# Callback function for mouse event
def mouse_callback(event, x, y, flags, param):
    global selected_point
    if event == cv.EVENT_LBUTTONDOWN:
        selected_point = (x, y)

def draw_center_line(frame):
    height, width, _ = frame.shape

    # Draw horizontal line
    cv.line(frame, (0, height // 2), (width, height // 2), (0, 255, 0), 2)

    # Draw vertical line
    cv.line(frame, (width // 2, 0), (width // 2, height), (0, 255, 0), 2)

# Initialize selected_point
selected_point = None

# Create a VideoCapture object
cap = cv.VideoCapture(1)

w = 640
h = 480


# Camera intrinsic parameters


#fx = 10 # Focal length in x-axis
#fy = 5 # Focal length in y-axis

cx = w // 2 # Principal point x-coordinate
cy = h // 2 # Principal point y-coordinate

# v_fov = 60

# h_fov = 60


#Z = 
z = 100 #mm


#cx = 


# Set frame width and height
cap.set(cv.CAP_PROP_FRAME_WIDTH, w)
cap.set(cv.CAP_PROP_FRAME_HEIGHT, h)
    
# Set mouse callback function
cv.namedWindow("frame")
cv.setMouseCallback("frame", mouse_callback)

# Conversion factor from pixels to millimeters
pixels_to_mm = 1  # Change this value based on your camera calibration

while cap.isOpened():
    
    _, frame = cap.read()

        
    # Find center coordinates of the frame
    center_x = frame.shape[1] // 2  #320 #640
    center_y = frame.shape[0] // 2  #240 #480


    # Display the frame
    if selected_point is not None:
        cv.putText(frame, f"Coordinates: {selected_point}", (50, 50), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        # Calculate distance in millimeters
        distance_mm = pixels_to_mm * 100  # 100 mm
        cv.putText(frame, f"Distance: {distance_mm} mm", (50, 100), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        # new_x = z * ( (selected_point[0] - center_x) / h_fov)

        # new_y = z * ( (selected_point[1] - center_y) / v_fov)

        # print(new_x,new_y)

        new_x = 20 #mm

        new_y = 17 #mm

        f_x = z * ((selected_point[0] - center_x) / new_x)

        f_y = z * ((selected_point[1] - center_y) / new_y)

        print(f_x,f_y)



    #print(center_x, center_y)
    cv.circle(frame, (center_x, center_y), 5, (0, 0, 255), -1)  # Draw a red circle at the center
    
    draw_center_line(frame)
    cv.imshow("frame", frame)
    
    # Check for key press
    key = cv.waitKey(1)
    if key == ord('q'):
        break

# Release the VideoCapture object and close all windows
cap.release()
cv.destroyAllWindows()
