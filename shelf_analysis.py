import os
import json
import csv
import cv2
import torch
import math
import subprocess
import imageio_ffmpeg
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
# CREATE OUTPUT FOLDERS
# ==========================================

os.makedirs(
    OUTPUT_FOLDER,
    exist_ok=True
)

os.makedirs(
    OUTPUT_VIDEO_FOLDER,
    exist_ok=True
)



# ==========================================
# LOAD SHELF ZONES
# ==========================================

with open(
    "shelf_zones.json",
    "r"
) as f:

    shelf_zones = json.load(f)




# ==========================================
# GLOBAL STORAGE
# ==========================================

video_fps = 30


visitor_ids = {}

frame_counter = {}


id_mapping = {}

next_customer_id = 1



MAX_MATCH_DISTANCE = 120



for shelf in shelf_zones:

    visitor_ids[shelf] = set()

    frame_counter[shelf] = {}





# ==========================================
# CUSTOMER ID STABILIZATION
# ==========================================

def get_customer_id(
        tracker_id,
        cx,
        cy
):

    global next_customer_id


    if tracker_id in id_mapping:

        id_mapping[tracker_id]["pos"]=(cx,cy)

        return id_mapping[tracker_id]["customer"]



    for old_id,data in id_mapping.items():

        px,py=data["pos"]


        distance = math.sqrt(
            (cx-px)**2 +
            (cy-py)**2
        )


        if distance < MAX_MATCH_DISTANCE:


            id_mapping[tracker_id]={

                "customer":
                data["customer"],

                "pos":
                (cx,cy)

            }


            return data["customer"]



    customer_id = next_customer_id


    id_mapping[tracker_id]={

        "customer":
        customer_id,

        "pos":
        (cx,cy)

    }


    next_customer_id += 1


    return customer_id





# ==========================================
# SHELF CHECK
# ==========================================

def point_inside_shelf(
        x,
        y,
        shelf
):

    return (

        shelf["x1"] <= x <= shelf["x2"]

        and

        shelf["y1"] <= y <= shelf["y2"]

    )





# ==========================================
# DRAW SHELVES
# ==========================================

def draw_shelves(frame):


    for name,shelf in shelf_zones.items():


        cv2.rectangle(

            frame,

            (
                shelf["x1"],
                shelf["y1"]
            ),

            (
                shelf["x2"],
                shelf["y2"]
            ),

            (255,0,0),

            3

        )


        cv2.putText(

            frame,

            name,

            (
                shelf["x1"],
                shelf["y1"]-10
            ),

            cv2.FONT_HERSHEY_SIMPLEX,

            1,

            (255,0,0),

            2

        )






# ==========================================
# VIDEO PROCESSING
# ==========================================

