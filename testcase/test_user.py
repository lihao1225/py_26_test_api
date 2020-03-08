'''
=======================
Author:李浩
时间：2020/3/3:18:47
Email:lihaolh_v@didichuxing.com
=======================
'''
import os
import unittest
import jsonpath
from commom.read_excal import ReadExcal
from library.ddt import data, ddt
from commom.handle_path import DATADIR
from commom.myconfig import conf
from commom.handle_request import SendRequest
from commom.handle_data import CaseData, replace_data
from commom.connectdb import DB
from commom.handle_log import log

file_path = os.path.join( DATADIR, "apicases.xlsx" )


@ddt
class TestUser( unittest.TestCase ):
    excel = ReadExcal( file_path, "user" )
    cases = excel.read_excal()
    request = SendRequest()
    db = DB()

    @classmethod
    def setUpClass(cls) -> None:
        url = conf.get( "env", "url" ) + "/member/login"
        headers = eval( conf.get( "env", "headers" ) )
        data = {
            "mobile_phone": conf.get( "test_data", "phone" ),
            "pwd": conf.get( "test_data", "pwd" )
        }
        response = cls.request.send_request( url=url, headers=headers, method="post", json=data )
        res = response.json()
        token = jsonpath.jsonpath( res, "$..token" )[0]
        token_type = jsonpath.jsonpath( res, "$..token_type" )[0]
        CaseData.token_value = token_type + " " + token
        member_id = jsonpath.jsonpath( res, "$..id" )[0]
        CaseData.member_id = str( member_id )


    @data( *cases )
    def test_user(self, case):
        url = conf.get( "env", "url" ) + replace_data( case["url"] )
        method = case["method"]
        headers = eval( conf.get( "env", "headers" ) )
        headers["Authorization"] = getattr( CaseData, "token_value" )
        expected=eval(case["expected"])
        row = case["case_id"]+1
        response = self.request.send_request(url=url,method=method,headers=headers)
        res = response.json()
        user_id = jsonpath.jsonpath(res,"$..id")[0]
        CaseData.user_id = str(user_id)



        try:
            self.assertEqual(expected["code"],res["code"])
            self.assertEqual(expected["msg"],res["msg"])
            if case["check_sql"]:
                sql = replace_data( case["check_sql"] )
                user_phone = self.db.find_one( sql )["mobile_phone"]
                self.assertEqual(conf.get("test_data","phone"),user_phone)
        except AssertionError as e:
            print(expected)
            print(res)
            self.excel.write_excal(row=row,column=8,value="未通过")
            log.error("用例执行{}未通过".format(case["title"]))
            log.exception(e)
            raise e
        else:
            self.excel.write_excal(row=row,column=8,value="通过")
            log.info("用例执行{}通过".format(case["title"]))