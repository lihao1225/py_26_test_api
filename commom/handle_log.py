'''
=======================
Author:李浩
时间：2020/2/25:10:28
Email:lihaolh_v@didichuxing.com
=======================
'''
import os
import logging
from commom.myconfig import conf
from commom.handle_path import LOGDIR

class HandLog(object):
    @staticmethod
    def create_log():
        #创建收集器，设置收集器等级
        mylog = logging.getLogger(conf.get("log","name"))
        mylog.setLevel(conf.get("log","level"))
        #创建输出到控制台，设置等级
        sh =logging.StreamHandler()
        sh.setLevel(conf.get("log","sh_level"))
        mylog.addHandler(sh)
        #创建输出到文件，设置等级
        fh = logging.FileHandler(filename=os.path.join(LOGDIR,"log.log"),encoding="utf-8" )
        fh.setLevel(conf.get("log","fh_level"))
        mylog.addHandler(fh)
        #设置日志输出格式
        formater = '%(asctime)s - [%(filename)s-->line:%(lineno)d] - %(levelname)s: %(message)s'
        fm = logging.Formatter(formater)
        sh.setFormatter(fm)
        fh.setFormatter(fm)
        return mylog

log =HandLog.create_log()