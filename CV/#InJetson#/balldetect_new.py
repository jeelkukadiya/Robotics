import argparse
import cv2
import numpy as np
import imutils
import time
import serial 
import collections

global_port = '/dev/ttyACM0'
detect_color = 'red'

# def setup_serial(port=global_port, baudrate=9600, timeout=1):
#     """ Initialize serial connection """
#     try:
#         ser = serial.Serial(port, baudrate, timeout=timeout)
#         if ser.is_open:
#             print(f"Serial port {port} opened successfully.")
#         return ser
#     except Exception as e:
#         print(f"Failed to connect to {port}: {str(e)}")
#         return None

# def write_verification_result(result):
#     with open("verification_result.txt", "w") as file:
#         file.write(result)

def detect_ball(ball_detected):
    with open("ball_detected.txt", "w") as file:
        file.write(ball_detected)
    # return ball_detected

def gstreamer_pipeline(
    sensor_id=0,
    capture_width=1920,
    capture_height=1080,
    display_width=960,
    display_height=540,
    framerate=30,
    flip_method=0,
):
    return (
        "nvarguscamerasrc sensor-id=%d ! "
        "video/x-raw(memory:NVMM), width=(int)%d, height=(int)%d, framerate=(fraction)%d/1 ! "
        "nvvidconv flip-method=%d ! "
        "video/x-raw, width=(int)%d, height=(int)%d, format=(string)BGRx ! "
        "videoconvert ! "
        "video/x-raw, format=(string)BGR ! appsink"
        % (
            sensor_id,
            capture_width,
            capture_height,
            framerate,
            flip_method,
            display_width,
            display_height,
        )
    )

# ap = argparse.ArgumentParser()
# ap.add_argument("-v", "--video",
# 	help="path to the (optional) video file")
# ap.add_argument("-b", "--buffer", type=int, default=64,
# 	help="max buffer size")
# ap.add_argument("-p", "--port", default=global_port,
#     help="serial port")
# args = vars(ap.parse_args())

# ser_port = setup_serial(args["port"], 9600)

# HSV颜色空间的最大值和最小值
# upper = [0, 0, 0]
# lower = [255, 255, 255]

# # 更新HSV最大值和最小值的函数
# def update_hsv_values(roi):
#     global upper, lower
#     # 转换ROI为数组
#     roi_array = roi.reshape(-1, 3)
#     roi_array = roi_array[np.all(roi_array != [0, 0, 0], axis=1)]
    
#     # 更新最大值和最小值
#     if roi_array.size > 0:
#         lower = np.min(roi_array, axis=0).tolist()
#         upper = np.max(roi_array, axis=0).tolist()

blueLower = (91, 126, 0)
blueUpper = (114, 254, 175)

#Upper HSV: [179, 247, 172] Lower HSV: [1, 5, 42]
# redUpper = (179, 247, 172)
# redLower = (1, 5, 42)

redUpper = (175, 255, 189)
redLower = (162, 56, 90)

# 开始捕捉视频
print("[INFO] starting video stream...")
vs = cv2.VideoCapture(gstreamer_pipeline(flip_method=0), cv2.CAP_GSTREAMER)
time.sleep(2.0)  # 让摄像头预热

# 创建窗口
# cv2.namedWindow("Color Picker")

frame_count = 0
start_time = time.time()

# last_done_time = None
ball_detected = 'no'
# detection_results = collections.deque(maxlen=30)

# write_verification_result("no")

while True:
    # 从视频流中读取帧
    ret, frame = vs.read()
    current_time = time.time()

    frame_count += 1
    # if we are viewing a video and we did not grab a frame, then we have reached the end of the video
    if frame is None:
        break

    frame = imutils.resize(frame, width=600)
    blurred = cv2.GaussianBlur(frame, (11, 11), 0)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

    # frame = imutils.resize(frame, width=600)
    # hsv_img = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask_blue = cv2.inRange(hsv, blueLower, blueUpper)
    mask_red = cv2.inRange(hsv, redLower, redUpper)

    if detect_color == 'blue':
        mask = cv2.erode(mask_blue, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)
        cv2.imshow("mask",mask)
        cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)  
    else:
        mask = cv2.erode(mask_red, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)
        cv2.imshow("mask",mask)
        cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)

    center = None
    # only proceed if at least one contour was found
    if len(cnts) > 0:
        # find the largest contour in the mask, then use it to compute the minimum enclosing circle and centroid
        c = max(cnts, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        M = cv2.moments(c)
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))


        if center is not None and radius > 10: #add threshold for crop frame
            ball_detected = 'yes'
            print("ball_detected", ball_detected)
        else:
            ball_detected = 'no'
            print("ball_detected", ball_detected)

        # only proceed if the radius meets a minimum size
        if radius > 10:
            # draw the circle and centroid on the frame, then update the list of tracked points
            cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 2)
            cv2.circle(frame, center, 5, (0, 0, 255), -1)
    # 显示图像

    # with open("done_message.txt", "r") as file:
    #     line = file.read().strip()
        # if file.read().strip() == "done":
        #     line = "done"

    elapsed_time = time.time() - start_time
    if elapsed_time > 0:
        fps = frame_count / elapsed_time
        cv2.putText(frame, f"FPS: {fps:.2f}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)    
    
    # show the frame to our screen
    cv2.imshow("Frame", frame)
    detect_ball(ball_detected)

    # if line == "done":
    #     last_done_time = current_time
    #     if ball_detected == "yes":
    #         detection_results.append("yes")
    #     else:
    #         detection_results.append("no")
    # elif last_done_time and (current_time - last_done_time < 3):
    #     detection_results.append(ball_detected)
    #     if current_time - last_done_time >= 3:
    #         most_common_result = collections.Counter(detection_results).most_common(1)[0][0]
    #         # write_verification_result(most_common_result)
    #         print("most_common_result",most_common_result)
    #         break

    key = cv2.waitKey(1) & 0xFF
    # if the 'q' key is pressed, stop the loop
    if key == ord("q"):
        break

    # cv2.imshow("Color Picker", frame)

    # # 捕获键盘事件
    # key = cv2.waitKey(1) & 0xFF
    
    # # 按下 'r' 键选择ROI
    # if key == ord('r'):
    #     roi = cv2.selectROI("Color Picker", frame, fromCenter=False, showCrosshair=True)
    #     if roi != (0, 0, 0, 0):
    #         x, y, w, h = roi
    #         selected_roi = hsv_img[y:y+h, x:x+w]
    #         update_hsv_values(selected_roi)
    #         print(f"Upper HSV: {upper} Lower HSV: {lower}")
    
    # # 按下 'q' 键退出循环
    # if key == ord('q'):
    #     break

# 释放资源
cv2.destroyAllWindows()
vs.release()