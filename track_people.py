import os
import cv2
import torch
from ultralytics import YOLO
from config import *

# ==========================================
# DEVICE
# ==========================================

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

print(f"\nUsing Device : {DEVICE.upper()}")

# ==========================================
# LOAD MODEL
# ==========================================

model = YOLO(MODEL_NAME)
model.to(DEVICE)

# ==========================================
# OUTPUT FOLDER
# ==========================================

os.makedirs(TRACK_OUTPUT_FOLDER, exist_ok=True)

# ==========================================
# TRACK SINGLE VIDEO
# ==========================================

def track_video(video_path, output_path):

    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print("Cannot open :", video_path)
        return

    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)

    writer = cv2.VideoWriter(
        output_path,
        cv2.VideoWriter_fourcc(*'mp4v'),
        fps,
        (width, height)
    )

    cv2.namedWindow("Tracking", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Tracking", 1400, 800)

    frame_number = 0

    while True:

        success, frame = cap.read()

        if not success:
            break

        frame_number += 1

        if FRAME_SKIP > 1:

            if frame_number % FRAME_SKIP != 0:
                writer.write(frame)
                continue

        results = model.track(
            frame,
            classes=[PERSON_CLASS_ID],
            tracker="bytetrack.yaml",
            persist=True,
            conf=0.4,
            iou=0.5,
            verbose=False
        )

        if results[0].boxes is not None:

            for box in results[0].boxes:

                x1, y1, x2, y2 = map(int, box.xyxy[0])

                confidence = float(box.conf[0])

                if box.id is None:
                    person_id = -1
                else:
                    person_id = int(box.id[0])

                cv2.rectangle(
                    frame,
                    (x1, y1),
                    (x2, y2),
                    (0,255,0),
                    2
                )

                cv2.putText(
                    frame,
                    f"ID {person_id}",
                    (x1,y1-10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (0,255,0),
                    2
                )

                cv2.putText(
                    frame,
                    f"{confidence:.2f}",
                    (x1,y2+20),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6,
                    (0,255,255),
                    2
                )

        writer.write(frame)

        display = cv2.resize(frame, (1400,800))

        cv2.imshow("Tracking", display)

        key = cv2.waitKey(1)

        if key == ord("q"):
            break

    cap.release()
    writer.release()

# ==========================================
# PROCESS DATASET
# ==========================================

def process_dataset():

    if TEST_MODE:

        videos = [TEST_VIDEO]

    else:

        videos = [
            file
            for file in os.listdir(DATASET_FOLDER)
            if file.endswith(".mp4")
        ]

    print(f"\nVideos to Process : {len(videos)}\n")

    for video in videos:

        print("Tracking :", video)

        input_video = os.path.join(
            DATASET_FOLDER,
            video
        )

        output_video = os.path.join(
            TRACK_OUTPUT_FOLDER,
            video
        )

        track_video(
            input_video,
            output_video
        )

    cv2.destroyAllWindows()

    print("\nTracking Completed Successfully!")

# ==========================================
# MAIN
# ==========================================

if __name__ == "__main__":

    process_dataset()