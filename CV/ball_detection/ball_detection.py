






# install opencv "pip install opencv-python"
import cv2
import numpy as np

# Distance from camera to object measured in centimeters
Known_distance = 76.2

# Diameter of the balls in the real world in centimeters
Known_diameter = 20  # Assuming a standard tennis ball diameter

# Colors
GREEN = (0, 255, 0)
RED = (244, 54, 76)
BLUE = (48, 127, 226)
PURPLE = (161, 90, 149)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Defining the fonts
fonts = cv2.FONT_HERSHEY_COMPLEX

# Focal length finder function
def Focal_Length_Finder(measured_distance, real_diameter, diameter_in_rf_image):
    focal_length = (diameter_in_rf_image * measured_distance) / real_diameter
    return focal_length

# Distance estimation function
def Distance_finder(Focal_Length, real_diameter, diameter_in_frame):
    distance = (real_diameter * Focal_Length) / diameter_in_frame
    return distance

# Ball detection function
def detect_ball(image, lower, upper, color):
    # Convert image to HSV color space
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    
    # Threshold the HSV image to get only desired colors
    mask = cv2.inRange(hsv, lower, upper)
    
    # Find contours in the mask
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    if contours:
        # Get the largest contour
        contour = max(contours, key=cv2.contourArea)
        
        # Get the radius and center of the circle that encloses the contour
        ((x, y), radius) = cv2.minEnclosingCircle(contour)
        
        # Draw the circle and centroid on the frame
        cv2.circle(image, (int(x), int(y)), int(radius), color, 2)

        cv2.circle(image, (int(x), int(y)), 2, color, -1)
        
        return radius * 2  # Return diameter
    else:
        return 0

# Reading reference image from directory
ref_image = cv2.imread("red_ball.jpg")

# Find the diameter of the ball (pixels) in the reference image
# You need to define these HSV ranges
# Red ball HSV range
lower_red = np.array([244, 0, 28])
upper_red = np.array([244, 54, 76])

# Purple ball HSV range
lower_purple = np.array([100, 50, 100])
upper_purple = np.array([161, 90, 149])

# Blue ball HSV range
lower_blue = np.array([0, 100, 226])
upper_blue = np.array([48, 127, 226])





# Find the diameter of the balls (pixels) in the reference image
ref_image_red_diameter = detect_ball(ref_image, lower_red, upper_red, RED)
ref_image_blue_diameter = detect_ball(ref_image, lower_blue, upper_blue, BLUE)
ref_image_purple_diameter = detect_ball(ref_image, lower_purple, upper_purple, PURPLE)

# Get the focal length for each ball by calling "Focal_Length_Finder"
Focal_length_red = Focal_Length_Finder(Known_distance, Known_diameter, ref_image_red_diameter)
Focal_length_blue = Focal_Length_Finder(Known_distance, Known_diameter, ref_image_blue_diameter)
Focal_length_purple = Focal_Length_Finder(Known_distance, Known_diameter, ref_image_purple_diameter)

print(Focal_length_red)
#print(Focal_length_blue)
#print(Focal_length_purple)


# Show the reference image
cv2.imshow("ref_image", ref_image)

# Initialize the camera object
cap = cv2.VideoCapture(0)

while True:
    # Reading the frame from the camera
    _, frame = cap.read()

    # Detecting red ball
    red_diameter_in_frame = detect_ball(frame, lower_red, upper_red, RED)

    # Check if the ball is detected
    if red_diameter_in_frame != 0:
        # Finding the distance
        Distance_red = Distance_finder(Focal_length_red, Known_diameter, red_diameter_in_frame)

        # Drawing Text on the screen
        cv2.putText(frame, f"Red Ball: {round(Distance_red, 2)} CM", (30, 35), fonts, 0.6, RED, 2)

    # Detecting blue ball
    blue_diameter_in_frame = detect_ball(frame, lower_blue, upper_blue, BLUE)

    # Check if the ball is detected
    if blue_diameter_in_frame != 0:
        # Finding the distance
        Distance_blue = Distance_finder(Focal_length_blue, Known_diameter, blue_diameter_in_frame)

        # Drawing Text on the screen
        cv2.putText(frame, f"Blue Ball: {round(Distance_blue, 2)} CM", (30, 65), fonts, 0.6, BLUE, 2)

    # Detecting purple ball
    purple_diameter_in_frame = detect_ball(frame, lower_purple, upper_purple, PURPLE)

    # Check if the ball is detected
    if purple_diameter_in_frame != 0:
        # Finding the distance
        Distance_purple = Distance_finder(Focal_length_purple, Known_diameter, purple_diameter_in_frame)

        # Drawing Text on the screen
        cv2.putText(frame, f"Purple Ball: {round(Distance_purple, 2)} CM", (30, 95), fonts, 0.6, PURPLE, 2)
    

    # # Check if the ball is detected
    # if red_diameter_in_frame != 0:
    #     # Finding the distance
    #     Distance = Distance_finder(
    #         Focal_length_found, Known_diameter, red_diameter_in_frame)

    #     # Drawing Text on the screen
    #     cv2.putText(
    #         frame, f"Distance to Red Ball: {round(Distance, 2)} CM", (30, 35),
    #         fonts, 0.6, RED, 2)

    # # Show the frame on the screen
        
    cv2.imshow("frame", frame)

    # Quit the program if you press 'q' on keyboard
    if cv2.waitKey(1) == ord("q"):
        break

# Closing the camera
cap.release()

# Closing the windows that are opened
cv2.destroyAllWindows()

