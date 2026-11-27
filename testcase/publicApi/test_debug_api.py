import allure
import pytest

from common.readyaml import get_testcase_yaml
from base.apiutil import BaseRequests
from base.generateId import m_id, c_id


@allure.feature(next(m_id) + '用户管理模块（单接口）')
class TestUserManager:

    ADD_USER = "./testcase/publicApi/addUser.yaml"
    UPDATE_USER = "./testcase/publicApi/updateUser.yaml"
    DELETE_USER = "./testcase/publicApi/deleteUser.yaml"
    QUERY_USER = "./testcase/publicApi/queryUser.yaml"

    # 场景，allure报告的目录结构
    @allure.story(next(c_id) + "新增用户")
    # 测试用例执行顺序设置
    @pytest.mark.run(order=1)
    # 参数化，yaml数据驱动
    @pytest.mark.parametrize('base_info,testcase', get_testcase_yaml(ADD_USER))
    def test_add_user(self,base_info,testcase):
        allure.dynamic.title(testcase['case_name'])
        BaseRequests().specification_yaml(base_info, testcase)

    @allure.story(next(c_id) + "修改用户")
    @pytest.mark.run(order=2)
    @pytest.mark.parametrize('base_info,testcase', get_testcase_yaml(UPDATE_USER))
    def test_update_user(self,base_info,testcase):
        allure.dynamic.title(testcase['case_name'])
        BaseRequests().specification_yaml(base_info, testcase)

    @allure.story(next(c_id) + "查询用户")
    @pytest.mark.run(order=4)
    @pytest.mark.parametrize('base_info,testcase', get_testcase_yaml(QUERY_USER))
    def test_query_user(self,base_info,testcase):
        allure.dynamic.title(testcase['case_name'])
        BaseRequests().specification_yaml(base_info, testcase)

    @allure.story(next(c_id) + "删除用户")
    @pytest.mark.run(order=3)
    @pytest.mark.parametrize('base_info,testcase', get_testcase_yaml(DELETE_USER))
    def test_delete_user(self,base_info,testcase):
        allure.dynamic.title(testcase['case_name'])
        BaseRequests().specification_yaml(base_info, testcase)

