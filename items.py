# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DoubanItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    book_bag_class = scrapy.Field()     # 大分类
    book_class = scrapy.Field()         # 小分类
    books_urls = scrapy.Field()         # 小分类链接
    book_name = scrapy.Field()          # 书名
    author = scrapy.Field()             # 作者
    publish_house = scrapy.Field()      # 出版社
    time = scrapy.Field()               # 出版时间
    pirce = scrapy.Field()              # 价格
    grade = scrapy.Field()              # 评分
    people = scrapy.Field()             # 参与人数
    intro = scrapy.Field()              # 简介
    book_href = scrapy.Field()          # 图书详情链接

