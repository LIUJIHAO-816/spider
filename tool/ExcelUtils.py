# /usr/bin/python
# -*- coding: utf8 -*-

__author__ = 'Liujuhao'

import xlwt
import xlrd
import re
import time


def text_to_excel(in_file, out_file, titles):
    upath = unicode(in_file, "utf-8")
    opath = unicode(out_file, "utf-8")

    fopen = open(upath)

    lines = fopen.readlines()

    file = xlwt.Workbook(encoding="gbk", style_compression=0)

    sheet = file.add_sheet("mydata")

    # 生成标签项
    j = 0
    for title in titles:
        sheet.write(0, j, unicode(title, "utf8"))
        j += 1

    # excel_do(sheet, lines)
    excel_db_ddl(sheet, lines)
    file.save(opath)


def excel_do(sheet, lines):
    # 定义写函数
    i = 1
    for line in lines:
        if not len(line) or line.isspace():
            continue
        str = re.split("\||--", line.strip("\n"))
        str_1 = str[0].split("=")
        print(str_1[0] + " || " + str_1[1] + " || " + str[1])
        sheet.write(i, 0, str_1[0])
        sheet.write(i, 1, str_1[1])
        sheet.write(i, 2, str[1])
        i += 1

        # i = 1
        # for line in lines:
        #     if not len(line) or line.isspace():
        #         continue
        #     str = re.split(",", line)
        #     print(str[0] + " || " + str[1] + " || " + str[2])
        #     sheet.write(i, 0, str[0])
        #     sheet.write(i, 1, str[1])
        #     sheet.write(i, 2, str[2])
        #     i += 1


def excel_db_ddl(sheet, lines):
    i = 0
    for line in lines:
        table = ''
        comment = ''
        if not len(line) or line.isspace():
            continue
        if str(line).find('IF EXISTS') != -1:
            table = re.findall(r'`(.*)`', str(line))[0]
            i += 1
            sheet.write(i, 0, table)
        if str(line).find('COMMENT') == 0:
            comment = re.findall(r'\'(.*)\'', str(line))[0].encode('gbk')
            sheet.write(i, 1, comment)


def main():
    # 输入路径
    in_path = "G:\五舟汉云\大数据组\公积金\开发测试\贯标文档\ddl.sql"
    # 输出路径
    out_path = "G:\五舟汉云\大数据组\公积金\开发测试\贯标文档\ddl_" + str(int(time.time())) + ".xls"
    # Label标签
    titles = ["数据库表名", "描述", "是否是国标表"]

    text_to_excel(in_path, out_path, titles)


if __name__ == '__main__':
    main()
