# 🛒 RetailVision AI: Intelligent Retail Shelf Engagement Analytics & Business Recommendation Platform

> **"Beyond Analytics – AI That Tells Retailers What to Improve."**

---

# 📖 Project Overview

Retail stores generate enormous amounts of CCTV footage every day. However, most of this video data is never analyzed beyond security monitoring. Valuable insights about customer behavior, shopping patterns, and product engagement remain hidden.

Retail managers often need answers to questions such as:

- Which shelves attract the most customers?
- How long do customers spend near specific products?
- Which shelves receive little or no attention?
- Where should premium products or promotional displays be placed?

Traditionally, answering these questions requires manual observation, which is time-consuming, inconsistent, and often impractical.

**RetailVision AI** is an AI-powered retail analytics platform that transforms ordinary CCTV footage into actionable business intelligence using Computer Vision and Artificial Intelligence.

The system automatically performs:

- 👤 Customer Detection
- 🎯 Multi-Object Customer Tracking
- 🛍️ Shelf Interaction Detection
- 📊 Visitor Counting
- ⏱️ Dwell Time Analysis
- 🔥 Customer Movement Heatmap Generation
- 📈 Shelf Performance Analytics
- 🤖 AI-Powered Business Recommendations

Unlike traditional analytics systems that only display charts and statistics, **RetailVision AI** acts as a **Retail Decision-Support Platform**, helping retailers make informed business decisions to improve customer engagement and optimize product placement.

---

# ❗ Problem Statement

Although most retail stores are equipped with CCTV cameras, the recorded footage is primarily used for surveillance purposes and rarely utilized for business analytics.

Retailers face several challenges:

- Manual video monitoring is labor-intensive and inefficient.
- Customer behavior is difficult to analyze accurately.
- Shelf performance cannot be measured objectively.
- Product placement decisions are often based on assumptions rather than data.
- Low-engagement shelves remain unidentified, resulting in lost sales opportunities.

As a result, retailers lack the insights needed to improve store layout, optimize product placement, and enhance customer experience.

---

# 💡 Our Solution

RetailVision AI leverages **Computer Vision**, **Deep Learning**, and **Artificial Intelligence** to convert CCTV footage into meaningful retail analytics.

The system automatically:

- Detects customers using YOLO
- Tracks customers throughout the store using ByteTrack
- Detects customer interactions with predefined shelf regions
- Calculates visitor count and dwell time for each shelf
- Generates customer movement heatmaps
- Produces shelf-wise engagement analytics
- Provides AI-generated business recommendations for improving shelf performance

By combining real-time analytics with intelligent recommendations, RetailVision AI transforms raw surveillance footage into actionable business insights that support smarter retail decision-making.

---

# ✨ Key Features

- ✅ Customer Detection using YOLO
- ✅ Multi-Object Tracking using ByteTrack
- ✅ Shelf Region (ROI) Detection
- ✅ Shelf Interaction Detection
- ✅ Visitor Count Analytics
- ✅ Dwell Time Calculation
- ✅ Customer Movement Heatmap
- ✅ Interactive Streamlit Dashboard
- ✅ AI Business Recommendation Engine

---

# 🏗️ System Architecture

```
                 CCTV Video
                      │
                      ▼
             YOLO Person Detection
                      │
                      ▼
              ByteTrack Tracking
                      │
                      ▼
              Shelf ROI Detection
                      │
                      ▼
           Shelf Interaction Analysis
                      │
                      ▼
         Visitor & Dwell Time Analytics
                      │
                      ▼
             Heatmap Generation
                      │
                      ▼
        AI Business Recommendation Engine
                      │
                      ▼
          Interactive Streamlit Dashboard
```

---

# 💡 AI Business Recommendation Engine

Instead of displaying only analytics, the system automatically generates business insights.

### Example Recommendations

### Low Engagement

```
Insight:
No customer interaction detected.

Recommendation:
Change product placement or add promotional signage.
```

---

### High Traffic + Low Dwell

