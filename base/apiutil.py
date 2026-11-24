import json
import allure
import jsonpath

from common.readyaml import ReadYamlData,get_testcase_yaml
from common.debugtalk import DebugTalk
from common.recordlog import logs
from conf.operateCoinfig import OperateConfig
from common.sendrequest import SendRequest
from common.assertions import Assertions

assert_res = Assertions()

class BaseRequests:

    def __init__(self):
        self.read = ReadYamlData()
        self.conf = OperateConfig()
        self.send = SendRequest()

    def replace_load(self,data):
        """yaml文件替换解析${}"""

        str_data = data
        if not isinstance(data,str):
            str_data = json.dumps(data,ensure_ascii=False)
        for i in range(str_data.count("${")):

            if "${" in str_data and "}" in str_data:
                # index 检测字符串，找到字符串索引位置
                start_index = str_data.index("$")
                end_index = str_data.index("}",start_index)
                ref_all_params = str_data[start_index:end_index + 1]
                # 取出函数名
                func_name = ref_all_params[2:ref_all_params.index("(")]
                # 取出函数里面的参数值
                func_params = ref_all_params[ref_all_params.index("(") + 1:ref_all_params.index(")")]
                # 传入替换的参数获取对应的值
                extract_data = getattr(DebugTalk(),func_name)(*func_params.split(",") if func_params else "")
                if extract_data and isinstance(extract_data,list):
                    extract_data = ','.join(e for e in extract_data)

                # 数据替换
                str_data = str_data.replace(ref_all_params,str(extract_data))

        # 还原数据
        if data and isinstance(data,dict):
             data = json.loads(str_data)
        else:
            data = str_data

        return data


    def specification_yaml(self,case_info):
        """
        规范yaml接口测试数据的写法
        :param case_info: list类型，调取case_info[0]
        :return:
        """
        cookie=None
        params_type = ['params','data','json']
        try:
            base_url = self.conf.get_envi('host')
            url = base_url + case_info['baseInfo']['url']
            allure.attach(url,f'接口地址：{url}')
            api_name = case_info['baseInfo']['api_name']
            allure.attach(api_name, f'接口名称：{api_name}')
            method = case_info['baseInfo']['method']
            allure.attach(method, f'请求方法：{method}')
            header = case_info['baseInfo']['header']
            allure.attach(str(header), f'请求头：{header}',allure.attachment_type.TEXT)

            try:
                cookie = self.replace_load(case_info =['baseInfo']['cookies'])
                allure.attach(cookie, f'cookie：{header}', allure.attachment_type.TEXT)
            except:
                pass

            for tc in case_info['testCase']:
                case_name = tc.pop('case_name')
                allure.attach(case_name, f'测试用例名称：{case_name}')
                validation = tc.pop('validation', None)
                extract = tc.pop('extract', None)
                extract_list = tc.pop('extract_list', None)
                for key,value in tc.items():
                    if key in params_type:
                        tc[key] = self.replace_load(value)

                res = self.send.run_main(name=api_name, url=url, case_name=case_name,
                                         header=header, method=method, cookies=cookie, **tc)
                res_text = res.text
                try:
                    attach_text = json.dumps(res.json(),indent=4,ensure_ascii=False)
                except Exception:
                    attach_text = res.text

                allure.attach(attach_text, f'接口的响应信息：{url}',allure.attachment_type.TEXT)
                allure.attach(str(res.status_code),f"接口的状态码：{res.status_code}",allure.attachment_type.TEXT)

                if extract is not None:
                    self.extract_data(extract,res_text)
                if extract_list is not None:
                    self.extract_data_list(extract_list,res_text)

                # 处理接口断言
                res_json = res.json()    # assert_result的response要json格式
                assert_res.assert_result(validation,res_json,res.status_code)

        except Exception as e:
            logs.error(e)
            raise e

    def extract_data(self,testcase_extract,response):
        """
        提取接口的返回值，支持正则表达式提取以及json提取器
        :param testcase_extract: yaml文件中的extract的值
        :param response: 接口的实际返回值
        :return:
        """
        try:
            for key,value in testcase_extract.items():
                # json提取器
                if "$" in value:
                    ext_json = jsonpath.jsonpath(json.loads(response),value)[0]
                    if ext_json:
                        extract_data = {key:ext_json}
                    else:
                        extract_data = {key: '未提取到数据，该接口返回值为空或者json提取表达式有误'}
                    logs.info(f'json提取到的参数：{extract_data}')
                    self.read.write_yaml_data(extract_data)
        except:
            logs.error('接口返回值提取异常，请检查yaml文件的extract表达式是否正确')


    def extract_data_list(self, testcase_extract_list, response):
        """
        提取多个参数，支持正则表达式和json提取，提取结果以列表形式返回
        :param testcase_extract_list: yaml文件中的extract_list信息
        :param response: 接口的实际返回值,str类型
        :return:
        """
        try:
            for key, value in testcase_extract_list.items():
                if "$" in value:
                    # 增加提取判断，有些返回结果为空提取不到，给一个默认值
                    ext_json = jsonpath.jsonpath(json.loads(response), value)
                    if ext_json:
                        extract_date = {key: ext_json}
                    else:
                        extract_date = {key: "未提取到数据，该接口返回结果可能为空"}
                    logs.info('json提取到参数：%s' % extract_date)
                    self.read.write_yaml_data(extract_date)
        except:
            logs.error('接口返回值提取异常，请检查yaml文件extract_list表达式是否正确！')


    def extract_data_list(self, testcase_extract_list, response):
        """
        提取多个参数，支持正则表达式和json提取，提取结果以列表形式返回
        :param testcase_extract_list: yaml文件中的extract_list信息
        :param response: 接口的实际返回值,str类型
        :return:
        """
        try:
            for key, value in testcase_extract_list.items():
                if "$" in value:
                    # 增加提取判断，有些返回结果为空提取不到，给一个默认值
                    ext_json = jsonpath.jsonpath(json.loads(response), value)
                    if ext_json:
                        extract_date = {key: ext_json}
                    else:
                        extract_date = {key: "未提取到数据，该接口返回结果可能为空"}
                    logs.info('json提取到参数：%s' % extract_date)
                    self.read.write_yaml_data(extract_date)
        except:
            logs.error('接口返回值提取异常，请检查yaml文件extract_list表达式是否正确！')






if __name__ == '__main__':
    req = BaseRequests()
    data = get_testcase_yaml("../testcase/Login/login.yaml")[0]
    print(req.specification_yaml(data))