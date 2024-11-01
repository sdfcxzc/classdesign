from pathlib import Path
import sys

file_path = Path(__file__).resolve()

root_path = file_path.parent

if root_path not in sys.path:
    sys.path.append(str(root_path))

ROOT = root_path.relative_to(Path.cwd())

SOURCES_LIST = ["图片", "视频", "摄像"]

DETECTION_MODEL_DIR = ROOT / 'weights' / 'detection'
YOLOv5s_best = DETECTION_MODEL_DIR / "best.pt"

DETECTION_MODEL_LIST = [
    "best.pt"]
