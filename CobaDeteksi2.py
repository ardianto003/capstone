import torch
import cv2
import pathlib
import serial
import time
from pathlib import Path
pathlib.PosixPath = pathlib.WindowsPath
import warnings
# warnings.filterwarnings("ignore", message="`torch.cuda.amp.autocast(args...)` is deprecated. Please use `torch.amp.autocast('cuda', args...)` instead.")
warnings.filterwarnings("ignore", category=FutureWarning)

# Initialize serial communication
# ser = serial.Serial('COM1', 9600)  # Adjust COM port as needed
time.sleep(2)  # Give some time for the serial connection to initialize

# Load YOLOv5 model
model = torch.hub.load('ultralytics/yolov5', 'custom', path='best.pt', force_reload=True)

# Initialize webcam (Camera ID 0; try 1 or 2 if not detected)
cap = cv2.VideoCapture(1)

# Check if the webcam is open
if not cap.isOpened():
    print("Cannot open webcam")
    exit()

while True:
    # Read frame from webcam
    ret, frame = cap.read()
    if not ret:
        print("Failed to capture image from webcam")
        break

    # Object detection on frame
    results = model(frame)

    # Extract output with bounding boxes
    labels, coords = results.xyxyn[0][:, -1], results.xyxyn[0][:, :-1]

    motorcycle_detected = False  # Flag to check if motorcycle is seen

    # Display detection results on frame
    for i, (x_min, y_min, x_max, y_max, conf) in enumerate(coords):
        if conf > 0.5:  # Only display if confidence > 0.5
            # Convert normalized coordinates to pixels
            x1, y1, x2, y2 = int(x_min * frame.shape[1]), int(y_min * frame.shape[0]), \
                             int(x_max * frame.shape[1]), int(y_max * frame.shape[0])
            label = f"{model.names[int(labels[i])]}: {conf:.2f}"
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            
            # Check if detected object is a motorcycle
            motorcycle_detected = True

    # Send serial signal based on detection
    if motorcycle_detected:
        # ser.write(b'CLOSE')  # Send 'CLOSE' command to close the barrier
        print("Motorcycle detected - closing barrier")
    else:
        # ser.write(b'OPEN')   # Send 'OPEN' command to open the barrier
        print("No motorcycle detected - opening barrier")
    
    # Display the frame in a window
    cv2.imshow('Webcam - Object Detection', frame)

    # Press 'q' to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Cleanup and close
cap.release()
cv2.destroyAllWindows()
# ser.close()  # Close serial connection
