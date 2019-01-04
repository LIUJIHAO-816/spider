# -*- coding: utf-8 -*- 
__author__ = 'Liujuhao'

import scrapy


class QuotesSpider(scrapy.Spider):
    name = "quotes"

    def start_requests(self):
        urls = [
            # 'http://quotes.toscrape.com/page/1/',
            # 'http://quotes.toscrape.com/page/2/',
            'http://172.18.20.162/train/www/bug-browse-43--unclosed-0--80-20-1.html'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        page = response.url.split("/")[-2]
        filename = 'quotes-%s.html' % page
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)