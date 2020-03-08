'''
=======================
Author:李浩
时间：2020/2/25:15:34
Email:lihaolh_v@didichuxing.com
=======================
'''
import os
import unittest
from commom.handle_path import CASEDIR,REPORT
from library.HTMLTestRunnerNew import HTMLTestRunner
from commom.handle_email import send_email

suite = unittest.TestSuite()

loader = unittest.TestLoader()
case = suite.addTest(loader.discover(CASEDIR))

runner = HTMLTestRunner(stream=open(os.path.join(REPORT,"report.html"),"wb"),
                        title="自己写",
                        description="全部重新写的",
                        tester="lihao")
runner.run(suite)

report_file = os.path.join(REPORT,"report.html")
send_email(report_file,"自己写")