from ultralytics import YOLO
import streamlit as st
import cv2
from PIL import Image
import tempfile
import torch


mp3_file='123.mp3'

html="""
<script>
  alert("请注意！疑似检测到火情");
</script>
"""


def _display_detected_frames(conf, model, st_frame, image,count):
    image = cv2.resize(image, (720, int(720 * (9 / 16))))
    res = model.predict(image, conf=conf)
    if count < 5:
        for result in res:
            for box in result.boxes:
                label = f'{model.names[int(box.cls)]}'
                if label == 'fire' or label == 'smoke':
                    return label
                    break
    res_plotted = res[0].plot()
    st_frame.image(res_plotted,
                   caption='检测图像',
                   channels="BGR",
                   use_column_width=True
                   )


@st.cache_resource
def load_model(model_path):
    model = YOLO(model_path)
    return model


def infer_uploaded_image(conf, model):
    source_img = st.sidebar.file_uploader(
        label="选择图片...",
        type=("jpg", "jpeg", "png", 'bmp', 'webp')
    )

    model.names[1]='人'
    model.names[2]='烟雾'
    col1, col2 = st.columns(2)
    with col1:
        if source_img:
            uploaded_image = Image.open(source_img)
            st.image(
                image=source_img,
                caption="原图像",
                use_column_width=True
            )

    if source_img:
        if st.button("开始检测"):
            with st.spinner("检测..."):
                res = model.predict(uploaded_image,
                                    conf=conf)
                boxes = res[0].boxes
                res_plotted = res[0].plot()[:, :, ::-1]
                label = f'{model.names[int(boxes.cls)]}'
                with col2:
                    st.image(res_plotted,
                             caption="检测图像",
                             use_column_width=True)
                    try:
                        with st.expander("检测到像素坐标"):
                            for box in boxes:
                                st.write(box.xywh)
                    except Exception as ex:
                        st.write("No image is uploaded yet!")
                        st.write(ex)
                if label == 'smoke' or label == 'fire':
                    st.components.v1.html(html)
                    st.audio(mp3_file, autoplay=True)

def infer_uploaded_video(conf, model):
    count=0
    source_video = st.sidebar.file_uploader(
        label="选择视频..."
    )
    if source_video:
        st.video(source_video)
    if source_video:
        if st.button("开始检测"):
            with st.spinner("检测..."):
                try:
                    tfile = tempfile.NamedTemporaryFile()
                    tfile.write(source_video.read())
                    vid_cap = cv2.VideoCapture(
                        tfile.name)
                    st_frame = st.empty()
                    while (vid_cap.isOpened()):
                        success, image = vid_cap.read()
                        if success:
                            label = _display_detected_frames(conf,
                                                     model,
                                                     st_frame,
                                                     image,
                                                    count
                                                     )
                            if label == 'smoke' or label == 'fire':
                                count += 1
                                if count == 5:
                                    st.components.v1.html(html)
                                    st.audio(mp3_file, autoplay=True)
                        else:
                            vid_cap.release()
                            break
                except Exception as e:
                    st.error(f"Error loading video: {e}")


def infer_uploaded_webcam(conf, model):
    try:
        flag = st.button(
            label="停止运行"
        )
        vid_cap = cv2.VideoCapture(0)
        st_frame = st.empty()
        count=0
        while not flag:
            success, image = vid_cap.read()
            if success:
                label = _display_detected_frames(
                    conf,
                    model,
                    st_frame,
                    image,
                    count
                )
                if label == 'smoke' or label == 'fire':
                    count += 1
                    if count == 5:
                        st.components.v1.html(html)
                        st.audio(mp3_file, autoplay=True)
            else:
                vid_cap.release()
                break
    except Exception as e:
        st.error(f"Error loading video: {str(e)}")
