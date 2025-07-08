import cv2 as cv
import numpy as np

#original
color_ranges = {
    "red": ((161, 49, 61), (255, 255, 255)),  # Adjusted range for red
    "blue": ((101, 24, 0), (121, 255, 255)),  # Keeping blue the same
    "purple": ((120, 12, 47), (165, 163, 255))  # Adjusted range for purple to not overlap with red
}

# Define BGR colors for drawing rectangles
colors = {
    "red": (76, 54, 244),  # Example for red
    "blue": (226, 127, 48),  # Example for blue
    "purple": (149, 90, 161)  # Example for purple
}

#wrong
# color_ranges = {
#     "red": ((0, 59, 121), (57, 255, 208)),  # Adjusted range for red
#     "blue": ((82, 104, 57), (125, 255, 255)),  # Keeping blue the same
#     "purple": ((127, 68, 99), (160, 160, 141))  # Adjusted range for purple to not overlap with red
# }
# colors = {
#     "red": (76, 54, 244),  # Example for red
#     "blue": (226, 127, 48),  # Example for blue
#     "purple": (92, 43, 99)  # Example for purple
# }

# Function to be called whenever a mouse event happens
def click_event(event, x, y, flags, param):
    if event == cv.EVENT_LBUTTONDOWN:  # Left button click
        print(x,",",y)
        # Optionally, you can also mark the clicked point on the image
        cv.circle(img, (x, y), 3, (255, 0, 255), -1)
        cv.imshow("Image", img)

def draw_min_max_bounding_box(img, objects, color):
    """
    Draws a bounding box around the minimum and maximum coordinates of given objects.

    Parameters:
    - img: The image on which to draw.
    - objects: A list of tuples, each representing the bounding box of an object
               in the form (x_min, y_min, x_max, y_max).
    - color: A tuple for the color of the bounding box (B, G, R).
    """
    if not objects:
        return  # No objects to draw a box around
    
    for (x_min, y_min, x_max, y_max) in objects:
        cv.rectangle(img, (x_min, y_min), (x_max, y_max), color, 2)

def mark_centers_of_balls(img, balls, color):
    """
    Marks the center of each ball's bounding box on the image.

    Parameters:
    - img: The image on which to draw.
    - balls: A list of tuples, each representing the bounding box of a ball
             in the form (x_min, y_min, x_max, y_max).
    - color: A tuple for the color of the center mark (B, G, R).
    """
    centers_of_balls = []
    for (x_min, y_min, x_max, y_max) in balls:
        # Calculate the center of the bounding box
        center_x = int((x_min + x_max) / 2)
        center_y = int((y_min + y_max) / 2)
        centers_of_balls.append((center_x, center_y))
        
        # Draw a small circle at the center
        cv.circle(img, (center_x, center_y), 3, color, -1)
    
    return centers_of_balls

def is_center_in_silo(center, silo):
    cx, cy = center
    x_min, y_min, x_max, y_max = silo
    return x_min <= cx <= x_max and y_min <= cy <= y_max

def classify_and_visualize_balls(image, balls):
    hsv_image = cv.cvtColor(image, cv.COLOR_BGR2HSV)
    classified_balls = {"red": [], "blue": [], "purple": []}

    for box in balls:
        x1, y1, x2, y2 = box
        # Calculate the center of the bounding box
        center_x, center_y = (x1 + x2) // 2, (y1 + y2) // 2

        # Define a smaller region around the center (e.g., a 10x10 square)
        region_size = 10
        region_half = region_size // 2
        region_x1, region_y1 = max(center_x - region_half, 0), max(center_y - region_half, 0)
        region_x2, region_y2 = min(center_x + region_half, image.shape[1]), min(center_y + region_half, image.shape[0])

        # Sample the smaller region
        sampled_region = hsv_image[region_y1:region_y2, region_x1:region_x2]

        # Flatten the region to a list of pixels
        pixels = sampled_region.reshape(-1, sampled_region.shape[-1])

        # Determine the most frequently occurring color in the region
        max_color = ''
        max_count = 0
        for color, (lower, upper) in color_ranges.items():
            mask = cv.inRange(sampled_region, np.array(lower), np.array(upper))
            count = cv.countNonZero(mask)
            if count > max_count:
                max_count = count
                max_color = color

        if max_color:
            classified_balls[max_color].append(box)
            cv.rectangle(image, (x1, y1), (x2, y2), colors[max_color], 2)

    # cv.imshow('Classified Balls', image)
    # cv.waitKey(0)
    # cv.destroyAllWindows()

    # for color, boxes in classified_balls.items():
    #     print(f"{color.capitalize()} balls:", boxes)

    # return classified_balls
    return {
        "red_ball": classified_balls["red"],
        "blue_ball": classified_balls["blue"],
        "purple_ball": classified_balls["purple"]
    }

