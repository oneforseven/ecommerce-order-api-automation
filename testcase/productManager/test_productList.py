import pytest
import allure
from common.readyaml import get_testcase_yaml
from common.recordlog import logs
from common.readyaml import get_testcase_yaml
from base.apiutil import BaseRequests
from base.generateId import c_id,m_id

@allure.feature(next(m_id) + '商品管理')
class TestLogin:

    @allure.story(next(c_id) +'获取商品列表')
    @pytest.mark.run(order=1)
    @pytest.mark.parametrize("base_info,testcase",get_testcase_yaml("./testcase/productManager/getProductList.yaml"))
    def test_get_product_list(self,base_info,testcase):
        allure.dynamic.title(testcase['case_name'])
        BaseRequests().specification_yaml(base_info,testcase)

    @allure.story(next(c_id) +'获取商品详情信息')
    @pytest.mark.run(order=1)
    @pytest.mark.parametrize("base_info,testcase", get_testcase_yaml("./testcase/productManager/productDetail.yaml"))
    def test_get_product_detail(self, base_info,testcase):
        allure.dynamic.title(testcase['case_name'])
        BaseRequests().specification_yaml(base_info, testcase)




