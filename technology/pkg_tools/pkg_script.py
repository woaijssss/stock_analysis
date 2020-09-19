import os
import shutil
from pathlib import Path

exePath = Path("exe")
configPath = Path("exe/conf")
os.chdir("..")
try:
    shutil.rmtree(exePath)
except Exception as e:
    pass
os.system("pyinstaller -F bin/main.py")
if not exePath.is_dir():  # exe目录不存在，则创建
    exePath.mkdir()

shutil.move("build", "exe/")
shutil.move("dist", "exe/")
shutil.move("main.spec", "exe/")
shutil.copytree("conf", configPath)
