'''
=======================
Author:李浩
时间：2020/3/2:9:03
Email:lihaolh_v@didichuxing.com
=======================
'''

"""
投资接口：
1需要有标：管理员登录，加标，审核
2用户登录
3投资用例的执行
关于投资的sql校验
1用户表校验余额减少是否发生变化，变化金额等于所投金额（根据用户id查询）
2根据member_id和loan_id去投资表中查用户投资记录，
3根据pay_member_id判断用户是否新增记录
4在刚好投满的情况下可以根据，可以根据投资记录的id，去回款计划表中查询是否生成回款计划
    

"""
import os
import unittest
import jsonpath
from commom.read_excal import ReadExcal
from library.ddt import data,ddt
from commom.handle_path import DATADIR
from commom.myconfig import conf
from commom.handle_data import CaseData,replace_data
from commom.handle_request import SendRequest
from commom.connectdb import DB
from decimal import Decimal
from commom.handle_log import log




file_path = os.path.join(DATADIR,"apicases.xlsx")


@ddt
class TestInvest(unittest.TestCase):
    excel = ReadExcal(file_path,"invest")
    cases = excel.read_excal()
    request = SendRequest()
    db = DB()
    @data(*cases)
    def test_invest(self,case):
        url = conf.get("env","url") + case["url"]
        method = case["method"]
        headers = eval(conf.get("env","headers"))
        if case["interface"] != "login":
            headers["Authorization"] = getattr(CaseData,"token_value")
        data = eval(replace_data(case["data"]))
        expected = eval(case["expected"])
        row = case["case_id"]+1
        #投资成功后的校验

        if case["check_sql"]:
            # 一，账号金额变化
            sql = "SELECT leave_amount FROM futureloan.member WHERE id = {}".format(CaseData.member_id)
            start_money = self.db.find_one(sql)["leave_amount"]
            #二，投资记录变化
            sql1 = "SELECT * FROM futureloan.invest WHERE member_id = {} and loan_id = {}".format(CaseData.member_id,CaseData.loan_id)
            start_invest = self.db.find_count(sql1)
            sql2 = "SELECT * FROM futureloan.financelog WHERE pay_member_id = {}".format(CaseData.member_id)
            start_financelog = self.db.find_count(sql2)
        response = self.request.send_request(url= url,method=method,headers=headers,json=data)
        res = response.json()
        if case["check_sql"]:
            sql = "SELECT leave_amount FROM futureloan.member WHERE id = {}". format( CaseData.member_id )
            end_money = self.db.find_one(sql)["leave_amount"]
            sql1 = "SELECT * FROM futureloan.invest WHERE member_id = {} and loan_id = {}".format(CaseData.member_id,CaseData.loan_id)
            end_invest = self.db.find_count( sql1 )
            sql2 = "SELECT * FROM futureloan.financelog WHERE pay_member_id = {}".format(CaseData.member_id)
            end_financelog = self.db.find_count(sql2)
        if case["interface"] == "login":
            token = jsonpath.jsonpath(res,"$..token")[0]
            token_type = jsonpath.jsonpath(res,"$..token_type")[0]
            CaseData.token_value = token_type+" "+token
            CaseData.member_id = str(jsonpath.jsonpath(res,"$..id")[0])
        if case["interface"] == "add":
            CaseData.loan_id = str(jsonpath.jsonpath(res,"$..id")[0])
        try:
            self.assertEqual(expected["code"],res["code"])
            # self.assertEqual(expected["msg"],res["msg"])
            self.assertIn(expected["msg"],res["msg"])
            if case["check_sql"]:
                self.assertEqual(start_money-end_money,Decimal(str(data["amount"])))
                self.assertEqual(end_invest-start_invest,1)
                self.assertEqual(end_financelog-start_financelog,1)
        except AssertionError as e:
            self.excel.write_excal(row=row,column=8,value="未通过")
            log.error( "测试用例{}未通过".format( case["title"] ) )
            log.exception( e )
            raise e
        else:
            self.excel.write_excal(row=row,column=8,value="通过")
            log.info("测试用例{}未通过".format( case["title"] ))