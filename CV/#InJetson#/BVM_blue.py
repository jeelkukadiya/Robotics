import cv2
import pyrealsense2 as rs
from ultralytics import YOLO
import numpy as np
import torch

# Load the trained YOLOv8x model
model = YOLO('C:\\RoboCon\\runs\detect\\train4\\weights\\best.pt').to('cuda')  # Use the YOLOv8x model and move to GPU

# Configure Intel RealSense camera
pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

# Start streaming
pipeline.start(config)

# Function to get current threshold value from trackbar
def get_threshold(x):
    global threshold
    threshold = x / 100.0

# Function to get current confidence value from trackbar
def get_confidence(x):
    global confidence
    confidence = x / 100.0

# Function to get current brightness value from trackbar
def get_brightness(x):
    global brightness
    brightness = x - 50

# Function to get current contrast value from trackbar
def get_contrast(x):
    global contrast
    contrast = x / 50.0

# Create a window
cv2.namedWindow('RealSense')

# Create trackbars for threshold, confidence, brightness, and contrast
cv2.createTrackbar('Threshold', 'RealSense', 50, 100, get_threshold)
cv2.createTrackbar('Confidence', 'RealSense', 50, 100, get_confidence)
cv2.createTrackbar('Brightness', 'RealSense', 50, 100, get_brightness)
cv2.createTrackbar('Contrast', 'RealSense', 50, 100, get_contrast)

# Initialize global variables
threshold = 0.5
confidence = 0.5
brightness = 0
contrast = 1.0

# blueUpper = (112, 190, 168)
# blueLower = (101, 40, 3)

#Upper HSV: [173, 255, 171] Lower HSV: [5, 9, 5]

blueUpper = (173,255,171)
blueLower = (5,9,5)

color_ranges = {
    "red": ((161, 49, 61), (255, 255, 255)),  # Adjusted range for red
    "blue": ((5,9,5), (173,255,171)),  # Keeping blue the same
    "purple": ((120, 12, 47), (165, 163, 255))  # Adjusted range for purple to not overlap with red
}

def verify_blue_hsv(image, x1, y1, x2, y2):
    center_x = (x1+x2) / 2
    center_y = (y1+y2) / 2

    
    # cv2.rectangle(color_image, (x-10, y-10), (x+10, y+10), (0, 255, 0), 2)

    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    # avg_hsv = np.mean(hsv, axis=(0,1))

            # Define a smaller region around the center (e.g., a 10x10 square)
    region_size = 10
    region_half = region_size // 2
    region_x1, region_y1 = max(center_x - region_half, 0), max(center_y - region_half, 0)
    region_x2, region_y2 = min(center_x + region_half, image.shape[1]), min(center_y + region_half, image.shape[0])

     # Sample the smaller region
    sampled_region = hsv_image[int(region_y1):int(region_y2), int(region_x1):int(region_x2)]

    max_color = ''
    max_count = 0
    for color, (lower, upper) in color_ranges.items():
        mask = cv2.inRange(sampled_region, np.array(lower), np.array(upper))
        count = cv2.countNonZero(mask)
        if count > max_count:
            max_count = count
            max_color = color

    return max_color

    # if max_color:
    #     classified_balls[max_color].append(box)
    #     cv.rectangle(image, (x1, y1), (x2, y2), colors[max_color], 2)

    # if blueLower[0] < avg_hsv[0] < blueUpper[0] and blueLower[1] < avg_hsv[1] < blueUpper[1] and blueLower[2] < avg_hsv[2] < blueUpper[2]:
    #     return True
    # else:
    #     return False

    # mask = cv2.inRange(hsv, blueLower, blueUpper)
    # mask = cv2.erode(mask, None, iterations=2)
    # mask = cv2.dilate(mask, None, iterations=2)
    # return mask 

try:
    while True:
        # Wait for a coherent pair of frames: depth and color
        frames = pipeline.wait_for_frames()
        color_frame = frames.get_color_frame()
        if not color_frame:
            continue

        # Convert images to numpy arrays
        color_image = np.asanyarray(color_frame.get_data())

        # Adjust brightness and contrast
        color_image = cv2.convertScaleAbs(color_image, alpha=contrast, beta=brightness)

        # Perform object detection
        results = model(color_image)

        # Draw bounding boxes and labels on the image
        for result in results:
            boxes = result.boxes
            for box in boxes:
                x1, y1, x2, y2 = box.xyxy[0].tolist()
                #ball bbox
                conf = box.conf.item()  # Convert Tensor to float
                cls = int(box.cls.item())  # Convert Tensor to int

                if conf >= confidence:  # Apply confidence threshold
                    label = f'{model.names[cls]}: {conf:.2f}'

                    color = verify_blue_hsv(color_image,int(x1),int(y1),int(x2),int(y2))
                    print(color)

                    if label == 'blue' and color == 'blue':

                        cv2.rectangle(color_image, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
                        cv2.putText(color_image, label, (int(x1), int(y1) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
                    else:
                        label = 'purple'
                    #add logic of blue to original_blue and purple
                        cv2.rectangle(color_image, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
                        cv2.putText(color_image, label, (int(x1), int(y1) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

        # Display the resulting frame
        cv2.imshow('RealSense', color_image)

        # Break the loop on 'q' key press
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
finally:
    # Stop streaming
    pipeline.stop()

# Release the window
cv2.destroyAllWindows()