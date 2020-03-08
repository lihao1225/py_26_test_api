'''
=======================
Author:李浩
时间：2020/2/28:11:35
Email:lihaolh_v@didichuxing.com
=======================
'''
import re
s="1987-02-09 07:30:00 "
res = re.findall(r"\d{4}|-\d{2}",s)
res6 = re.findall(r"(\d+?)-(\d+?)-(\d+?)",s)
print(res6)

s1="aaaa  xiasd@163.com 77777777777 xiaori@139.com aaaaaaa"
res1 = re.findall(r"\bxiasd@163.com|\bxiaori@139.com",s1)
res5=re.findall(r"\w+@\w+.com",s1)
print(res5)

matchstr = "_abc, abc, abc_1, 1_abc, abc$, @#!,8xiap"
res2 = re.findall(r"(\b[a-zA-Z_]\w+\b)",matchstr)
print(res2)
