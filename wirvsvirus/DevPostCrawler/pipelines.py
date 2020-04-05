# -*- coding: utf-8 -*-

# Pipeline has to be added to ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import json


class DevPostCrawlerPipeline(object):

    def __init__(self):
        self.file = open('items.jl', 'w')

    def open_spider(self, spider):
        pass

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        line = json.dumps(dict(item)) + "\n"
        self.file.write(line)
        return item
