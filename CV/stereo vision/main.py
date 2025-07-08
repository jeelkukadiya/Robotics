import os
from ultralytics import YOLO
import cv2
import torch

# Select GPU device 0 (if you have multiple GPUs, adjust accordingly)
device = torch.device("cuda:1" if torch.cuda.is_available() else "cpu")

VIDEOS_DIR = os.path.join('.', 'videos')


cap = cv2.VideoCapture(0)
cap.set(3,1920)
cap.set(4,1080)

model_path = os.path.join('best.pt')

model = YOLO(model_path)
threshold = 0.5

while True:
    
    ret, frame = cap.read()
    results = model(frame)[0]

    for result in results.boxes.data.tolist():
        x1, y1, x2, y2, score, class_id = result

        if score > threshold:
            cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 4)
            cv2.putText(frame, results.names[int(class_id)].upper(), (int(x1), int(y1 - 10)),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 255, 0), 3, cv2.LINE_AA)

    cv2.imshow("YOLO Object Detection", frame)
    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()