
'''
A Scrapy spider class to crawl and extract social hackathon projects from helpwithcovid.com written for ccivictechhub.org
'''
__author__= "Aneesh Panoli"


import scrapy
from twisted.internet import reactor, defer
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from collections import defaultdict
import pandas as pd
from pathlib import Path
import os
import re

class EventsSpider(scrapy.Spider):
    name = 'events'
    start_urls = []

    # 15 pages of projects
    for i in range(1, 16):
        start_urls.append('https://helpwithcovid.com/projects/p/{}'.format(i))

    def __init__(self):
        self.data = defaultdict(list)
        # path to the data folder
        self.data_path = Path(Path(__file__).resolve().parent, "csv")

    def parse(self, response):
        self.helpwithcovid(response)
        df = pd.DataFrame.from_dict(self.data, orient='index')
        df.transpose().to_csv(os.path.join(self.data_path, 'helpwithcovid.csv'), header=True, index=False)


    def helpwithcovid(self, response):
        helpwithcovid_pattern = {
            'GroupName':'//div[@class="text-sm leading-5 font-medium text-indigo-600 truncate"]/a/text()',
            'Resources':'//div[@class="text-sm leading-5 font-medium text-indigo-600 truncate"]/a/@href',
            'CountryName':'//div[@class="mt-2 flex items-center text-sm leading-5 text-gray-500 sm:mt-0"]/text()[2]',
            'Summary':'//div[@class="text-sm leading-5 text-gray-500"]/p[1]/text()[1]',
            'ImageUrl':'//div[@class="noimageshere"]'
        }
        for key, value in helpwithcovid_pattern.items():
            parsed = response.xpath(value).extract()
            if key == 'Resources':
                parsed = ['https://helpwithcovid.com'+i for i in parsed]
            self.data[key].extend(parsed)


class DemoContactSpider(scrapy.Spider):

    name = 'democontact'
    start_urls = pd.read_csv(os.path.join(Path(Path(__file__).resolve().parent, "csv"), 'helpwithcovid.csv'))['Resources'].tolist()
    # start_urls = ['https://helpwithcovid.com/projects/309-gift-card-bank']

    def __init__(self):
        self.df = pd.read_csv(os.path.join(Path(Path(__file__).resolve().parent, "csv"), 'helpwithcovid.csv'))

        self.data = []
        # self.text_list = []
        self.data_path = Path(Path(__file__).resolve().parent, "csv")

    def parse(self, response):
        self.democontact(response)
        # print(len(self.data), len(self.df))
        if len(self.data) == len(self.df):
            # df_text = pd.DataFrame()
            # df_text['text'] = self.text_list
            # df_text.to_csv('text.csv', header=True, index=False)
            self.df['Resources'] = self.data
            self.df.to_csv(os.path.join(self.data_path, 'helpwithcovid_clean.csv'), header=True, index=False)
            print("******helpwithcovid_clean.csv has been saved to {}!".format(self.data_path))

    def democontact(self, response):

        text_links = self.link_from_text(', '.join([i for i in response.xpath("//dl//text()").extract() if i]))
        self.data.append('|||'.join([i for i in [text_links, response.url] if i]))

    def link_from_text(self, text):
        # self.text_list.append(text)
        urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', text)
        emails = re.findall('[\w\.-]+@[\w\.-]+', text)
        return '|||'.join([i.strip(',') for i in urls+emails if i])

@defer.inlineCallbacks
def crawl(spyder):
    yield spyder.crawl(EventsSpider)
    yield spyder.crawl(DemoContactSpider)
    reactor.stop()


if __name__ == '__main__':
    configure_logging()
    spyder = CrawlerRunner()
    crawl(spyder)
    reactor.run()
