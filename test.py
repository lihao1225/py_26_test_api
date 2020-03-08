'''
=======================
Author:李浩
时间：2020/2/25:18:57
Email:lihaolh_v@didichuxing.com
=======================
'''
import pymysql
import re

"""
主机：
port：3306
用户：future
密码：123456
"""

str1 = "1232#ddd#12321#yyy#123#fff#"
res = re.findall(r"#(.+)#",str1)
print(res)
# # 第一步：连接到数据库
# conn = pymysql.connect(host="120.78.128.25",
#                        port=3306,
#                        user="future",
#                        password="123456",
#                        charset="utf8")
#
# # 第二步:创建一个游标对象
# cur = conn.cursor()
#
#
# # 第三步：执行sql语句
# # sql = "SELECT id FROM futureloan.member WHERE mobile_phone=13367899876"
# # sql2 = "SELECT * FROM  futureloan.member LIMIT 10"
# sql ="SELECT mobile_phone FROM futureloan.member WHERE mobile_phone=13367899876"
# res = cur.execute(sql)
# # 返回的是查询到的数据条数
# # print(res)
#
# # 第四步：获取查询的数据
# # fechone:获取一条数据(返回的查询集中的第一条数据，元组类型)
# data = cur.fetchone()
# print(data)
# print(cur.fetchone())
# print(cur.fetchone())
# print(cur.fetchone())


# 获取查询集中的所有数据
# datas = cur.fetchall()
# print(datas)


# 注意点：pymysql操作数据库。默认是开启事务的。
# 关键增加、删除、修改等相关涉及到数据库中数据变动的sql语句执行
# 执行的方式和查询是一样的
# cur.execute(sql2)
# 在执行完sql语句之后，要多出一步：调用commit提交事务
# conn.commit()




# pymssql  操作sql server
# cx_oracle: 操作oracel
s="1987-02-09 07:30:00 "
res = re.findall(r"\d{4}|-\d{2}",s)
print(res)

s1="aaaa  xiasd@163.com 77777777777 xiaori@139.com aaaaaaa"
res1 = re.findall(r"\bxiasd@163.com|\bxiaori@139.com",s1)
print(res1)

matchstr = "_abc, abc, abc_1, 1_abc, abc$, @#!,8xiap"
res2 = re.findall(r"(\b[a-zA-Z_]\w+\b)",matchstr)
print(res2)
