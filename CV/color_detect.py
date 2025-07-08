import cv2 as cv
import numpy as np

def preprocess_image(img):
    # img = cv.imread(image_path)
    # Convert to HSV
    hsv_img = cv.cvtColor(img, cv.COLOR_BGR2HSV)
    return hsv_img

def detect_balls(hsv_img):
    # Define approximate HSV color ranges for the balls
    color_ranges = {
        "red1": ((0, 100, 100), (10, 255, 255)),
        "red2": ((160, 100, 100), (180, 255, 255)),
        "purple": ((130, 50, 50), (160, 255, 255)),  # Adjusted for purple
        "blue": ((100, 150, 50), (130, 255, 255))  # Adjusted for blue
    }
    
    detected_balls = []
    
    for color, (lower, upper) in color_ranges.items():
        mask = cv.inRange(hsv_img, np.array(lower), np.array(upper))
        # Special handling for red to combine two ranges
        if color == "red1" or color == "red2":
            if color == "red1":
                lower2, upper2 = color_ranges["red2"]
                mask2 = cv.inRange(hsv_img, np.array(lower2), np.array(upper2))
                mask = cv.bitwise_or(mask, mask2)
            color_label = "red"  # Use a common label for both red ranges
        else:
            color_label = color  # Use the actual color name
        
        # Apply morphological operations
        mask = cv.morphologyEx(mask, cv.MORPH_OPEN, np.ones((3, 3), np.uint8))
        mask = cv.morphologyEx(mask, cv.MORPH_CLOSE, np.ones((5, 5), np.uint8))
        
        # Find contours and extract bounding boxes
        contours, _ = cv.findContours(mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
        for cnt in contours:
            x, y, w, h = cv.boundingRect(cnt)
            if w*h > 100:  # Filter out small areas
                detected_balls.append((color_label, (x, y, w, h)))
                
    return detected_balls

def draw_bounding_boxes(original_img, detected_balls):
    for color, (x, y, w, h) in detected_balls:
        cv.rectangle(original_img, (x, y), (x+w, y+h), (0, 255, 0), 2)
        cv.putText(original_img, color, (x, y-10), cv.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
    cv.imshow("Detected Balls", original_img)
    cv.waitKey(0)
    cv.destroyAllWindows()

# Main program
if __name__ == "__main__":
    image_path = "1.png"
    original_img = cv.imread(image_path)
    original_img = cv.resize(original_img,(640,480))
    hsv_img = preprocess_image(original_img)

    red_lower1 = np.array([0, 100, 100])
    red_upper1 = np.array([10, 255, 255])
    red_lower2 = np.array([160, 100, 100])
    red_upper2 = np.array([180, 255, 255])

    mask1 = cv.inRange(hsv_img, red_lower1, red_upper1)
    mask2 = cv.inRange(hsv_img, red_lower2, red_upper2)
    red_mask = cv.bitwise_or(mask1, mask2)

    detected_balls = detect_balls(hsv_img)
    draw_bounding_boxes(original_img, detected_balls)



