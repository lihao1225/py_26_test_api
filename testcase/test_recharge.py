'''
=======================
Author:李浩
时间：2020/2/25:14:45
Email:lihaolh_v@didichuxing.com
=======================
'''
import os
import unittest
import jsonpath
from library.ddt import ddt,data
from commom.read_excal import ReadExcal
from commom.handle_path import DATADIR
from commom.myconfig import conf
from commom.handle_request import SendRequest
from commom.connectdb import DB
from decimal import Decimal
from commom.handle_log import log
from commom.handle_data import CaseData,replace_data

file_path = os.path.join(DATADIR,"apicases.xlsx")

@ddt
class TestRegister(unittest.TestCase):
    excal = ReadExcal(file_path,"recharge")
    cases = excal.read_excal()
    request = SendRequest()
    db = DB()

    @classmethod
    def setUpClass(cls):
        #1准备登录数据
        url = conf.get("env","url")+"/member/login"
        data = {
            "mobile_phone":conf.get("test_data","phone"),
            "pwd":conf.get("test_data","pwd")
        }
        headers = eval(conf.get("env","headers"))
        #发送请求，进行登录
        response = cls.request.send_request(url=url,method="post",json=data,headers=headers)
        #获取返回数据
        res = response.json()
        #提取token保存为类属性
        token = jsonpath.jsonpath(res,"$..token")[0]
        token_type = jsonpath.jsonpath(res,"$..token_type")[0]
        #将提取到的token设置成类属性
        CaseData.token_value = token_type +" "+token
        #提取用户id，保存为类属性
        CaseData.member_id = str(jsonpath.jsonpath(res,"$..id")[0])

    @data(*cases)
    def test_recharge(self,case):
        #准备数据
        url = conf.get("env","url")+case["url"]
        method = case["method"]
        #替换参数中的用户id
        case["data"] = replace_data(case["data"])
        data = eval(case["data"])
        headers = eval(conf.get("env","headers"))
        headers["Authorization"] = getattr(CaseData,"token_value")
        expected =eval(case["expected"])
        row = case["case_id"]+1

        #第二步发送请求，获取结果
        #发送请求前，获取用户余额
        if case["check_sql"]:
            sql= "SELECT leave_amount FROM futureloan.member WHERE mobile_phone={}".format(
                conf.get( "test_data", "phone" ) )
            #查询用户当前余额
            start_money =self.db.find_one(sql)["leave_amount"]
        response = self.request.send_request(url=url,method=method,json=data,headers=headers)
        res =response.json()
        #发送完请求后获取余额
        if case["check_sql"]:
            sql = "SELECT leave_amount FROM futureloan.member WHERE mobile_phone={}".format(
                conf.get( "test_data", "phone" ) )
            end_money = self.db.find_one(sql)["leave_amount"]

        #第三步，断言
        try:
            self.assertEqual(expected["code"],res["code"])
            self.assertEqual(expected["msg"],res["msg"])
            if case["check_sql"]:
                self.assertEqual(end_money-start_money,Decimal(str(data["amount"])))
        except AssertionError as e:
            print(expected)
            print(res)
            self.excal.write_excal(row=row,column=8,value="未通过")
            log.error("用例执行{}未通过".format(case["title"]))
            log.exception(e)
            raise e
        else:
            self.excal.write_excal(row=row,column=8,value="通过")
            log.info("用例执行{}通过".format(case["title"]))

