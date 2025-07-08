import cv2 as cv
import numpy as np
import imutils

# Define colors and their corresponding HSV ranges
colors = {
    'my_red_color': [np.array([0, 100, 100]), np.array([10, 255, 255])],  # Red hue wraps around
    'my_blue_color': [np.array([97, 100, 100]), np.array([117, 255, 255])],
    'my_purple_color': [np.array([145, 100, 100]), np.array([165, 255, 255])]
}

def find_color(frame, points):
    mask = cv.inRange(frame, points[0], points[1])  # Create mask with boundaries
    # Apply morphological operations to reduce noise
    mask = cv.erode(mask, None, iterations=2)
    mask = cv.dilate(mask, None, iterations=2)
    cnts = cv.findContours(mask.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    for c in cnts:
        area = cv.contourArea(c)
        if area > 0.1:  # Adjust as necessary
            # Compute the centroid of the contour
            M = cv.moments(c)
            if M["m00"] != 0:
                cx = int(M["m10"] / M["m00"])
                cy = int(M["m01"] / M["m00"])
                return c, cx, cy
    return None, None, None

cap = cv.VideoCapture(0)

while cap.isOpened():
    _, frame = cap.read()
    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    
    # Create a black mask
    mask_all = np.zeros_like(frame)

    for name, clr in colors.items():
        c, cx, cy = find_color(hsv, clr)
        if c is not None:
            cv.drawContours(mask_all, [c], -1, (255, 255, 255), -1)  # Draw contours on black mask

    # Bitwise AND operation to mask the original frame with the created mask
    result = cv.bitwise_and(frame, mask_all)

    cv.imshow("Result", result)
    if cv.waitKey(1) == ord('q'):
        break

cap.release()
cv.destroyAllWindows()
