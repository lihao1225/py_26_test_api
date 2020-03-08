'''
=======================
Author:李浩
时间：2020/3/4:9:30
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
from commom.connectdb import DB
from commom.handle_log import log

file_path = os.path.join( DATADIR, "apicases.xlsx" )


@ddt
class TestUpdate( unittest.TestCase ):
    excel = ReadExcal( file_path, "update" )
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
        member_id = jsonpath.jsonpath( res, "$..id" )[0]
        CaseData.member_id = str( member_id )
        CaseData.token_value = token_type + " " + token

    @data( *cases )
    def test_update(self, case):
        url = conf.get( "env", "url" ) + case["url"]
        method = case["method"]
        headers = eval( conf.get( "env", "headers" ) )
        headers["Authorization"] = getattr( CaseData, "token_value" )
        data = eval( replace_data( case["data"] ) )
        expected = eval( case["expected"] )
        row = case["case_id"] + 1

        response = self.request.send_request( url=url, method=method, headers=headers, json=data )
        res = response.json()

        try:
            self.assertEqual( expected["code"], res["code"] )
            self.assertEqual( expected["msg"], res["msg"] )
            if case["check_sql"]:
                sql = replace_data( case["check_sql"] )
                reg_name = self.db.find_one( sql )["reg_name"]
                self.assertEqual( reg_name, data["reg_name"] )
        except AssertionError as e:
            print( expected )
            print( res )
            self.excel.write_excal( row=row, column=8, value="未通过" )
            log.error( "测试用例{}未通过".format( case["title"] ) )
            log.exception( e )
            raise e
        else:
            self.excel.write_excal( row=row, column=8, value="通过" )
            log.info( "测试用例{}通过".format( case["title"] ) )
