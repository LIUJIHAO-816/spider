# -*- coding: utf-8 -*- 
__author__ = 'Liujuhao'  # 输入路径

import time
import datetime
import re
import numpy as np
import pandas as pd
import matplotlib as plt

in_path = "C:\Users\Liujuhao\Desktop\汉东省办公厅.txt"
# in_path = "C:\Users\Liujuhao\Desktop\五舟汉云.txt"

out_path = "C:\Users\Liujuhao\Desktop\汉东省办公厅" + str(int(time.time())) + ".xlsx"

upath = unicode(in_path, "utf-8")

opath = unicode(out_path, "utf-8")

fopen = open(upath)

lines = fopen.readlines()

re_1 = "(.*\\-.*\\-.*)\s{1}(.*)\s{1}(.*)"

dict_name_times = {}

flag = True
start = ""
end = ""

v_keys = [u"累计次数", u"话题发起次数"]

p_time = datetime.datetime.strptime("00:00:00", '%H:%M:%S')
p_day = ""

for line in lines:
    if not len(line) or line.isspace():
        continue
    try:
        if re.match(re_1, line):
            # print unicode(line, "utf8")
            title = re.split("\s", line)
            time = title[1]
            name = title[2]

            if flag:
                start = title[0] + " " + title[1]
                flag = False
            if "09:00:00" < time < "18:00:00":
                if dict_name_times.has_key(name):
                    dict_name_times[name][v_keys[0]] += 1
                else:
                    dict_name_times[name] = {v_keys[0]: 1, v_keys[1]: 0}

                c_time = datetime.datetime.strptime(time, '%H:%M:%S')

                if title[0] == p_day:
                    if str(c_time - p_time).zfill(8) > "01:00:00":
                        # print str(c_time - p_time)
                        dict_name_times[name][v_keys[1]] += 1
                else:
                    dict_name_times[name][v_keys[1]] += 1

                p_time = c_time
                p_day = title[0]

            # if (c_time - p_time).hour > 1:
            #     print "aaa"

            end = title[0] + " " + title[1]
    except:
        continue

print unicode("起算时间：" + start, "utf-8"), unicode("\n截止时间：" + end, "utf-8")
date1 = datetime.datetime.strptime(start, '%Y-%m-%d %H:%M:%S')
date2 = datetime.datetime.strptime(end, '%Y-%m-%d %H:%M:%S')
print unicode("共计：", 'utf-8') + str((date2 - date1)) + "\n" + "-" * 40

dirty_key = ['10000', '搁浅', '系统消息(10000)']  #手动在此添加过滤项

for dk in dirty_key:
    if dict_name_times.has_key(dk):
        del dict_name_times[dk]

df = pd.DataFrame(dict_name_times).T
print df

df.plot()
