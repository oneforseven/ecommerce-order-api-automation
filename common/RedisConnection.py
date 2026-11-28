from common.recordlog import logs
from conf.operateCoinfig import OperateConfig
import pymysql
import redis
from rediscluster import RedisCluster

conf = OperateConfig()

class RedisClient:
    """
    从Redis中读取、设置相关数据
    """

    def __init__(self):

        self.__redis_conf = {
            'host': conf.get_redis_conf('host'),
            'port': int(conf.get_redis_conf('port')),
            'username': conf.get_redis_conf('username') or None,
            'password': conf.get_redis_conf('password') or None,
            'db' : int(conf.get_redis_conf('db'))
        }

        redis_nodes_str = conf.get_redis_conf('startup_nodes')
        self.node_list = []
        if redis_nodes_str:
            node_str_list = redis_nodes_str.split(',')
            for node_str in node_str_list:
                host,port = node_str.split(',')
                node_data = {'host':host, 'port':port}
                self.node_list.append(node_data)

            self.redis_cluster = RedisCluster(startup_nodes=self.node_list)
            logs.info(f"连接到Redis集群服务，host:{redis_nodes_str}")

        elif self.__redis_conf['host'] and self.__redis_conf['port']:

            try:
                logs.info(f"连接到Redis服务器：ip：{self.__redis_conf['host']}")
                # 建立连接
                pool = redis.ConnectionPool(**self.__redis_conf)
                self.redis_cluster = redis.Redis(connection_pool=pool)
            except Exception as e:
                logs.error(f"Redis连接失败,{e}")

    @classmethod
    def redis_except(cls,e):
        if 'MOVED' in e:
            logs.error(f"请检查Redis是否使用了集群模式或者主从复制的情况，数据被迁移到了另外一个Redis实例上：{e}")
        else:
            logs.error(f'Redis Error：{e}')

    def get(self,key):
        """
        获取Redis里面的数据
        :param key: Redis里面的键
        :return:
        """
        try:
            value = self.redis_cluster.get(key)
            if isinstance(value,bytes):
                return value.decode('utf-8')
            return value
        except Exception as e:
            self.redis_except(e)


    def set(self,key,value,ex=None):
        """
        设置Redis的值
        :param key: Redis键
        :param value: 需要设置的内容
        :param ex: 过期时间（s）
        :return:
        """
        try:
            return self.redis_cluster.set(name=key,value=value,ex=ex)
        except Exception as e:
            logs.redis_except(e)




if __name__ == '__main__':
    redis_con = RedisClient()
    key = "openapi:token:uquqwdqdqwdo0qw01@!&##"
    res = redis_con.get(key)
    print(res,type(res))