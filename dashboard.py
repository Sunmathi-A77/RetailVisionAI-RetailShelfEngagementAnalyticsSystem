import streamlit as st
import os
import subprocess
import pandas as pd
import json
import cv2


# ==============================
# CONFIG
# ==============================

UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "output"
VIDEO_FOLDER = "output/annotated_videos"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


st.set_page_config(
    page_title="RetailVision AI",
    layout="wide"
)


st.title("🏪 RetailVision AI")
st.subheader(
    "Intelligent Retail Shelf Engagement & Business Recommendation System"
)


# ==============================
# VIDEO UPLOAD
# ==============================

uploaded_video = st.file_uploader(
    "Upload Retail CCTV Video",
    type=["mp4","avi","mov"]
)


if uploaded_video:


    input_path = os.path.join(
        UPLOAD_FOLDER,
        uploaded_video.name
    )


    with open(input_path,"wb") as f:
        f.write(uploaded_video.read())


    st.success(
        "Video Uploaded Successfully"
    )


    if st.button("🚀 Analyze Video"):


        with st.spinner(
            "AI is analyzing customer behaviour..."
        ):


            # -------------------------
            # Run YOLO Analysis
            # -------------------------

            command = [
                "python",
                "shelf_analysis.py",
                input_path
            ]

            subprocess.run(command)


            # -------------------------
            # Run Recommendation Engine
            # -------------------------

            subprocess.run(
                [
                    "python",
                    "recommendation.py"
                ]
            )


        st.success(
            "Analysis Completed!"
        )



        # ==========================
        # DISPLAY ANALYTICS
        # ==========================


        st.header(
            "📊 Shelf Analytics"
        )


        csv_path = (
            "output/analytics.csv"
        )


        if os.path.exists(csv_path):

            df = pd.read_csv(csv_path)


            col1,col2,col3 = st.columns(3)


            with col1:

                st.metric(
                    "Total Visitors",
                    df["Visitors"].sum()
                )


            with col2:

                st.metric(
                    "Most Visited Shelf",
                    df.loc[
                    df["Visitors"].idxmax(),
                    "Shelf"
                    ]
                )


            with col3:

                st.metric(
                    "Highest Dwell",
                    df.loc[
                    df["Total Dwell Time (sec)"].idxmax(),
                    "Shelf"
                    ]
                )


            st.dataframe(df)



            # charts

            st.bar_chart(
                df.set_index("Shelf")
                [
                "Visitors"
                ]
            )


            st.bar_chart(
                df.set_index("Shelf")
                [
                "Total Dwell Time (sec)"
                ]
            )



        # ==========================
        # ANNOTATED VIDEO
        # ==========================


        st.header(
            "🎥 Annotated Video"
        )


        annotated_path = os.path.join(
            VIDEO_FOLDER,
            uploaded_video.name
        )


        if os.path.exists(annotated_path):

            st.video(
                annotated_path
            )

        else:

            st.warning(
                "Annotated video not found"
            )



        # ==========================
        # RECOMMENDATION
        # ==========================


        st.header(
            "🤖 AI Business Recommendation"
        )


        recommendation_file = (
            "output/recommendations.txt"
        )


        if os.path.exists(
            recommendation_file
        ):


            with open(
                recommendation_file,
                "r"
            ) as f:

                recommendation = f.read()


            st.info(
                recommendation
            )

        else:

            st.warning(
                "Recommendation not generated"
            )