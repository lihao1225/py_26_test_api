'''
=======================
Author:李浩
时间：2020/3/4:16:04
Email:lihaolh_v@didichuxing.com
=======================
'''
import os
import unittest
import jsonpath
from library.ddt import data,ddt
from commom.read_excal import ReadExcal
from commom.handle_path import DATADIR
from commom.myconfig import conf
from commom.handle_request import SendRequest
from commom.handle_log import log

file_path = os.path.join(DATADIR,"apicases.xlsx")

@ddt
class TestLoans(unittest.TestCase):
    excel = ReadExcal(file_path,"loans")
    cases = excel.read_excal()
    request = SendRequest()
    @data(*cases)
    def test_loans(self,case):
        url = conf.get("env","url") + case["url"]
        method = case["method"]
        headers = eval(conf.get("env","headers"))
        data = eval(case["data"])
        expected = eval(case["expected"])
        row = case["case_id"]+1
        response = self.request.send_request(url=url,method=method,headers=headers,params=data)
        res = response.json()
        count = jsonpath.jsonpath(res,"$..data")[0]
        count1 = len(count)

        try:
            self.assertEqual( expected["code"], res["code"] )
            self.assertEqual(expected["msg"],res["msg"])
            if case["title"] !="不传参数":
                self.assertEqual(data["pageSize"],count1)
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
