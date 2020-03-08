'''
=======================
Author:李浩
时间：2020/2/25:16:27
Email:lihaolh_v@didichuxing.com
=======================
'''
import os
import unittest
import random
from library.ddt import ddt,data
from commom.read_excal import ReadExcal
from commom.handle_path import DATADIR
from commom.myconfig import conf
from commom.handle_request import SendRequest
from commom.connectdb import DB
from commom.handle_log import log
case_file = os.path.join(DATADIR,"apicases.xlsx")
@ddt
class TestRegister(unittest.TestCase):
    excal = ReadExcal(case_file,"register")
    cases = excal.read_excal()
    request = SendRequest()
    db = DB()

    @data(*cases)
    def test_register(self,case):
        #准备数据
        url = conf.get("env","url")+case["url"]
        method = case["method"]
        #生成一个手机号
        phone = self.random_phone()
        #替换用例数据中的手机号
        case["data"] = case["data"].replace("#phone#",phone)
        headers = eval(conf.get("env","headers"))
        data = eval(case["data"])
        expected = eval(case["expected"])
        row = case["case_id"]+1
        response = self.request.send_request(url=url,method=method,headers=headers,json=data)
        res = response.json()

        try:
            self.assertEqual(expected["code"],res["code"])
            self.assertEqual(expected["msg"],res["msg"])
            if case["check_sql"]:
                sql = "SELECT * FROM futureloan.member WHERE mobile_phone={}".format( data["mobile_phone"] )
                # 查询手机号
                count = self.db.find_count( sql )
                self.assertEqual( 1, count )
        except AssertionError as e:
            print( "预期结果：", expected )
            print( "实际结果：", res )
            self.excal.write_excal( row=row, column=8, value="未通过" )
            log.error( "用例：{}，执行未通过".format( case["title"] ) )
            log.exception( e )
            raise e
        else:
            self.excal.write_excal( row=row, column=8, value="通过" )
            log.info( "用例：{}，执行未通过".format( case["title"] ) )





    def random_phone(self):
        phone = "138"
        n = random.randint(100000000,999999999)
        phone +=str(n)[1:]
        return phone