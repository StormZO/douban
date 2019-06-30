# -*- coding: utf-8 -*-
import scrapy
from douban.items import DoubanItem
from copy import deepcopy
from scrapy_redis.spiders import RedisSpider

class DbBookSpider(RedisSpider):
    name = 'db_book'
    allowed_domains = ['douban.com']
    #start_urls = ['https://book.douban.com/tag/?view=type&icn=index-sorttags-hot']
    redis_key = 'douban:start_urls'

    def parse(self, response):
        div_list = response.xpath("//div[@class='article']/div[2]/div")
        item = DoubanItem()
        for div in div_list:
            item['book_bag_class'] = div.xpath("./a/@name").extract_first()
            books_urls = ['https://book.douban.com' + i for i in  div.xpath(".//td/a/@href").extract()]
            books_class= div.xpath(".//td/a/text()").extract()
            for url, book_class in zip(books_urls,books_class):
                item['book_class']= book_class
                yield scrapy.Request(url=url, callback=self.parse_1, meta={'item':deepcopy(item)})

    def parse_1(self, response):
        item = response.meta['item']
        li_list = response.xpath("//*[@id='subject_list']/ul/li")
        # 翻页
        next_url = response.xpath("//span[@class='next']/a/@href").extract_first()
        if len(li_list)+1 > 20 :
            next_url = 'https://book.douban.com' + str(next_url)
            print(next_url)
            yield scrapy.Request(url=next_url, callback=self.parse_1, meta={'item': item})
        # 提取数据
        for li in li_list:
            item['book_name'] = li.xpath("./div[2]/h2/a/@title").extract_first()
            text = li.xpath(".//div[@class='pub']/text()").extract_first()
            text = text.strip().replace(' ','').split('/')
            for i in text:
                if '出版'in i:
                    item['publish_house'] = i
                elif '-'in i :
                    item['time'] = i
                elif '.00'or'元'in i:
                    item['pirce'] = i
                else:
                    item['author'] = i
            item['grade'] = li.xpath(".//*[@class='rating_nums']/text()").extract_first()
            people = li.xpath(".//*[@class='pl']/text()").extract()
            item['people'] = people[0].strip().replace('(','').replace(')','')
            item['intro'] = ''.join([i.replace('\n','')for i in li.xpath(".//p/text()").extract()])
            item['book_href'] = li.xpath(".//*[@class='nbg']/@href").extract_first()
            yield item




