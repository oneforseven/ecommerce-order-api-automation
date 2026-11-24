import os
import sys
import logging

# 取到根目录
DIR_PATH = os.path.dirname(os.path.dirname(__file__))
# 放进环境变量
sys.path.append(DIR_PATH)

# log 日志的级别输出
LOG_LEVEL = logging.DEBUG   # 日志输出到文件的级别
STREAM_LOG_LEVEL = logging.DEBUG  # 输出日志到控制台

# 文件路径
FILE_PATH = {
    'extract': os.path.join(DIR_PATH,'extract.yaml'),
    'conf': os.path.join(DIR_PATH,'conf','config.ini'),
    'LOG':os.path.join(DIR_PATH,'log')
}