img = cv.imread("xy.jpg")
img = cv.resize(img,(640,480))
# for image 9.jpg
# balls_float = [
#     (66.41960144042969 , 270.59527587890625 , 126.72383117675781 , 339.4127197265625),(
# 290.324951171875 , 282.27410888671875 , 343.2933349609375 , 353.672607421875),(
# 419.2613525390625 , 225.18524169921875 , 472.3126220703125 , 289.17156982421875),(
# 278.931884765625 , 216.138916015625 , 329.7767333984375 , 284.0390625),(
# 547.271728515625 , 293.94561767578125 , 606.653564453125 , 362.78155517578125),(
# 169.01199340820312 , 215.85519409179688 , 226.03781127929688 , 277.7164001464844),(
# 401.33770751953125 , 283.4932861328125 , 452.2261962890625 , 353.6011962890625),(
# 166.10882568359375 , 147.7796630859375 , 224.66415405273438 , 221.59490966796875),(
# 172.58132934570312 , 279.036376953125 , 227.19979858398438 , 348.1397705078125)
# ]

# for xy.jpg
balls_float = [(61 , 245,100 , 305),(51 , 302,97 , 365),(164 , 187,215 , 252),(174 , 249,218 , 301),(171 , 304,222 , 360),(294 , 187,343 , 248),(289 , 249,338 , 305),(290 , 304,340 , 364),(412 , 191,460 , 255),(403 , 244,450 , 303),(408 , 307,454 , 361),(526 , 233,578 , 301),(521 , 300,568 , 359)]

balls = [(int(x1), int(y1), int(x2), int(y2)) for x1, y1, x2, y2 in balls_float]

# balls = [(60,260,145,342),(219,260,295,335),(239,196,313,266),(324,260,401,335),(345,196,419,264),(323,132,402,204),(442,257,516,326),(447,193,521,264),(561,249,639,320)]


# silos = [(39,169,167,357),(219,152,323,336),(323,145,431,346),(427,146,540,338),(550,162,669,341)]

# for image 9.jpg
# silos = [(27,170,120,365),(148,170,235,362),(274,170,344,373),(398,170,464,372),(528,170,598,381)]

# for xy.jpg
silos = [(42 , 207,118 , 371),(158 , 189,225 , 373),(270 , 183,349 , 382),(397 , 195,458 , 377),(518 , 192,566 , 382)]

result = classify_and_visualize_balls(img,balls)
red_ball = result["red_ball"]
blue_ball = result["blue_ball"]
purple_ball = result["purple_ball"]
# print("red_ball:",red_ball)
# print("blue_ball:",blue_ball)
# print("purple_ball:",purple_ball)


# for 9.jpg
# red_ball = [(219,260,295,335),(324,260,401,335),(345,196,419,264)]
# blue_ball = [(60,260,145,342),(239,196,313,266),(323,132,402,204),(442,257,516,326),(447,193,521,264),(561,249,639,320)]

draw_min_max_bounding_box(img, red_ball, (0, 0, 255))  # Red bounding box for all red balls
draw_min_max_bounding_box(img, blue_ball, (255, 0, 0))  # Blue bounding box for all blue balls
draw_min_max_bounding_box(img, silos, (255, 255, 255))  # Green bounding box for all silos

# Mark the centers of the balls
centers_of_balls = mark_centers_of_balls(img, balls, (0, 255, 0)) 

#print(centers_of_balls) # Using green color for the center marks

sorted_silos = sorted(silos, key=lambda x: x[0])

# print("silo:",sorted_silos)

balls_in_silo = [[] for _ in sorted_silos]

for center, ball in zip(centers_of_balls, balls):
    # ball_color = "RED" if ball in red_ball else "BLUE" if ball in blue_ball else "PURPLE"#"PURPLE" if ball in purple_ball else ""

    for i, silo in enumerate(sorted_silos):
        if is_center_in_silo(center, silo):
            balls_in_silo[i].append(ball)  # Use "BALL" as a placeholder
            break

# print(balls_in_silo)
    
# Sort balls within each silo by their y-coordinate (bottom to top) and ensure 3 elements per silo
# for i in range(len(balls_in_silo)):
#     balls_in_silo[i] = sorted(balls_in_silo[i], key=lambda x: -centers_of_balls[balls.index(x)][1] if x in balls else 0)
#     # Fill missing spots with empty strings to ensure 3 elements
#     balls_in_silo[i] += [""] * (3 - len(balls_in_silo[i]))


def get_ball_color(ball):
    if ball in red_ball:
        return "RED"
    elif ball in blue_ball:
        return "BLUE"
    elif ball in purple_ball:
        return "PURPLE"
    else:
        return ""
    
# Sort balls within each silo by their y-coordinate (bottom to top)
for i in range(len(balls_in_silo)):
    # Sort based on the y-coordinate of the ball's center
    balls_in_silo[i] = sorted(balls_in_silo[i], key=lambda ball: -((ball[1] + ball[3]) // 2))

    # Convert sorted ball tuples to their colors or placeholders
    balls_in_silo[i] = [get_ball_color(ball) for ball in balls_in_silo[i]]

    # Ensure 3 elements per silo, filling missing spots with placeholders
    while len(balls_in_silo[i]) < 3:
        balls_in_silo[i].append("")

print(balls_in_silo)

# Ensure the window is created by displaying the image before setting the mouse callback
cv.imshow("Image", img)


cv.setMouseCallback("Image", click_event)

cv.waitKey(0)
cv.destroyAllWindows()