import os
import cv2
from ultralytics import YOLO
from config import *

# -----------------------------
# Load YOLO Model
# -----------------------------
model = YOLO(MODEL_NAME)
model.to("cuda")  # Use NVIDIA GPU

# -----------------------------
# Create Output Folder
# -----------------------------
os.makedirs(OUTPUT_VIDEO_FOLDER, exist_ok=True)


def detect_people(video_path, output_path):

    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print(f"Cannot open {video_path}")
        return

    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)

    writer = cv2.VideoWriter(
        output_path,
        cv2.VideoWriter_fourcc(*"mp4v"),
        fps,
        (width, height)
    )

    frame_count = 0

    while True:

        success, frame = cap.read()

        if not success:
            break

        frame_count += 1

        # Skip frames for faster processing
        if frame_count % FRAME_SKIP != 0:
            writer.write(frame)
            continue

        # Person Detection
        results = model.predict(
            frame,
            classes=[PERSON_CLASS_ID],
            verbose=False,
            device="cuda"
        )

        boxes = results[0].boxes

        if boxes is not None:

            for box in boxes:

                x1, y1, x2, y2 = map(int, box.xyxy[0])

                confidence = float(box.conf[0])

                # Draw Bounding Box
                cv2.rectangle(
                    frame,
                    (x1, y1),
                    (x2, y2),
                    (0, 255, 0),
                    2
                )

                # Draw Confidence
                cv2.putText(
                    frame,
                    f"Person {confidence:.2f}",
                    (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6,
                    (0, 255, 0),
                    2
                )

        writer.write(frame)

        cv2.imshow("Person Detection", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    writer.release()


def process_dataset():

    if TEST_MODE:
        video_files = [TEST_VIDEO]
    else:
        video_files = [
            file for file in os.listdir(DATASET_FOLDER)
            if file.endswith(".mp4")
        ]

    print(f"\nVideos to Process : {len(video_files)}\n")

    for video in video_files:

        print(f"Processing : {video}")

        input_video = os.path.join(DATASET_FOLDER, video)

        output_video = os.path.join(
            OUTPUT_VIDEO_FOLDER,
            video
        )

        detect_people(input_video, output_video)

    cv2.destroyAllWindows()

    print("\nPerson Detection Completed Successfully")


if __name__ == "__main__":
    process_dataset()