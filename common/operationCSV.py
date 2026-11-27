import csv
from conf.setting import DIR_PATH
import os
from common.recordlog import logs


def read_csv_data(file_name, encoding='utf-8-sig'):
    """读取 data 目录下 CSV，返回 [{列名: 值}, ...]"""
    path = os.path.join(DIR_PATH, 'data', file_name)
    try:
        with open(path, 'r', encoding=encoding, newline='') as f:
            rows = list(csv.DictReader(f))
        return [r for r in rows if any((v or '').strip() for v in r.values())]  # 过滤空行
    except Exception as e:
        logs.error(f'读取CSV失败 {path}: {e}')
        return []