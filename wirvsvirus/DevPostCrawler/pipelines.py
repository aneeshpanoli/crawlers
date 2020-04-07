# -*- coding: utf-8 -*-

# Pipeline has to be added to ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import json
import spacy
from collections import Counter


class DevPostCrawlerPipeline(object):

    def __init__(self):
        self.file = open('items.jl', 'w')
        self.nlp = spacy.load("en_core_web_sm")

    def open_spider(self, spider):
        pass

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        key_words = []
        text = item['storyText'][0].rstrip()
        doc = self.nlp(text)
        for chunk in doc.noun_chunks:
            key_words.append(chunk.root.text)
        dict_item = dict(item)
        dict_item['popular_word'] = [a.title() for a, _
                                     in Counter(key_words).most_common(3)]
        line = json.dumps(dict_item) + "\n"
        self.file.write(line)
        return item
