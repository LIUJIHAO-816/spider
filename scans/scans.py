#/usr/bin/python
#-*- coding: utf8 -*-
__author__ = 'Liujuhao'

from bs4 import BeautifulSoup
import urllib2
import re
import MySQLdb


def get_project_from_website():
    headers = {
    'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'
    }
    req = urllib2.Request(
    url = 'https://scans.io/',
    headers = headers
    )
    res = urllib2.urlopen(req)
    html = res.read()
    soup = BeautifulSoup(html,from_encoding="GBK")
    project_list = soup.find_all("div",class_="panel panel-primary")
    project_dict = {}
    for project in project_list:
        a_text = project.find("a")
        project_name_contents = a_text.contents
        project_name = project_name_contents[0].replace('0xf6','').replace(' ','-')
        value = 'https://scans.io' + a_text['href']
        project_dict[project_name] = value
    return project_dict

def get_details_from_project(project_site):
    headers = {
    'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'
    }
    req = urllib2.Request(
    url = project_site,
    headers = headers
    )
    res = urllib2.urlopen(req)
    html = res.read()
    soup = BeautifulSoup(html)
    avliable = []
    for i in soup.find_all("a"):
        if re.match(r"zgrab-results$|(.+?)\.json$|(.+?)\.tar.xz$|(.+?)\.gz$",i.contents[0]):
            name = i.contents[0]
            href = i['href']
            try:
                time = re.compile(r"-|/(\d{8})").findall(href)[0]
            except(Exception):
                time = 'unknow'
            avliable.append((name,href,time))
    return avliable

def init_mysql():
    conn = MySQLdb.connect(
        host='localhost',
        port = 3306,
        user='root',
        passwd='root',
        db ='test',
    )
    cur = conn.cursor()

    sql = """CREATE TABLE spider (
         id int(11) NOT NULL auto_increment,
         name CHAR(200),
         href CHAR(200),
         time CHAR(10),
         project CHAR(200),
         PRIMARY KEY  (`id`)
          )"""
    cur.execute(sql)
    conn.close()

def insert_into_mysql():
    projects_dict = get_project_from_website()
    for k in projects_dict:
        try:
            print k,projects_dict[k]
            details = get_details_from_project(projects_dict[k])
            details = get_details_from_project('https://scans.io/study/hanno-axfr')
            for de in details:
                print '--->',de[0]
                if k.find(u'枚'):
                    k = k.replace(u'枚','')
                sql = """insert into spider(name,href,time,project) values("%s","%s","%s","%s")""" % (de[0],de[1],de[2],k)
                #print sql
                conn = MySQLdb.connect(
                                        host='localhost',
                                        port = 3306,
                                        user='root',
                                        passwd='root',
                                        db ='test',
                                        )
                cur = conn.cursor()
                cur.execute(sql)
                conn.commit()
                conn.close()
        except(Exception):
            print 'unkown error!'

def main():
    #print get_details_from_project("https://scans.io/series/993-imaps-tls-full_ipv4")
    #get_details_from_project("https://scans.io/study/hanno-axfr")
    #init_mysql()
    insert_into_mysql()

if __name__ == '__main__':
    main()

