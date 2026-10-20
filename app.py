import cv2
import numpy as np
import pandas as pd
import streamlit as st
from PIL import Image

from emotion import detect_emotions, draw_results
st.set_page_config(page_title="Emotion Detector", page_icon="🙂")
st.title("🙂 Emotion Detector")
st.write("Take a photo with your webcam or upload one. AI will find faces and detect emotion")

source = st.radio ("Input", ["Webcam", "Upload"], horizontal=True)

if source == "Webcam":
    file = st.camera_input("Take a photo")
else:
    file = st.file_uploader("Upload an image", type=[".jpg", ".jpeg",".png"])

if file is not None:
    image = Image.open(file).convert("RGB")
    image_bgr = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

    with st.spinner("Analyzing..."):
        results = detect_emotions(image_bgr)

    if not results:
        st.warning("No face found. Try better lighting or face the camera directly.")
    else:
         annotated = draw_results(image_bgr, results)
         st.image(cv2.cvtColor(annotated, cv2.COLOR_BGR2RGB), caption="Results")

         for i, face in enumerate(results, start=1):
             st.subheader(f"Face{i}: {face['dominant_emotion']. title()}")
             st.bar_chart(pd.Series(face["emotion"]))
st.caption("Limitation: results depend on lighting and camera angle, and a facialexpression dosen't always match what someone actully feels.")