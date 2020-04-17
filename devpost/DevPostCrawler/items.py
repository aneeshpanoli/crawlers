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
    hackathons = scrapy.Field()         # array
    url = scrapy.Field()
    category = scrapy.Field()
    image = scrapy.Field()              # URL
    video = scrapy.Field()              # URL
    storyText = scrapy.Field()          # in english
    storyTextOriginal = scrapy.Field()  # not translated
    keywords = scrapy.Field()           # array (extracted by spacey) in english
    links = scrapy.Field()              # array (combines story links plus app links)
    nrLikes = scrapy.Field()            # int
    nrComments = scrapy.Field()         # int
    nrUpdates = scrapy.Field()          # int
    nrHighlights = scrapy.Field()       # int
    lastUpdatedAt = scrapy.Field()      # Date
    teamMembers = scrapy.Field()        # array
    builtWith = scrapy.Field()          # array
    language = scrapy.Field()           # added by pipeline, detected from storyText
    scrapedAt = scrapy.Field()          # Date
