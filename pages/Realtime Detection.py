import streamlit as st
from ultralytics import YOLO
from PIL import Image
import cv2

model = YOLO("models/bestv8.pt")
model.conf = 0.25
model.iou = 0.45

st.title("Lemonade Object Detection 🍋🍋")

input_type = st.radio("Select input type", ["Image", "Video file"])

if input_type == "Image":
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption='Uploaded Image.', use_column_width=True)
        st.write("Detecting objects...")

        results = model(image)

        for result in results:
            boxes = result.boxes
            if boxes is not None:
                df = boxes.xyxy.cpu().numpy()
                #st.write("Detection Results:", df)

            annotated_image = result.plot()
            st.image(annotated_image, caption='Detected Image.', use_column_width=True)

else:
    uploaded_video = st.file_uploader("Choose a video file", type=["mp4", "avi", "mov"])

    if uploaded_video is not None:
        cap = cv2.VideoCapture(uploaded_video.name)

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            results = model(frame)
            annotated_frame = results[0].plot()
            st.image(annotated_frame)
