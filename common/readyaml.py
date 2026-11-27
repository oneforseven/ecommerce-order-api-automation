import yaml
import os
from common.recordlog import logs
from conf.setting import FILE_PATH

def get_testcase_yaml(file):
    """
        获取 yaml 文件的数据
        :param file: yaml 文件的路径
        :return:
        """
    testcase_list = []
    try:
        with open(file, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
            if len(data) <= 1:
                yam_data = data[0]
                base_info = yam_data.get('baseInfo')
                for ts in yam_data.get('testCase'):
                    param = [base_info, ts]
                    testcase_list.append(param)
                return testcase_list
            else:
                return data
    except UnicodeDecodeError:
        logs.error(f"[{file}]文件编码格式错误，--尝试使用utf-8编码解码YAML文件时发生了错误，请确保你的yaml文件是UTF-8格式！")
    except FileNotFoundError:
        logs.error(f'[{file}]文件未找到，请检查路径是否正确')
    except Exception as e:
        logs.error(f'获取【{file}】文件数据时出现未知错误: {str(e)}')


class ReadYamlData:
    """读取yaml数据。以及写入数据yaml文件"""

    def __init__(self,yaml_file=None):
        if yaml_file is not None:
            self.yaml_file = yaml_file
        else:
            self.yaml_file = "../testcase/Login/login.yaml"

    def write_yaml_data(self,value):
        """
        写入数据到yaml文件
        :param value: （dist）写入的数据
        :return:
        """
        file_path = FILE_PATH['extract']
        if not isinstance(value,dict):
            print("写入到【extract.yaml】的数据必须为字典类型")
            return
        # 先读出旧数据（文件不存在或为空时{}）
        old_data = {}
        if os.path.exists(file_path):
            try:
                with open(file_path,"r",encoding="utf-8") as rf:
                    old_data = yaml.safe_load(rf) or {}
            except Exception as e:
                print(e)
        # 合并
        old_data.update(value)
        # 覆盖写回整份文件
        try:
            with open(file_path,"w",encoding="utf-8") as wf:
                yaml.dump(old_data,wf,allow_unicode=True,sort_keys=False)
        except Exception as e:
            print(e)


    def get_extract_yaml(self,node_name):
        """
        读取接口提取的变量值
        :param node_name: yaml文件的key值
        :return:
        """
        file_path = FILE_PATH['extract']

        if os.path.exists(file_path):
            pass
        else:
            print("extract不存在")
            file = open(file_path,"w")
            file.close()
            print("extract.yaml创建成功")

        with open(file_path,"r",encoding="utf-8") as rf:
            extract_data = yaml.safe_load(rf)
            return extract_data[node_name]

