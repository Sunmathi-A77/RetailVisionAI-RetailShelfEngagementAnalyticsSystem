import streamlit as st
import os
import pandas as pd
import cv2
import time

from shelf_analysis import process_uploaded_video
import recommendation


# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(
    page_title="RetailVision AI",
    page_icon="🛒",
    layout="wide"
)


# ==========================================
# TITLE
# ==========================================

st.title(
    "🛒 RetailVision AI"
)

st.subheader(
    "Intelligent Retail Shelf Engagement Analytics & Recommendation System"
)


st.write(
"""
AI-powered system that detects customers,
tracks movement, measures shelf engagement,
generates heatmaps and provides business recommendations.
"""
)



# ==========================================
# PATHS
# ==========================================

OUTPUT_FOLDER="output"

VIDEO_FOLDER="output_videos"

HEATMAP_PATH="output/heatmap.png"

RECOMMENDATION_FILE="output/recommendations.csv"



# ==========================================
# UPLOAD VIDEO
# ==========================================

uploaded_file = st.file_uploader(

    "Upload Retail Store Video",

    type=[
        "mp4",
        "avi",
        "mov"
    ]

)



if uploaded_file:



    input_video=os.path.join(

        "uploads",

        uploaded_file.name

    )


    os.makedirs(
        "uploads",
        exist_ok=True
    )


    with open(
        input_video,
        "wb"
    ) as f:

        f.write(
            uploaded_file.read()
        )



    st.success(
        "Video Uploaded Successfully"
    )



    # ======================================
    # PROCESS BUTTON
    # ======================================


    if st.button(
        "🚀 Analyze Video"
    ):


        with st.spinner(
            "Running YOLO Detection and Analytics..."
        ):


            result = process_uploaded_video(
                input_video
            )


            time.sleep(1)



        st.success(
            "Video Processing Completed!"
        )



        # ==================================
        # SAVE SESSION RESULTS
        # ==================================

        st.session_state["video"]=result["video"]

        st.session_state["analytics"]=result["analytics"]



        # ==================================
        # RUN HEATMAP
        # ==================================

        os.system(
            "python heatmap.py"
        )



        # ==================================
        # RUN RECOMMENDATION
        # ==================================

        os.system(
            "python recommendation.py"
        )




# ==========================================
# DISPLAY RESULTS
# ==========================================


if "video" in st.session_state:



    st.divider()


    st.header(
        "🎥 Annotated Video"
    )


    video_file = st.session_state["video"]


    if os.path.exists(video_file):


        with open(video_file,"rb") as f:

            video_bytes=f.read()


        st.video(
            video_bytes,
            format="video/mp4"
        )


    else:

        st.error(
            "Annotated video not found"
        )




    st.divider()


    st.header(
        "📊 Shelf Analytics"
    )



    analytics_file = st.session_state["analytics"]



    if os.path.exists(
        analytics_file
    ):


        df=pd.read_csv(
            analytics_file
        )


        st.dataframe(
            df,
            use_container_width=True
        )



        col1,col2,col3,col4=st.columns(4)



        total_visitors=df["Visitors"].sum()


        avg_dwell=df[
            "Average Dwell Time (sec)"
        ].mean()



        max_shelf=df.loc[
            df["Visitors"].idxmax(),
            "Shelf"
        ]



        best_dwell=df.loc[
            df[
            "Total Dwell Time (sec)"
            ].idxmax(),
            "Shelf"
        ]



        col1.metric(
            "Total Visitors",
            int(total_visitors)
        )


        col2.metric(
            "Average Dwell",
            round(avg_dwell,2)
        )


        col3.metric(
            "Most Visited Shelf",
            max_shelf
        )


        col4.metric(
            "Highest Engagement",
            best_dwell
        )





    st.divider()



    # ======================================
    # HEATMAP
    # ======================================


    st.header(
        "🔥 Customer Movement Heatmap"
    )


    if os.path.exists(
        HEATMAP_PATH
    ):


        st.image(
            HEATMAP_PATH,
            use_container_width=True
        )


    else:

        st.warning(
            "Heatmap not generated"
        )




    st.divider()



    # ======================================
    # RECOMMENDATION
    # ======================================


    st.header(
        "🤖 AI Business Recommendation Engine"
    )



    if os.path.exists(
        RECOMMENDATION_FILE
    ):


        rec=pd.read_csv(
            RECOMMENDATION_FILE
        )



        for _,row in rec.iterrows():


            with st.container():


                st.subheader(
                    row["Shelf"]
                )


                st.write(
                    "**Insight:**",
                    row["Insight"]
                )


                st.info(
                    row["Recommendation"]
                )


                st.divider()



    else:


        st.warning(
            "Recommendation file not available"
        )



# ==========================================
# FOOTER
# ==========================================

st.sidebar.title(
    "RetailVision AI"
)


st.sidebar.write(
"""
Pipeline:

YOLOv11
↓
ByteTrack Tracking
↓
Shelf Interaction Detection
↓
Dwell Time Analytics
↓
Heatmap
↓
AI Recommendation Engine
"""
)