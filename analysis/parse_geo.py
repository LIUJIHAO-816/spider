# -*- coding: utf-8 -*- 
__author__ = 'Liujuhao'

import pymysql

db = pymysql.connect("172.20.31.108", "mysql", "mysql", "information", charset='utf8')
cur = db.cursor()

in_path = "G:\五舟汉云\行为感知\接口设计\国家经纬度.txt"

upath = str(in_path, "utf8")

fopen = open(upath)

lines = fopen.readlines()

for line in lines:
    if line.count('\n') == len(line) or not len(line) or line.isspace():
        continue
    # print line
    lst = line.split(':')
    name = lst[0].replace('"', '').strip()
    geo = lst[1][:-2].strip()
    print(name, geo)
    sql = "UPDATE country_basic SET capital_geo = '" + geo + "' WHERE name = '" + name + "'"
    print(sql)
    try:
        cur.execute(sql)
        db.commit()
    except:
        db.rollback()

db.close()
