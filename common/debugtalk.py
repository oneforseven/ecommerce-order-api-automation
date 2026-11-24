from common.readyaml import ReadYamlData
import random

class DebugTalk:

    def __init__(self):
        self.read = ReadYamlData()

    def get_extract_order_data(self, data, randoms):
        """胡哦去extract.yaml数据，不为0，-1，-2的情况，就按顺序取读取key里面的数据"""
        if randoms not in [0, -1, -2]:
            return data[randoms - 1]

    def get_extract_data(self, node_name):
        """获取 extract.yaml 中的单个值（字符串/数字）"""
        return self.read.get_extract_yaml(node_name)

    def get_extract_data_list(self, node_name, randoms=None):
        """
        获取 extract.yaml的数据
        :param node_name: extract.yaml中的key值
        :param randoms: 0=随机取一个; 正数n=取第n个; -1=逗号拼接; -2=拆成列表
        :return:
        """
        data = self.read.get_extract_yaml(node_name)
        if randoms is None:
            return data

        randoms = int(randoms)
        if randoms == 0:
            return random.choice(data)
        if randoms == -1:
            return ','.join(data)
        if randoms == -2:
            return ','.join(data).split(',')
        return self.get_extract_order_data(data,randoms)





    def md5_params(self,params):
        print("实现md5加密")