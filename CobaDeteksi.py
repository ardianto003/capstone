import torch
import cv2
import pathlib
from pathlib import Path
pathlib.PosixPath = pathlib.WindowsPath

# Load model YOLOv5
model = torch.hub.load('ultralytics/yolov5', 'custom', path='best.pt', force_reload=True)

# Menginisialisasi webcam (ID kamera 0, jika tidak terdeteksi coba ganti ke 1 atau 2)
cap = cv2.VideoCapture(0)

# Cek apakah webcam terbuka
if not cap.isOpened():
    print("Tidak bisa membuka webcam")
    exit()

while True:
    # Baca frame dari webcam
    ret, frame = cap.read()
    if not ret:
        print("Gagal mengambil gambar dari webcam")
        break

    # Deteksi objek pada frame
    results = model(frame)

    # Ambil output dengan bounding box
    labels, coords = results.xyxyn[0][:, -1], results.xyxyn[0][:, :-1]

    # Tampilkan hasil deteksi pada frame
    for i, (x_min, y_min, x_max, y_max, conf) in enumerate(coords):
        if conf > 0.5:  # Tampilkan hanya jika kepercayaan > 0.5
            # Convert koordinat normal ke pixel
            x1, y1, x2, y2 = int(x_min * frame.shape[1]), int(y_min * frame.shape[0]), \
                             int(x_max * frame.shape[1]), int(y_max * frame.shape[0])
            label = f"{model.names[int(labels[i])]}: {conf:.2f}"
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    
    # Tampilkan frame di jendela
    cv2.imshow('Webcam - Object Detection', frame)

    # Tekan 'q' untuk keluar
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Bersihkan dan tutup
cap.release()
cv2.destroyAllWindows()
