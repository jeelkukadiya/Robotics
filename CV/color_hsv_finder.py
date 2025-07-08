import cv2
import urllib.request
import numpy as np
 
def nothing(x):
    pass
 
def use_values(l_h, l_s, l_v, u_h, u_s, u_v):
    # Example function that uses the values
    print(f"LH: {l_h}, LS: {l_s}, LV: {l_v}, UH: {u_h}, US: {u_s}, UV: {u_v}")

#change the IP address below according to the
#IP shown in the Serial monitor of  Arduino code
 
cv2.namedWindow("live transmission", cv2.WINDOW_AUTOSIZE)
 
cv2.namedWindow("Tracking")
cv2.createTrackbar("LH", "Tracking", 0, 255, nothing)
cv2.createTrackbar("LS", "Tracking", 0, 255, nothing)
cv2.createTrackbar("LV", "Tracking", 0, 255, nothing)
cv2.createTrackbar("UH", "Tracking", 255, 255, nothing)
cv2.createTrackbar("US", "Tracking", 255, 255, nothing)
cv2.createTrackbar("UV", "Tracking", 255, 255, nothing)
 
while True:
    # imgnp=cv2.imread("blue.jpg")
    # frame=cv2.imdecode(imgnp,-1)

    #BLUE:LH: 83, LS: 62, LV: 24, UH: 134, US: 187, UV: 118
    #RED:LH: 0, LS: 147, LV: 0, UH: 88, US: 227, UV: 199

    frame = cv2.imread("bvm.jpg") 
    frame = cv2.resize(frame, (640, 480))
    
    
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
 
    l_h = cv2.getTrackbarPos("LH", "Tracking")
    l_s = cv2.getTrackbarPos("LS", "Tracking")
    l_v = cv2.getTrackbarPos("LV", "Tracking")
 
    u_h = cv2.getTrackbarPos("UH", "Tracking")
    u_s = cv2.getTrackbarPos("US", "Tracking")
    u_v = cv2.getTrackbarPos("UV", "Tracking")

    # Use the values here or pass them to another function
    use_values(l_h, l_s, l_v, u_h, u_s, u_v)
 
    l_b = np.array([l_h, l_s, l_v])
    u_b = np.array([u_h, u_s, u_v])
    
    mask = cv2.inRange(hsv, l_b, u_b) 
    res = cv2.bitwise_and(frame, frame, mask=mask)
 
    cv2.imshow("live transmission", frame)
    cv2.imshow("mask", mask)
    cv2.imshow("res", res)
    key=cv2.waitKey(5)
    if key==ord('q'):
        break
    
cv2.destroyAllWindows()