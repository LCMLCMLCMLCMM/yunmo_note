import os
import sys
from pathlib import *

current_file = Path(__file__)
current_dir = current_file.parent.resolve()

parent_dir = current_dir.parent.resolve()

python_dir = parent_dir / "python"
src_dir = parent_dir / "src"

os.system(f"{python_dir}\\python313\\pythonw.exe {src_dir}\\main.py")