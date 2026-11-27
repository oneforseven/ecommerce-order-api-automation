import allure
import pytest

from common.readyaml import get_testcase_yaml
from base.apiutil import BaseRequests
from base.generateId import m_id, c_id

@allure.feature(next(m_id) + "物料项目")
class TestLogistic:

    MATERIAL = "./testcase/logistic/getMaterial.yaml"

    @allure.story(next(c_id) + "获取物料信息")
    @pytest.mark.parametrize('base_info,testcase',get_testcase_yaml(MATERIAL))
    def test_get_material(self,base_info,testcase):
        allure.dynamic.title(testcase['case_name'])
        BaseRequests().specification_yaml(base_info, testcase)