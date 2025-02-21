# -*- coding: utf-8 -*-

import concurrent.futures
import os,sys,platform
import psutil

sys.path[0] = os.path.dirname(os.path.abspath(__file__))
from utilTools.getConfig import CommonConfig
from common.dataHandle import findFilesList

def executableFiles(file):
    os.system(file) if platform.system() == "Windows" else os.system("python3 " + file)

def getProcessMaxWorkers():
    # 获取逻辑CPU核心数
    logical_cores = psutil.cpu_count()
    CommonConfig.set_cf("setting","threadMaxWorkers", str(logical_cores - 1))


if __name__ == '__main__':
    getProcessMaxWorkers()
    processMaxWorkers = int(CommonConfig.get_cf("config", "setting", "processMaxWorkers"))
    # 找出/prepare路径下所有.py的文件
    pyFiles = findFilesList('/prepare', '.py')

    fileCount = len(pyFiles)
    if processMaxWorkers > fileCount: processMaxWorkers = fileCount

    with concurrent.futures.ProcessPoolExecutor(max_workers=processMaxWorkers) as executor:
        executor.map(executableFiles, pyFiles)