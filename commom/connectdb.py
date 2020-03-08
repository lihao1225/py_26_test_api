'''
=======================
Author:李浩
时间：2020/2/25:14:26
Email:lihaolh_v@didichuxing.com
=======================
'''
import pymysql
from commom.myconfig import conf
class DB:
    def __init__(self):
        #创建一个对象
        self.conn = pymysql.connect(host=conf.get("mysql","host"),
                                    port= conf.getint("mysql","port"),
                                    user = conf.get("mysql","user"),
                                    password =conf.get("mysql","pwd"),
                                    charset = conf.get("mysql","charset"),
                                    cursorclass = pymysql.cursors.DictCursor)

        #创建一个游标
        self.cur =self.conn.cursor()
    #查询一条数据
    def find_one(self,sql):
        """获取查询出来的第一条数据"""
        self.conn.commit()
        self.cur.execute(sql)
        data =self.cur.fetchone()
        return data
    def find_all(self,sql):
        """获取查询出来的所有数据"""
        self.conn.commit()
        self.cur.execute(sql)
        data = self.cur.fetchall()
        return data
    def find_count(self,sql):
        """返回查询数据的条数"""
        self.conn.commit()
        return self.cur.execute(sql)

    def close(self):
        """关闭游标，断开连接"""
        self.cur.close()
        self.conn.close()
