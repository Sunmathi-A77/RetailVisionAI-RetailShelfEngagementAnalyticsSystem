import cv2
import json
import os
from config import *

# -----------------------------
# SETTINGS
# -----------------------------
MAX_SHELVES = 5          # Change if your store has more racks

# -----------------------------
# Load First Frame
# -----------------------------
video_path = os.path.join(DATASET_FOLDER, TEST_VIDEO)

cap = cv2.VideoCapture(video_path)

ret, original_frame = cap.read()

if not ret:
    print("Cannot read video.")
    exit()

cap.release()

# -----------------------------
# Resize Frame for Display
# -----------------------------
screen_width = 1400

h, w = original_frame.shape[:2]

scale = screen_width / w

display_width = int(w * scale)
display_height = int(h * scale)

display_frame = cv2.resize(
    original_frame,
    (display_width, display_height)
)

frame = display_frame.copy()

# -----------------------------
# Variables
# -----------------------------
drawing = False
ix, iy = -1, -1

shelves = {}
count = 1


# -----------------------------
# Mouse Callback
# -----------------------------
def draw_rectangle(event, x, y, flags, param):

    global drawing, ix, iy, frame, count

    if count > MAX_SHELVES:
        return

    if event == cv2.EVENT_LBUTTONDOWN:

        drawing = True
        ix, iy = x, y

    elif event == cv2.EVENT_LBUTTONUP:

        drawing = False

        x1 = min(ix, x)
        y1 = min(iy, y)
        x2 = max(ix, x)
        y2 = max(iy, y)

        # Draw rectangle
        cv2.rectangle(
            frame,
            (x1, y1),
            (x2, y2),
            (0, 255, 0),
            2
        )

        # Draw label
        cv2.putText(
            frame,
            f"Shelf {count}",
            (x1, y1 - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0,255,0),
            2
        )

        # Convert coordinates back to original image size
        shelves[f"Shelf_{count}"] = {

            "x1": int(x1 / scale),
            "y1": int(y1 / scale),
            "x2": int(x2 / scale),
            "y2": int(y2 / scale)

        }

        print(f"Shelf {count} Saved")

        count += 1


# -----------------------------
# Window
# -----------------------------
cv2.namedWindow("Shelf Zone Selection", cv2.WINDOW_NORMAL)

cv2.resizeWindow(
    "Shelf Zone Selection",
    display_width,
    display_height
)

cv2.setMouseCallback(
    "Shelf Zone Selection",
    draw_rectangle
)

# -----------------------------
# Main Loop
# -----------------------------
while True:

    temp = frame.copy()

    cv2.putText(
        temp,
        f"Draw Shelf {min(count, MAX_SHELVES)} of {MAX_SHELVES} | Press Q to Save",
        (20,40),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0,0,255),
        2
    )

    cv2.imshow(
        "Shelf Zone Selection",
        temp
    )

    key = cv2.waitKey(1)

    if key == ord("q"):
        break

    if count > MAX_SHELVES:
        print("\nAll Shelf Zones Drawn")
        break

cv2.destroyAllWindows()

# -----------------------------
# Save JSON
# -----------------------------
with open("shelf_zones.json", "w") as file:

    json.dump(
        shelves,
        file,
        indent=4
    )

print("\nShelf Zones Saved Successfully!")
print("Saved as shelf_zones.json")