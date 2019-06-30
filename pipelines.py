# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from pymongo import MongoClient

class DoubanPipeline(object):
    def __init__(self):
        self.client = MongoClient()     # 创建链接

    def process_item(self, item, spider):
        item = dict(item)
        db = self.client[item['book_bag_class']]
        post = db[item['book_class']]
        post.insert(item)
        return item
