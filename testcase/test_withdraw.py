'''
=======================
Author:李浩
时间：2020/2/26:20:15
Email:lihaolh_v@didichuxing.com
=======================
'''
import os
import unittest
from library.ddt import ddt,data
from commom.read_excal import ReadExcal
from commom.handle_path import DATADIR
from commom.myconfig import conf
from commom.handle_request import SendRequest
from commom.handle_log import log
import jsonpath
from commom.connectdb import DB
from decimal import Decimal
file_path = os.path.join(DATADIR,"apicases.xlsx")

@ddt
class TestWithdraw(unittest.TestCase):
    excal = ReadExcal(file_path,"withdraw")
    cases = excal.read_excal()
    request =SendRequest()
    db = DB()
    @data(*cases)
    def test_withdraw(self,case):
        #准备用例数据
        url = conf.get("env","url")+case["url"]
        case["data"] = case["data"].replace("#phone#",conf.get("test_data","phone"))
        case["data"] = case["data"].replace("#pwd#",conf.get("test_data","pwd"))
        headers = eval( conf.get( "env", "headers" ) )
        # 判断是否是取现接口，取现接口则加上请求头
        if case["interface"].lower() == "withdraw":
            headers["Authorization"] = self.token_value
            case["data"] = case["data"].replace("#member_id#",str(self.member_id))
        data = eval(case["data"])
        expected = eval(case["expected"])

        method = case["method"]
        row = case["case_id"]+1
        #判断是否需要sql校验
        if case["check_sql"]:
            sql = case["check_sql"].format(conf.get("test_data","phone"))
            start_money = self.db.find_one(sql)["leave_amount"]

        response = self.request.send_request(url=url,headers=headers,method=method,json=data)
        res = response.json()
        if case["interface"]=="login":
            #提取用户id保存为类属性
            TestWithdraw.member_id = jsonpath.jsonpath(res,"$..id")[0]
            token= jsonpath.jsonpath(res,"$..token")[0]
            token_type = jsonpath.jsonpath(res,"$..token")[0]
            TestWithdraw.token_value = token_type+" "+token

        try:
            self.assertEqual(expected["code"],res["code"])
            self.assertEqual(expected["msg"],res["msg"])
            if case["check_sql"]:
                sql = case["check_sql"].format( conf.get( "test_data", "phone" ) )
                end_money = self.db.find_one( sql )["leave_amount"]
                self.assertEqual(Decimal(str(case["amount"])),start_money-end_money)
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

