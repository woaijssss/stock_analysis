
import os
import shutil
from pathlib import Path

def createPath(path:str):
    os.mkdir(path)

def deletePath(path:str):
    filePath = Path(path)
    if filePath.exists():
        shutil.rmtree(path)
    # print(del_list)
    # for f in del_list:
    #     file_path = os.path.join(path, f)
    #     if os.path.isfile(file_path):
    #         os.remove(file_path)
    #     elif os.path.isdir(file_path):
    #         shutil.rmtree(file_path)

if __name__ == '__main__':
    deletePath("../datas/指数数据")