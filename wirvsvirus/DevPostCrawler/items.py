# -*- coding: utf-8 -*-

# The models for scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class DevPostCrawlerItem(scrapy.Item):
    title = scrapy.Field()
    subtitle = scrapy.Field()           # in english
    subtitleOriginal = scrapy.Field()   # not translated
    url = scrapy.Field()
    category = scrapy.Field()
    image = scrapy.Field()
    video = scrapy.Field()
    storyText = scrapy.Field()          # in english
    storyTextOriginal = scrapy.Field()  # not translated
    keywords = scrapy.Field()           # array (extracted by spacey) in english
    links = scrapy.Field()              # array (combines story links plus app links)
    nrLikes = scrapy.Field()            # int
    nrComments = scrapy.Field()         # int
    nrUpdates = scrapy.Field()          # int
    lastUpdatedAt = scrapy.Field()      # Date
    teamMembers = scrapy.Field()        # array
    builtWith = scrapy.Field()          # array
    language = scrapy.Field()           # added by pipeline, detected from storyText
    scrapedAt = scrapy.Field()          # Date
