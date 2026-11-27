import pytest
import allure
from common.readyaml import get_testcase_yaml
from common.recordlog import logs
from common.readyaml import get_testcase_yaml
from base.apiutil import BaseRequests
from base.generateId import m_id, c_id

@allure.feature((next(m_id)) + '登录接口')
class TestLogin:

    @allure.story((next(c_id)) +'用户名和密码登录正常校验')
    @pytest.mark.run(order=0)
    @pytest.mark.parametrize("base_info,testcase",get_testcase_yaml("./testcase/Login/login.yaml"))
    def test_case01(self,base_info,testcase):
        allure.dynamic.title(testcase['case_name'])
        BaseRequests().specification_yaml(base_info, testcase)




