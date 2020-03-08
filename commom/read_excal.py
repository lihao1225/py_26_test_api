'''
=======================
Author:李浩
时间：2020/2/25:10:00
Email:lihaolh_v@didichuxing.com
=======================
'''
import openpyxl

class ReadExcal(object):
    def __init__(self,file_name,sheet_name):
        self.file_name = file_name
        self.sheet_name = sheet_name

    def open(self):
        self.wb = openpyxl.load_workbook(self.file_name)
        self.sh = self.wb[self.sheet_name]


    def read_excal(self):
        self.open()
        #获取出excal中的所有数据转换为列表
        data = list(self.sh.rows)
        #创建一个空列表来存储数据
        case_data = []
        #使用列表推导式获取表头数据
        title = [i.value for i in data[0]]
        #使用列表推导式获取除表头的其他所有数据
        for j in data[1:]:
            values = [k.value for k in j]
            #只用zip函数把表头和每行数据组合成需要的数据
            case_data1 = dict(zip(title,values))
            #把所有组合数据放在新列表中
            case_data.append(case_data1)
        return case_data

    def write_excal(self,row,column,value):
        self.open()
        self.sh.cell(row=row,column=column,value=value)
        self.wb.save(self.file_name)