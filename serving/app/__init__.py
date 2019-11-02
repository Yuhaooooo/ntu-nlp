import sys
from pathlib import Path

BASE_PATH = Path(__file__).absolute().parent.parent
THIRD_DIR = BASE_PATH / 'third'

sys.path.insert(0, BASE_PATH)
sys.path.insert(0, THIRD_DIR)
