## 提示
为保护个人隐私，网页不提供实时检测功能。如需使用实时检测功能，请按以下方式进行本地运行

## 安装
打开终端，输入
### 使用anconda3创建虚拟环境
```commandline
conda create -n yolo-streamlit python=3.8 -y

conda activate yolo-streamlit
```
### git到本地
```commandline
git clone https://github.com/sdfcxzc/classdesign.git
```
### 安装依赖
```commandline
pip install ultralytics

pip install streamlit
```
## 运行
```commandline
streamlit run app.py
```
## 打开摄像头功能
用记事本打开app.py文件，找到
```commandline
#elif source_selectbox == config.SOURCES_LIST[2]:
#    infer_uploaded_webcam(confidence, model)
```
将#删除，保存文件。然后用记事本打开config.py文件，找到
```commandline
SOURCES_LIST = ["图片", "视频"]
```
替换为
```commandline
SOURCES_LIST = ["图片", "视频", "摄像"]
```
保存文件，重新运行即可打开实时检测功能。

