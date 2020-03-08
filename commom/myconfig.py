'''
=======================
Author:李浩
时间：2020/2/25:10:14
Email:lihaolh_v@didichuxing.com
=======================
'''
import os
from configparser import ConfigParser
from commom.handle_path import CONFDIR
class HandConfig(ConfigParser):
    def __init__(self,file_name):
        super().__init__()
        self.file_name = file_name
        self.read(file_name,encoding="utf-8")

    def write_conf(self,section,option,value):
        self.set(section=section,option=option,value=value)
        self.write(fp=open(self.file_name,"w"))

conf = HandConfig(os.path.join(CONFDIR,"config.ini"))