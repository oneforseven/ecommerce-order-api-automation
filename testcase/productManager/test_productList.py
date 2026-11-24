import pytest
import allure
from common.readyaml import get_testcase_yaml
from common.recordlog import logs
from common.readyaml import get_testcase_yaml
from base.apiutil import BaseRequests

@allure.feature('商品管理')
class TestLogin:

    @allure.story('获取商品列表')
    @pytest.mark.parametrize("params",get_testcase_yaml("./testcase/productManager/getProductList.yaml"))
    def test_get_product_list(self,params):
        BaseRequests().specification_yaml(params)

    @allure.story('获取商品详情信息')
    @pytest.mark.parametrize("params", get_testcase_yaml("./testcase/productManager/productDetail.yaml"))
    def test_get_product_detail(self, params):
        BaseRequests().specification_yaml(params)