def analyze_video(video_path):


    global video_fps
    global id_mapping
    global next_customer_id



    # RESET

    id_mapping={}

    next_customer_id=1



    for shelf in shelf_zones:

        visitor_ids[shelf].clear()

        frame_counter[shelf].clear()




    cap=cv2.VideoCapture(video_path)



    if not cap.isOpened():

        raise Exception(
            "Video cannot open"
        )




    video_fps = cap.get(
        cv2.CAP_PROP_FPS
    )


    if video_fps<=0:

        video_fps=30




    width=int(
        cap.get(
            cv2.CAP_PROP_FRAME_WIDTH
        )
    )


    height=int(
        cap.get(
            cv2.CAP_PROP_FRAME_HEIGHT
        )
    )




    # ======================================
    # STREAMLIT COMPATIBLE VIDEO
    # ======================================


    temp_video=os.path.join(

    OUTPUT_VIDEO_FOLDER,

    "temp_"+os.path.basename(video_path)

)


    output_video=os.path.join(

        OUTPUT_VIDEO_FOLDER,

        "annotated_"+os.path.basename(video_path)

    )

    writer=cv2.VideoWriter(

    temp_video,

    cv2.VideoWriter_fourcc(
        *"mp4v"
    ),

    video_fps,

    (
        width,
        height
    )

)


    # CSV

    positions_csv=os.path.join(

        OUTPUT_FOLDER,

        "customer_positions.csv"

    )


    csv_file=open(

        positions_csv,

        "w",

        newline=""

    )


    csv_writer=csv.writer(csv_file)



    csv_writer.writerow(

        [

            "Frame",

            "Customer_ID",

            "Center_X",

            "Center_Y"

        ]

    )



    frame_number=0




    while True:


        success,frame=cap.read()



        if not success:

            break



        frame_number+=1




        draw_shelves(frame)




        results=model.track(

            frame,

            classes=[
                PERSON_CLASS_ID
            ],

            tracker="bytetrack.yaml",

            persist=True,

            conf=0.4,

            iou=0.5,

            verbose=False

        )




        if results[0].boxes is not None:



            for box in results[0].boxes:



                if box.id is None:

                    continue




                tracker_id=int(
                    box.id[0]
                )



                x1,y1,x2,y2=map(

                    int,

                    box.xyxy[0]

                )



                cx=(x1+x2)//2

                cy=y2




                customer_id=get_customer_id(

                    tracker_id,

                    cx,

                    cy

                )





                csv_writer.writerow(

                    [

                        frame_number,

                        customer_id,

                        cx,

                        cy

                    ]

                )





                cv2.rectangle(

                    frame,

                    (x1,y1),

                    (x2,y2),

                    (0,255,0),

                    2

                )




                cv2.putText(

                    frame,

                    f"Customer {customer_id}",

                    (x1,y1-10),

                    cv2.FONT_HERSHEY_SIMPLEX,

                    0.7,

                    (0,255,0),

                    2

                )





                cv2.circle(

                    frame,

                    (cx,cy),

                    5,

                    (0,0,255),

                    -1

                )





                for shelf_name,shelf in shelf_zones.items():



                    if point_inside_shelf(
                        cx,
                        cy,
                        shelf
                    ):


                        visitor_ids[shelf_name].add(
                            customer_id
                        )


                        if customer_id not in frame_counter[shelf_name]:

                            frame_counter[shelf_name][customer_id]=0



                        frame_counter[shelf_name][customer_id]+=1



                        cv2.putText(

                            frame,

                            shelf_name,

                            (x1,y2+25),

                            cv2.FONT_HERSHEY_SIMPLEX,

                            0.7,

                            (0,255,255),

                            2

                        )


                        break




        writer.write(frame)




    cap.release()

    writer.release()

    csv_file.close()



    # ==========================================
    # CONVERT TO STREAMLIT COMPATIBLE H264
    # ==========================================


    ffmpeg_path = imageio_ffmpeg.get_ffmpeg_exe()



    command = [

        ffmpeg_path,

        "-y",

        "-i",

        temp_video,

        "-vcodec",

        "libx264",

        "-pix_fmt",

        "yuv420p",

        output_video

    ]


    subprocess.run(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )



    if os.path.exists(temp_video):

        os.remove(temp_video)



    print(
        "H264 conversion completed"
    )



    print(
        "\nAnnotated Video Saved"
    )


    return (
        os.path.abspath(output_video),
        os.path.abspath(positions_csv)
    )






# ==========================================
# SAVE ANALYTICS
# ==========================================

def save_csv():


    path=os.path.join(

        OUTPUT_FOLDER,

        "analytics.csv"

    )


    with open(

        path,

        "w",

        newline=""

    ) as f:


        writer=csv.writer(f)



        writer.writerow(

            [

                "Shelf",

                "Visitors",

                "Total Dwell Time (sec)",

                "Average Dwell Time (sec)"

            ]

        )




        for shelf in shelf_zones:


            visitors=len(
                visitor_ids[shelf]
            )


            frames=sum(
                frame_counter[shelf].values()
            )


            total_time=frames/video_fps


            avg=(

                total_time/visitors

                if visitors>0

                else 0

            )



            writer.writerow(

                [

                    shelf,

                    visitors,

                    round(total_time,2),

                    round(avg,2)

                ]

            )


    print(
        "Analytics CSV Saved"
    )


    return path






# ==========================================
# STREAMLIT FUNCTION
# ==========================================

def process_uploaded_video(video_path):


    print(
        "\nProcessing Uploaded Video"
    )



    video,positions=analyze_video(
        video_path
    )



    analytics=save_csv()



    return {


        "video":video,


        "positions":positions,


        "analytics":os.path.abspath(
            analytics
        )


    }





# ==========================================
# DATASET MODE
# ==========================================

def process_dataset():


    video_path=os.path.join(

        DATASET_FOLDER,

        TEST_VIDEO

    )


    analyze_video(video_path)

    save_csv()



if __name__=="__main__":

    process_dataset()