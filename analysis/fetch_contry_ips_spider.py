# -*- coding: UTF-8 -*-
import urllib3
from bs4 import BeautifulSoup
import pymysql

countrys_url = 'http://ip.bczs.net/countrylist'
base_url = 'http://ip.bczs.net'
headers_config = {
    'Content-Type': 'text/html; charset=utf-8',
    'Content-Encoding': 'gzip'
}
http = urllib3.PoolManager()


def get_country_info():
    r = http.request(
        'GET',
        countrys_url,
        headers=headers_config
    )

    print(r.status)

    soup = BeautifulSoup(r.data.decode('utf-8', 'ignore').replace(u'\xa9', u''), 'lxml')

    tbl_lst1 = soup.select('.ip1')
    tbl_lst2 = soup.select('.ip2')
    tbl_lst = tbl_lst1 + tbl_lst2

    map_lst = list()
    for t in tbl_lst:
        tds = t.find_all('td')
        dct = {'name': tds[1].string, 'nick': tds[2].string, 'url': t.a.get('href')}
        map_lst.append(dct)
    return map_lst


def get_ips_by_country(map_lst):
    db = pymysql.connect("172.20.31.108", "mysql", "mysql", "information", charset='utf8')
    cursor = db.cursor()
    country_search_sql = "SELECT name, id FROM country_basic"
    cursor.execute(country_search_sql)
    results = cursor.fetchall()
    country_dct = dict()
    for row in results:
        country_dct[row[0]] = row[1]
    total = 0
    for d in map_lst:
        name = d['name']
        nick_name = d['nick']
        url = d['url']
        country_id = country_dct.get(name, 0)
        print(name, nick_name, url)
        current_url = base_url + url
        # print current_url
        rs = http.request(
            'GET',
            current_url,
            headers={
                'Content-Type': 'text/html; charset=utf-8',
                'Content-Encoding': 'gzip'
            }
        )
        print(rs.status, name, url)
        soup = BeautifulSoup(rs.data.decode('utf-8', 'ignore').replace(u'\xa9', u''), 'lxml')
        chd_list = soup.tbody.select('tr')
        total_sub = 0
        ip_insert_sql = "INSERT INTO global_ip_country_map (start, end, country_id) VALUES "
        for chd in chd_list:
            start_ip = chd.a.string
            end_ip = chd.find_all('td')[1].string
            sql_append = "(" + "'" + start_ip + "'" + "," + "'" + end_ip + "'" + "," + "'" + str(
                country_id) + "'" + "),"
            ip_insert_sql += sql_append
            total_sub += 1
            # break
        total += total_sub
        print(total)
        ip_insert_sql = ip_insert_sql[0:-1]
        try:
            cursor.execute(ip_insert_sql)
            db.commit()
        except:
            db.rollback()

    print(total)
    db.close()


# 数据库写入国家基本信息的逻辑（只执行一次）
# sql = """INSERT INTO country_basic (name, nick_name) VALUES """
# country_lst = get_country_info()
# for c in country_lst:
#     name = c['name']
#     name_nick = c['nick']
#     sql_append = "(" + "'" + name + "'" + "," + "'" + name_nick + "'" + "),"
#     sql += sql_append
# sql = sql[0:-1]
# print sql

def main():
    country_lst = get_country_info()
    get_ips_by_country(country_lst)


if __name__ == '__main__':
    main()
