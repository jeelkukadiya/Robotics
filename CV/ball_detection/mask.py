import cv2 as cv
import numpy as np
import imutils


color = (0,0,0)
# I have defined lower and upper boundaries for each color for my camera
# Strongly recommended finding for your own camera.

#RED    [244, 54, 76]
#BLUE   [161,90,149]
#PURPLE [48,127,226]

colors = {'red': [np.array([167, 100, 100]), np.array([187, 255, 255])],
          'blue': [np.array([97,100,100]), np.array([117,255,255])],
          'purple': [np.array([145,100,100]), np.array([165,255,255])]}
          


def find_color(frame, points):
    mask = cv.inRange(frame, points[0], points[1])#create mask with boundaries 
    cnts = cv.findContours(mask, cv.RETR_TREE, 
                           cv.CHAIN_APPROX_SIMPLE) # find contours from mask
    cnts = imutils.grab_contours(cnts)
    for c in cnts:
        area = cv.contourArea(c) # find how big countour is
        if area > 500:       # only if countour is big enough, then
            M = cv.moments(c)
            cx = int(M['m10'] / M['m00']) # calculate X position
            cy = int(M['m01'] / M['m00']) # calculate Y position
            return c, cx, cy

cap = cv.VideoCapture(1)

while cap.isOpened(): #main loop
    _, frame = cap.read()
    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV) #convertion to HSV
    for name, clr in colors.items(): # for each color in colors
        if find_color(hsv, clr):  # call find_color function above
            c, cx, cy = find_color(hsv, clr)
            cv.drawContours(frame, [c], -1, color, 3) #draw contours
            cv.circle(frame, (cx, cy), 7, color, -1)  # draw circle
            cv.putText(frame, name, (cx,cy), 
                        cv.FONT_HERSHEY_SIMPLEX, 1, color, 1) # put text
    cv.imshow("Frame: ", frame) # show image
    if cv.waitKey(1) == ord('q'):
        break

cap.release()   #idk what it is
cv.destroyAllWindows() # close all windows opened by opencv