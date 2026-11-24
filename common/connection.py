from common.recordlog import logs
from conf.operateCoinfig import OperateConfig
import pymysql

conf = OperateConfig()

class ConnectMySql:
    """连接读取MySQL的数据"""

    def __init__(self):

        mysql_conf = {
            'host': conf.get_mysql_conf('host'),
            'port': int(conf.get_mysql_conf('port')),
            'user': conf.get_mysql_conf('username'),
            'password': conf.get_mysql_conf('password'),
            'database': conf.get_mysql_conf('database')
        }

        try:
            self.conn = pymysql.connect(**mysql_conf,charset='utf8')
            # cursor=pymysql.cursors.DictCursor：将数据库表地钻以key-value形式显示
            self.cursor = self.conn.cursor(cursor=pymysql.cursors.DictCursor)
            logs.info("""成功连接到MySQL数据库
            host:{host}
            port:{port}
            db:{database}
            """.format(**mysql_conf))
        except Exception as e:
            logs.error(e)


    def close(self):
        """关闭数据库连接"""
        if self.conn and self.cursor:
            self.cursor.close()
            self.conn.close()


    def query(self,sql):
        """查询数据"""
        try:
            self.cursor.execute(sql)
            self.conn.commit()
            res = self.cursor.fetchall()
            return res
        except Exception as e:
            logs.error(e)
        finally:
            self.close()



