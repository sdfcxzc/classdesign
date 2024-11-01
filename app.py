from pathlib import Path
from PIL import Image
import streamlit as st
import config
from utils import load_model, infer_uploaded_image, infer_uploaded_video, infer_uploaded_webcam

st.set_page_config(
    page_title="火灾检测系统",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
    )

st.title("火灾检测系统")

st.sidebar.header("模型配置")

task_type = st.sidebar.selectbox(
    "选择任务",
    ["检测"]
)

model_type = None
if task_type == "检测":
    model_type = st.sidebar.selectbox(
        "选择模型",
        config.DETECTION_MODEL_LIST
    )
else:
    st.error("Currently only 'Detection' function is implemented")

confidence = float(30) / 100

model_path = ""
if model_type:
    model_path = Path(config.DETECTION_MODEL_DIR, str(model_type))
else:
    st.error("Please Select Model in Sidebar")

try:
    model = load_model(model_path)
except Exception as e:
    st.error(f"Unable to load model. Please check the specified path: {model_path}")

st.sidebar.header("图片/视频-配置")
source_selectbox = st.sidebar.selectbox(
    "选择文件类型",
    config.SOURCES_LIST
)

source_img = None
if source_selectbox == config.SOURCES_LIST[0]:
    infer_uploaded_image(confidence, model)
elif source_selectbox == config.SOURCES_LIST[1]:
    infer_uploaded_video(confidence, model)
elif source_selectbox == config.SOURCES_LIST[2]:
    infer_uploaded_webcam(confidence, model)
else:
    st.error("Currently only 'Image' and 'Video' source are implemented")