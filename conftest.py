import os

import pytest

from common.recordlog import logs
from common.readyaml import ReadYamlData
from conf.setting import FILE_PATH

read = ReadYamlData()

def clear_extract_data():
    """清空 extract.yaml，避免上一次运行残留的 token/user_id 污染本次用例"""
    extract_file = FILE_PATH['extract']
    if os.path.exists(extract_file):
        with open(extract_file, 'w', encoding='utf-8'):
            pass

@pytest.fixture(scope='session',autouse=True)
def fixture_test():
    clear_extract_data()
    logs.info("-------------------接口测试开始-------------------")
    yield
    logs.info("-------------------接口测试结束-------------------")