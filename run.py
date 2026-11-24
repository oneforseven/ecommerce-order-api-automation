import os
import shutil
import pytest

if __name__ == '__main__':
    pytest.main()
    # 将系统环境报告手动复制到temp文件夹下
    shutil.copy('./environment.xml','./report/temp')
    os.system(f"allure serve ./report/temp")