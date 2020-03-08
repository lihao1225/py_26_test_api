'''
=======================
Author:李浩
时间：2020/2/28:20:45
Email:lihaolh_v@didichuxing.com
=======================
'''
import re
from commom.myconfig import conf


class CaseData:
    pass


def replace_data(s):
    r1 = r"#(.+?)#"
    while re.search( r1, s ):
        res = re.search( r1, s )
        data = res.group()
        key = res.group( 1 )
        try:
            # s = re.sub(r1,conf.get("test_data",key),s,1)
            s = s.replace( data, conf.get( "test_data", key ) )
        except Exception:
            s = s.replace( data, getattr( CaseData, key ) )
    return s


# class CaseData:
#     """这个类专门用来保存，执行执行过程中提取出来给其他用例用的数据"""
#     pass
#

# def replace_data(s):
#     r1 = r"#(.+?)#"
#     # 根据是否匹配到要替换的数据，来决定要不要进入循环
#     while re.search(r1, s):
#         # 匹配一个需要替换的内容
#         res = re.search(r1, s)
#         # 获取待替换的内容
#         data = res.group()
#         # 获取需要替换的字段
#         key = res.group(1)
#         try:
#             # 根据要替换的字典，去配置文件中找到对应的数据，进行替换
#             s = s.replace(data, conf.get("test_data", key))
#         except Exception:
#             # 如果配置文件中找不到，报错了，则去CaseData的属性中找对应的值进行替换
#             s = s.replace(data, getattr(CaseData, key))
#     return s


#
# def replace_data(s):
#     r1 = r"#(.+?)#"
#     while re.search(r1, s):
#         res = re.search(r1, s)
#         key = res.group(1)
#         try:
#             value = conf.get("test_data", key)
#         except Exception:
#             value = getattr(CaseDate, key)
#         finally:
#             s = re.sub(r1, value, s, 1)
#     return s


if __name__ == '__main__':
    # s = "123#member_id#111111"
    # res = replace_data(s)
    # print(res)
    pass
