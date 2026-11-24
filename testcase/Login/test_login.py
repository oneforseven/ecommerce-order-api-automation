import pytest
import allure
from common.readyaml import get_testcase_yaml
from common.recordlog import logs
from common.readyaml import get_testcase_yaml
from base.apiutil import BaseRequests

@allure.feature('登录接口')
class TestLogin:

    @allure.story('用户名和密码登录正常校验')
    @pytest.mark.parametrize("params",get_testcase_yaml("./testcase/Login/login.yaml"))
    def test_case01(self,params):
        BaseRequests().specification_yaml(params)




