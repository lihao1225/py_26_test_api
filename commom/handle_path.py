'''
=======================
Author:李浩
时间：2020/2/25:10:19
Email:lihaolh_v@didichuxing.com
=======================
'''

import os

#文件根目录路径
DIRPATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
#配置文件的目录路径
CONFDIR = os.path.join(DIRPATH,"config")
#配置日志的目录路径
LOGDIR = os.path.join(DIRPATH,"logs")
#配置excal的目录路径
DATADIR = os.path.join(DIRPATH,"data")
#测试用例类目录路径
CASEDIR = os.path.join(DIRPATH,"testcase")
#测试报告的目录路径
REPORT = os.path.join(DIRPATH,"reports")