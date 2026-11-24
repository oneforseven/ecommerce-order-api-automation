import os.path
import allure
import jsonpath

from common.recordlog import logs

class Assertions:
    """
    接口断言模式封装，支持
    1.字符串包含
    2.结果不相等断言
    3.结果不相等断言
    4.断言接口返回值里面的任意一个数
    5.数据库断言
    """

    def contains_assert(self,value,response,status_code):
        """
        第一种模式，字符串包含断言，断言预期结果的字符串是否包含在接口实际返回结果当中
        :param value: 预期结果，yaml文件validation关键字下的结果
        :param response: 实际结果
        :param status_code:
        :return:
        """
        # 断言状态标识，0->成功，其他代表失败
        flag = 0
        for assert_key,assert_value in value.items():
            print(assert_key,assert_value)
            if assert_key == 'status_code':
                if assert_value != status_code:
                    flag+=1
                    logs.error("contains断言失败，返回码【%s】不等于【%s】" %(status_code,assert_value))
                    allure.attach(f'预期结果：{assert_value}\n实际结果：{status_code}','响应代码断言结果：失败',
                                  allure.attachment_type.TEXT)
            else:
                resp_list = jsonpath.jsonpath(response,"$..%s" %assert_key)
                if isinstance(resp_list[0],str):
                    resp_list = ''.join(resp_list)
                if resp_list:
                    if assert_value in resp_list:
                        logs.info("字符串包含断言成功，【%s】,实际结果：【%s】" %(assert_value, resp_list))
                    else:
                        flag = flag + 1
                        logs.error("响应文本断言失败,预期结果：【%s】,实际结果：【%s】" %(assert_value, resp_list))
                        allure.attach(f'预期结果：{assert_value}\n实际结果：{resp_list}', '响应文本断言结果：失败',
                                      allure.attachment_type.TEXT)

        return flag


    def equal_assert(self):
        """相等模式"""

    def not_equal_assert(self):
        """不相等断言"""

    def assert_result(self,expected,response,status_code):
        """
        断言模式：通过all_flag标记
        :param expected: 预期结果
        :param response: 实际返回结果，需要json格式
        :param status_code: 实际返回状态码
        :return:
        """
        all_flag = 0
        # 断言状态标识，0->成功，其他代表失败
        try:
            for yq in expected:
                for key,value in yq.items():
                    if key == 'contains':
                        flag = self.contains_assert(value,response,status_code)
                        all_flag = all_flag + flag
                    elif key == 'eq':
                        self.equal_assert()

            assert all_flag == 0
            logs.info("测试成功！")
        except AssertionError:
            logs.error("测试失败！")
            raise
        except Exception as e:
            logs.error(f"异常信息：{e}")
            raise



