'''
=======================
Author:李浩
时间：2020/3/1:12:23
Email:lihaolh_v@didichuxing.com
=======================
'''
import os
import unittest
import jsonpath
from library.ddt import ddt, data
from commom.read_excal import ReadExcal
from commom.handle_path import DATADIR
from commom.myconfig import conf
from commom.handle_request import SendRequest
from commom.handle_data import CaseData, replace_data
from commom.handle_log import log
from commom.connectdb import DB

file_name = os.path.join( DATADIR, "apicases.xlsx" )


@ddt
class TestAdd( unittest.TestCase ):
    excel = ReadExcal( file_name, "add" )
    cases = excel.read_excal()
    request = SendRequest()
    db = DB()


    @classmethod
    def setUpClass(cls):
        """管理员账户登录"""
        url = conf.get("env", "url") + "/member/login"
        data = {
            "mobile_phone": conf.get("test_data", "admin_phone"),
            "pwd": conf.get("test_data", "admin_pwd")
        }
        headers = eval(conf.get("env", "headers"))
        response = cls.request.send_request(url=url, method="post", json=data, headers=headers)
        res = response.json()
        token = jsonpath.jsonpath(res, "$..token")[0]
        token_type = jsonpath.jsonpath(res, "$..token_type")[0]
        member_id = jsonpath.jsonpath(res, "$..id")[0]
        # 将提取的数据保存到CaseData的属性中
        CaseData.admin_token_value = token_type + " " + token
        CaseData.admin_member_id = str(member_id)

    @data( *cases )
    def test_add(self, case):
        url = conf.get( "env", "url" ) + case["url"]
        method = case["method"]
        headers = eval( conf.get( "env", "headers" ) )
        headers["Authorization"] = getattr( CaseData, "admin_token_value" )
        data = eval( replace_data( case["data"] ) )
        expected = eval( case["expected"] )
        row = case["case_id"] + 1

        response = self.request.send_request( url=url, method=method, json=data, headers=headers )
        res = response.json()

        # 第三步：断言（比对预期结果和实际结果）
        try:
            self.assertEqual( expected["code"], res["code"] )
            self.assertEqual( expected["msg"], res["msg"] )
            # 数据库校验
            if case["check_sql"]:
                loan_id = jsonpath.jsonpath( res, "$..id" )[0]
                CaseData.loan_id = str( loan_id )
                sql = replace_data( case["check_sql"] )
                sql_loan_id = self.db.find_one( sql )["id"]
                self.assertEqual( sql_loan_id, loan_id )

        except AssertionError as e:
            print( "预期结果：", expected )
            print( "实际结果：", res )
            self.excel.write_excal( row=row, column=8, value="未通过" )
            log.error( "用例：{}，执行未通过".format( case["title"] ) )
            log.exception( e )
            raise e
        else:
            self.excel.write_excal( row=row, column=8, value="通过" )
            log.info( "用例：{}，执行未通过".format( case["title"] ) )
