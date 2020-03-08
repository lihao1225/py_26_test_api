'''
=======================
Author:李浩
时间：2020/2/26:10:51
Email:lihaolh_v@didichuxing.com
=======================
'''
# import os
# import unittest
# import jsonpath
# from library.ddt import ddt,data
# from commom.read_excal import ReadExcal
# from commom.handle_path import DATADIR
# from commom.myconfig import conf
# from commom.handle_request import SendRequest
# from commom.connectdb import DB
# from decimal import Decimal
# from commom.handle_log import log
#
# file_case = os.path.join(DATADIR,"apicases.xlsx")
# @ddt
# class TestWithdrawal(unittest.TestCase):
#     excal = ReadExcal(file_case,"withdrawal")
#     cases = excal.read_excal()
#     request = SendRequest()
#     db = DB()
#
#     @classmethod
#     def setUpClass(cls):
#     #1准备登陆数据
#         url = conf.get("env","url")+"/member/login"
#         data = {
#             "mobile_phone":conf.get("test_data","phone"),
#             "pwd":conf.get("test_data","pwd")
#         }
#         headers = eval(conf.get("env","headers"))
#         response = cls.request.send_request(url=url,method="post",json=data,headers=headers)
#         res =response.json()
#         #提取token保存为类属性
#         token = jsonpath.jsonpath(res,"$..token")[0]
#         token_type = jsonpath.jsonpath(res,"$..token_type")[0]
#         #将提取到的token设置成类属性
#         cls.token_values= token_type+" "+token
#         #提取用户id保存为类属性
#         cls.member_id = jsonpath.jsonpath(res,"$..id")[0]
#     @data(*cases)
#     def test_withdrawal(self,case):
#         #准备数据
#         url = conf.get("env","url")+case["url"]
#         method =case["method"]
#         headers = eval(conf.get("env","headers"))
#         headers["Authorization"]=self.token_values
#         case["data"] = case["data"].replace("#member_id#",str(self.member_id))
#         data = eval(case["data"])
#         expected = eval(case["expected"])
#         row = case["case_id"]+1
#         #发送请求前获取用户余额
#         if case["check_sql"]:
#             sql ="SELECT leave_amount FROM futureloan.member WHERE mobile_phone = {}".format(conf.get("test_data","phone"))
#             #查询用户当前余额
#             start_money = self.db.find_one(sql)["leave_amount"]
#         response = self.request.send_request(url=url,method=method,headers=headers,json=data)
#         res = response.json()
#         #发送完请求后获取用户余额
#         if case["check_sql"]:
#             sql="SELECT leave_amount FROM futureloan.member WHERE mobile_phone = {}".format(conf.get("test_data","phone"))
#             #查询用户剩余余额
#             end_money = self.db.find_one(sql)["leave_amount"]
#         try:
#             self.assertEqual(expected["code"],res["code"])
#             self.assertEqual(expected["msg"],res["msg"])
#             self.assertEqual(start_money-end_money,Decimal(str(data["amount"])))
#         except AssertionError as e:
#             print(expected)
#             print(res)
#             self.excal.write_excal(row=row,column=8,value="未通过")
#             log.error("用例{}执行未通过".format(case["title"]))
#             log.exception(e)
#             raise e
#         else:
#             self.excal.write_excal(row=row,column=8,value="通过")
#             log.info("用例{}执行通过".format(case["title"]))
#


