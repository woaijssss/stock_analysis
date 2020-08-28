
from stock_analysis.src.StockService import StockService
import os
from pathlib import Path

if __name__ == '__main__':
    dataPath = Path("../datas")
    if not dataPath.is_dir():   # datas目录不存在，则创建（因git不上传数据文件，因此git clone之后没有datas目录）
        # StockService().startService()
        dataPath.mkdir()