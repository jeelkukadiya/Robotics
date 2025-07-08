import cv2 as cv

def draw_min_max_bounding_box(img, objects, color):
    for (x_min, y_min, x_max, y_max) in objects:
        cv.rectangle(img, (x_min, y_min), (x_max, y_max), color, 2)

def mark_centers_of_balls(img, balls, color):
    centers_of_balls = []
    for (x_min, y_min, x_max, y_max) in balls:
        center_x = int((x_min + x_max) / 2)
        center_y = int((y_min + y_max) / 2)
        centers_of_balls.append((center_x, center_y))
        cv.circle(img, (center_x, center_y), 3, color, -1)
    return centers_of_balls

def is_center_in_silo(center, silo):
    cx, cy = center
    x_min, y_min, x_max, y_max = silo
    return x_min <= cx <= x_max and y_min <= cy <= y_max



img = cv.imread("silo.jpg")

balls = [(60,260,145,342),(219,260,295,335),(239,196,313,266),(324,260,401,335),(345,196,419,264),(323,132,402,204),(442,257,516,326),(447,193,521,264),(561,249,639,320)]
silos = [(39,169,167,357),(219,152,323,336),(323,145,431,346),(427,146,540,338),(550,162,669,341)]

red_ball = [(219,260,295,335),(324,260,401,335),(345,196,419,264)]
blue_ball = [(60,260,145,342),(239,196,313,266),(323,132,402,204),(442,257,516,326),(447,193,521,264),(561,249,639,320)]

draw_min_max_bounding_box(img, balls, (0, 0, 255))  # Red bounding box for balls
draw_min_max_bounding_box(img, silos, (0, 255, 0))  # Green bounding box for silos

centers_of_balls = mark_centers_of_balls(img, balls, (255, 0, 0))  # Mark centers of balls

sorted_silos = sorted(silos, key=lambda x: x[0])
balls_in_silo = [[] for _ in sorted_silos]

for center, ball in zip(centers_of_balls, balls):
    ball_color = "RED" if ball in red_ball else "BLUE"
    for i, silo in enumerate(sorted_silos):
        if is_center_in_silo(center, silo):
            balls_in_silo[i].append(ball_color)  # Use "RED" or "BLUE" as a placeholder
            break

# Sort balls within each silo by their y-coordinate (bottom to top) and ensure 3 elements per silo
for i in range(len(balls_in_silo)):
    balls_in_silo[i] = sorted(balls_in_silo[i], key=lambda x: -centers_of_balls[balls.index(x)][1] if x in balls else 0)
    # Fill missing spots with empty strings to ensure 3 elements
    balls_in_silo[i] += [""] * (3 - len(balls_in_silo[i]))

print(balls_in_silo)

cv.imshow("Image with Bounding Boxes and Centers", img)
cv.waitKey(0)
cv.destroyAllWindows()