# -*- coding: utf-8 -*-

# Pipeline has to be added to ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import json
import logging
from DevPostCrawler.language_processing import LanguageProcessing


class DevPostCrawlerPipeline(object):

    def __init__(self):
        self.file = open('items.jl', 'w')
        self.lp = LanguageProcessing()

    def open_spider(self, spider):
        pass

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):

        story_text = item['storyTextOriginal'][0]
        subtitle = item['subtitleOriginal'][0]

        (score, language) = self.lp.spc_detect_language(story_text)
        item['language'] = language

        # Translate to english if necessary
        logging.debug('Detected language %s with score %.3f', language, score)
        if language == 'english' or language == 'en':  # and score > 0.85:
            item['storyText'] = story_text
        else:
            item['storyText'] = self.lp.ggl_translate(story_text, language)

        (score_st, language_st) = self.lp.spc_detect_language(subtitle)
        if language_st == 'english' or language_st == 'en':  # and score > 0.85:
            item['subtitle'] = subtitle
        else:
            item['subtitle'] = self.lp.ggl_translate(subtitle, language_st)

        # Extract most frequent words
        item['keywords'] = self.lp.get_keywords(item['storyText'])

        # Export to JSON line format
        line = json.dumps(dict(item)) + "\n"
        self.file.write(line)
        return item
