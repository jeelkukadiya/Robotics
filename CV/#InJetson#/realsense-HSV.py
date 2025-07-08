#c:\Users\ASUS\Downloads\USB-HSV.py
import cv2
import numpy as np
import pyrealsense2 as rs
import time

# HSV颜色空间的最大值和最小值
upper = [0, 0, 0]
lower = [255, 255, 255]

# 更新HSV最大值和最小值的函数
def update_hsv_values(roi):
    global upper, lower
    # 转换ROI为数组
    roi_array = roi.reshape(-1, 3)
    roi_array = roi_array[np.all(roi_array != [0, 0, 0], axis=1)]
    
    # 更新最大值和最小值
    if roi_array.size > 0:
        lower = np.min(roi_array, axis=0).tolist()
        upper = np.max(roi_array, axis=0).tolist()

# 配置RealSense流
pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

# 开始捕捉视频
print("[INFO] starting video stream...")
pipeline.start(config)
time.sleep(2.0)  # 让摄像头预热

# 创建窗口
cv2.namedWindow("Color Picker")

while True:
    # 从RealSense流中读取帧
    frames = pipeline.wait_for_frames()
    color_frame = frames.get_color_frame()
    if not color_frame:
        continue

    frame = np.asanyarray(color_frame.get_data())
    hsv_img = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    # 显示图像
    cv2.imshow("Color Picker", frame)

    # 捕获键盘事件
    key = cv2.waitKey(1) & 0xFF
    
    # 按下 'r' 键选择ROI
    if key == ord('r'):
        roi = cv2.selectROI("Color Picker", frame, fromCenter=False, showCrosshair=True)
        if roi != (0, 0, 0, 0):
            x, y, w, h = roi
            selected_roi = hsv_img[y:y+h, x:x+w]
            update_hsv_values(selected_roi)
            print(f"Upper HSV: {upper} Lower HSV: {lower}")
    
    # 按下 'q' 键退出循环
    if key == ord('q'):
        break

# 释放资源
cv2.destroyAllWindows()
pipeline.stop()