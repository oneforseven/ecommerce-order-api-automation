import pytest
from common.recordlog import logs
from common.readyaml import ReadYamlData

read = ReadYamlData()

def clear_extract_data():
    pass

@pytest.fixture(scope='session',autouse=True)
def fixture_test():
    logs.info("-------------------接口测试开始-------------------")
    yield
    logs.info("-------------------接口测试结束-------------------")