```
Insight:
Customers notice the shelf but leave quickly.

Recommendation:
Improve product arrangement, pricing visibility,
or promotional offers.
```

---

### High Dwell Time

```
Insight:
Customers spend more time at this shelf.

Recommendation:
Place premium products or high-value items here.
```

---

# 🛠 Technology Stack

| Component | Technology |
|------------|------------|
| Programming Language | Python |
| Object Detection | YOLO |
| Multi Object Tracking | ByteTrack |
| Computer Vision | OpenCV |
| Deep Learning | PyTorch |
| Analytics | Pandas |
| Heatmap | NumPy + OpenCV |
| Dashboard | Streamlit |

---

# 📂 Project Structure

```
RetailVisionAI/
│
├── app.py
├── config.py
├── shelf_analysis.py
├── recommendation.py
├── heatmap.py
├── dashboard.py
├── detect_people.py
├── track_people.py
├── shelf_zones.json
├── requirements.txt
├── README.md
│
├── dataset/
├── uploads/
├── uploaded_videos/
├── output/
├── input/
│
├── __pycache__/   (ignored)
├── venv/          (ignored)
│
└── yolov8n.pt
```

---

# 📊 Dashboard

The dashboard displays

- Total Visitors
- Shelf-wise Visitor Count
- Average Dwell Time
- Total Dwell Time
- Annotated Video
- Customer Heatmap
- Shelf Analytics
- AI Business Recommendations

---

# 📷 Demo Screenshots

## Dashboard

> <img width="1895" height="905" alt="image" src="https://github.com/user-attachments/assets/a00e7647-61c0-4964-ba70-93ad9f6c95f1" />
> <img width="1871" height="902" alt="image" src="https://github.com/user-attachments/assets/fc595ab4-7931-4a06-bea4-94896ade360f" />
> <img width="1891" height="897" alt="image" src="https://github.com/user-attachments/assets/d300ad6c-44db-4149-9a7e-bc3019172a8e" />

---

# 🎥 Demo Video

**Demo Video Link**

```
https://drive.google.com/file/d/1Fl-4zqX5qISAu81I3_Qqc075iJ-sr7Zb/view?usp=sharing
```

---

# 📁 Dataset

**Dataset Link**

```
https://drive.google.com/drive/folders/17GplNq6dB8SyFj1HUx3-IIg37PP7XKzv
```

---

# ⚙️ Installation

Clone the repository

```bash
git clone https://github.com/<your-username>/RetailVisionAI.git
```

Move into the project

```bash
cd RetailVisionAI
```

Create virtual environment

```bash
python -m venv venv
```

Activate environment

### Windows

```bash
venv\Scripts\activate
```

### Linux / Mac

```bash
source venv/bin/activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

### YOLOv8 Model

This project uses **YOLOv8 Nano (`yolov8n.pt`)** for real-time person detection.

> **Note:** You do **not** need to manually download the model. If `yolov8n.pt` is not available in the project folder, the **Ultralytics** package automatically downloads it the first time the application runs (provided you have an internet connection).

---

# ▶️ Run the Application

Launch the Streamlit application

```bash
streamlit run app.py
```

---

# 📈 Output

The system generates

- Annotated Video
- Analytics CSV
- Customer Position CSV
- Heatmap
- Dashboard
- AI Business Recommendations

---

# 🎯 Applications

- Retail Analytics
- Smart Supermarkets
- Shopping Mall Analytics
- Customer Behaviour Analysis
- Marketing Analytics
- Shelf Optimization
- Business Decision Support

---

# 🔮 Future Improvements

- Real-time CCTV Analytics
- Multi-camera Support
- Customer Journey Analytics
- Product Recommendation Engine
- Cloud Deployment
- Advanced AI Forecasting
- Retail KPI Prediction

---

# ⭐ Acknowledgements

- Ultralytics YOLO
- ByteTrack
- OpenCV
- Streamlit
- PyTorch
- Pandas
- NumPy

---

## ⭐ If you found this project useful, please consider giving it a Star!
