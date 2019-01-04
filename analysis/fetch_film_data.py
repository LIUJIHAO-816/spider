# -*- coding: UTF-8 -*-
import urllib3
from bs4 import BeautifulSoup

film_url = "http://dianying.nuomi.com/movie/boxoffice"
headers_config = {
    'Content-Type': 'application/json; charset=utf-8',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Content-Encoding': 'gzip',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'
}
data_form = {
    'date': '2019-01-01'
}
http = urllib3.PoolManager()


def get_film_info():
    r = http.request(
        'GET',
        film_url,
        headers=headers_config,
        fields=data_form
    )

    print(r.msg)
    soup = BeautifulSoup(r.data.decode('utf-8', 'ignore'), 'lxml')
    # print(soup.prettify())
    tables = soup.find('dl', {'class': 'movie-table'}).find_all('dd')
    for table in tables:
        # print(table)
        name = table.find('h5', {'class': 'movie-title'}).text
        release_days = table.find('li', {'class': 'days'}).text
        total = table.find('li', {'class': 'totals'}).span.text
        real = table.find('div', {'class': 'column colm-2'}).text
        boxoffice_ratio = table.find('div', {'class': 'column colm-3'}).text
        screen_ratio = table.find('div', {'class': 'column colm-4'}).text
        actul_seat_ratio = table.find('div', {'class': 'column colm-5'}).text
        seat_ratio = table.find('div', {'class': 'column colm-6'}).text
        screen_times = table.find('div', {'class': 'column colm-7'}).text
        person_times = table.find('div', {'class': 'column colm-8'}).text
        person_per_screen = table.find('div', {'class': 'column colm-9'}).text
        boxoffice_per_screen = table.find('div', {'class': 'column colm-10'}).text
        avg_price = table.find('div', {'class': 'column colm-11'}).text
        lst = [name, release_days, total, real, boxoffice_ratio, screen_ratio, actul_seat_ratio, seat_ratio,
               screen_times, person_times, person_per_screen, boxoffice_per_screen, avg_price]
        result = ','.join(lst)
        print(result)


def test():
    headers_config = {
        'Content-Type': 'application/json; charset=utf-8',
        'Accept': 'application/json, text/plain, */*',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36',
        'Origin': 'http://172.20.31.134:59',
        'Referer': 'http://172.20.31.134:59/login'
    }

    r = http.request(
        'POST',
        'http://172.20.31.135:8081/hr/common/login',
        headers=headers_config,
        fields={'username': '030', 'password': '123456'}
    )

    print(r.status)
    soup = BeautifulSoup(r.data.decode('utf-8', 'ignore'), 'lxml')
    print(soup.prettify())


if __name__ == '__main__':
    # get_film_info()
    test()
