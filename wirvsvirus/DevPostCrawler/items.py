# -*- coding: utf-8 -*-

# The models for scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class DevPostCrawlerItem(scrapy.Item):
    title = scrapy.Field()
    subtitle = scrapy.Field()
    url = scrapy.Field()
    challenge = scrapy.Field()
    image = scrapy.Field()
    video = scrapy.Field()
    storyText = scrapy.Field()
    storyHTML = scrapy.Field()
    nrLikes = scrapy.Field()
    nrComments = scrapy.Field()
    teamMembers = scrapy.Field()
    appLinks = scrapy.Field()
    builtWith = scrapy.Field()
