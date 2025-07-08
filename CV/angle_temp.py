import numpy as np
import cv2

def find_real_coordinates(u, v, Z, fx, fy, cx, cy):
    # Calculate X and Y coordinates using depth information
    X = (u - cx) * Z / fx
    Y = (v - cy) * Z / fy
    return X, Y, Z

def mouse_callback(event, x, y, flags, param):
    global depth_image, fx, fy, cx, cy

    if event == cv2.EVENT_MOUSEMOVE:
        depth = depth_image[y, x]
        X, Y, Z = find_real_coordinates(x, y, depth, fx, fy, cx, cy)
        # Display real-world coordinates on the depth image
        cv2.circle(color_image, (x, y), 5, (0, 255, 0), -1)  # Mark the point with a green circle
        cv2.putText(color_image, f"X: {X:.2f} mm, Y: {Y:.2f} mm, Z: {Z:.2f} mm", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        cv2.imshow('Color Image', color_image)


# Initialize camera parameters (you need to set these values based on your camera)
fx = 500.0  # Focal length in pixels (horizontal axis)
fy = 500.0  # Focal length in pixels (vertical axis)
cx = 320    # Principal point (horizontal coordinate)
cy = 240    # Principal point (vertical coordinate)

# Start webcam
cap = cv2.VideoCapture(0)

try:
    while True:
        ret, color_image = cap.read()
        if not ret:
            continue

        # Capture depth image
        ret, depth_image = cap.read()
        if not ret:
            continue

        # Show depth image
        cv2.imshow('Depth Image', depth_image)

        # Set mouse callback function
        cv2.setMouseCallback('Depth Image', mouse_callback)

        # Wait for key press
        key = cv2.waitKey(1)
        if key == ord('q'):
            break

finally:
    cap.release()
    cv2.destroyAllWindows()
