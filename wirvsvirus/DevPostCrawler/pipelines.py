# -*- coding: utf-8 -*-

# Pipeline has to be added to ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import json
import spacy
from collections import Counter
from googletrans import Translator
from googletrans import LANGUAGES


class DevPostCrawlerPipeline(object):

    def __init__(self):
        self.file = open('items.jl', 'w')
        self.nlp = spacy.load("en_core_web_sm")
        self.translator = Translator()

    def open_spider(self, spider):
        pass

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):

        # Extract most frequent words
        key_words = []
        text = item['storyText'][0].rstrip()
        doc = self.nlp(text)
        for chunk in doc.noun_chunks:
            key_words.append(chunk.root.text)
        dict_item = dict(item)
        dict_item['popular_word'] = [a.title() for a, _
                                     in Counter(key_words).most_common(3)]

        # Detect the subtitle language and translate it to english
        a = self.translator.translate(item['subtitle'][0])
        dict_item['language'] = LANGUAGES[a.src]
        if a.src != 'en':
            dict_item['en_subtitle'] = a.text
        else:
            dict_item['en_subtitle'] = ''

        line = json.dumps(dict_item) + "\n"
        self.file.write(line)
        return item
