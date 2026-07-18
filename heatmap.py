import os
import cv2
import pandas as pd
import numpy as np


# ==========================================
# GENERATE HEATMAP FUNCTION
# ==========================================

def generate_heatmap(video_file, csv_file, output_folder="output"):

    os.makedirs(
        output_folder,
        exist_ok=True
    )


    OUTPUT_IMAGE = os.path.join(
        output_folder,
        "heatmap.png"
    )


    # ==========================================
    # LOAD FIRST VIDEO FRAME
    # ==========================================

    cap = cv2.VideoCapture(video_file)

    success, frame = cap.read()


    if not success:

        print("Cannot open video.")

        return None


    height, width = frame.shape[:2]

    cap.release()



    # ==========================================
    # CREATE EMPTY HEATMAP
    # ==========================================

    heatmap = np.zeros(
        (height,width),
        dtype=np.float32
    )


    # ==========================================
    # LOAD CUSTOMER POSITIONS
    # ==========================================

    data = pd.read_csv(csv_file)


    print(
        f"\nCustomer Positions : {len(data)}"
    )


    # ==========================================
    # DRAW CUSTOMER MOVEMENT
    # ==========================================

    for _, row in data.iterrows():


        x = int(row["Center_X"])

        y = int(row["Center_Y"])


        if (
            0 <= x < width
            and
            0 <= y < height
        ):


            cv2.circle(

                heatmap,

                (x,y),

                40,

                1,

                -1

            )



    # ==========================================
    # SMOOTH HEAT
    # ==========================================

    heatmap = cv2.GaussianBlur(

        heatmap,

        (0,0),

        sigmaX=60,

        sigmaY=60

    )


    heatmap = cv2.normalize(

        heatmap,

        None,

        0,

        255,

        cv2.NORM_MINMAX

    )


    heatmap = heatmap.astype(
        np.uint8
    )



    # ==========================================
    # APPLY COLOR MAP
    # ==========================================

    heatmap_color = cv2.applyColorMap(

        heatmap,

        cv2.COLORMAP_JET

    )



    # ==========================================
    # OVERLAY WITH VIDEO FRAME
    # ==========================================

    overlay = cv2.addWeighted(

        frame,

        0.55,

        heatmap_color,

        0.45,

        0

    )



    # ==========================================
    # TITLE
    # ==========================================


    cv2.putText(

        overlay,

        "AI-Powered Retail Shelf Engagement Analytics",

        (40,50),

        cv2.FONT_HERSHEY_SIMPLEX,

        1.1,

        (255,255,255),

        3

    )


    cv2.putText(

        overlay,

        "Customer Movement Heatmap",

        (40,90),

        cv2.FONT_HERSHEY_SIMPLEX,

        0.9,

        (0,255,255),

        2

    )



    # ==========================================
    # LEGEND BOX
    # ==========================================


    cv2.rectangle(

        overlay,

        (20,120),

        (260,300),

        (40,40,40),

        -1

    )


    cv2.rectangle(

        overlay,

        (20,120),

        (260,300),

        (255,255,255),

        2

    )


    cv2.putText(

        overlay,

        "Heatmap Legend",

        (35,145),

        cv2.FONT_HERSHEY_SIMPLEX,

        0.7,

        (255,255,255),

        2

    )


    legend = [

        ("Low Activity",(255,0,0)),

        ("Medium Activity",(0,255,0)),

        ("High Activity",(0,255,255)),

        ("Very High",(0,0,255))

    ]


    y_position = 180


    for text,color in legend:


        cv2.circle(

            overlay,

            (45,y_position-5),

            10,

            color,

            -1

        )


        cv2.putText(

            overlay,

            text,

            (70,y_position),

            cv2.FONT_HERSHEY_SIMPLEX,

            0.55,

            (255,255,255),

            2

        )


        y_position += 35



    # ==========================================
    # SAVE IMAGE
    # ==========================================


    cv2.imwrite(

        OUTPUT_IMAGE,

        overlay

    )


    print(
        "\nHeatmap Saved Successfully!"
    )


    # Return path for Streamlit

    return OUTPUT_IMAGE



# ==========================================
# TEST MODE
# ==========================================

if __name__=="__main__":

    from config import *


    csv_path=os.path.join(

        OUTPUT_FOLDER,

        "customer_positions.csv"

    )


    video_path=os.path.join(

        DATASET_FOLDER,

        TEST_VIDEO

    )


    generate_heatmap(

        video_path,

        csv_path,

        OUTPUT_FOLDER

    )