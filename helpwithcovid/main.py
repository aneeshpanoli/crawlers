
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
from helper import get_country, get_keywords

'''
A spider class to crawl and extract social hackathon projects from helpwithcovid.com written for ccivictechhub.org
'''
class EventsSpider(scrapy.Spider):
    name = 'events'
    start_urls = []
    num_pages = 15
    for i in range(1, num_pages+1):
        start_urls.append('https://helpwithcovid.com/projects/p/{}'.format(i))

    def __init__(self):
        self.data = defaultdict(list)
        self.num_pages = 15
        self.columns = ['Group name', 'Topics', 'Description', 'Featured Image', 'Country','Country_spacy']
        # path to the data folder
        self.data_path = Path(Path(__file__).resolve().parent, "csv")

    def parse(self, response):
        helpwithcovid_pattern = {
            'Resources':'//div[@class="text-sm leading-5 font-medium text-indigo-600 truncate"]/a/@href',
        }
        # extract links for crawling project details page. 
        # These links become input for DemoContactSpider
        for key, value in helpwithcovid_pattern.items():
            parsed = response.xpath(value).extract()
            if key == 'Resources':
                parsed = ['https://helpwithcovid.com'+i for i in parsed]
            self.data[key].extend(parsed)

        self.num_pages -= 1 # track processed links
        # save data once all the pages are crawled
        # !!!!make sure that num_pages == self.num_pages!!!
        if self.num_pages <= 0:
            self.save_data()

    def save_data(self):
        # prevent pandas from creating a series
        # add dummy placeholder column to table
        self.data['dummy'] = [''] * len(self.data['Resources'])
        df = pd.DataFrame.from_dict(self.data)
        df.to_csv(os.path.join(self.data_path, 'helpwithcovid.csv'), header=True, index=False)


class DemoContactSpider(scrapy.Spider):
    name = 'democontact'
    start_urls = pd.read_csv(os.path.join(Path(Path(__file__).resolve().parent, "csv"), 'helpwithcovid.csv'))['Resources'].tolist()
    def __init__(self):
        self.df = pd.read_csv(os.path.join(Path(Path(__file__).resolve().parent, "csv"), 'helpwithcovid.csv'))
        self.data = defaultdict(list)
        self.data_path = Path(Path(__file__).resolve().parent, "csv")

    def parse(self, response):
        full_text = ', '.join([i for i in response.xpath("//dl//text()").extract() if i])
        self.data['Resources'].append('|||'.join([i for i in [self.link_from_text(full_text), response.url] if i]))
        self.data['Country_spacy'].append(get_country(full_text))
        self.data['Description'].append(', '.join([i for i in response.xpath("//div//dt[contains (text(),'Description')]/following-sibling::dd/p/text()").extract() if i]))
        self.data['Topics'].append(', '.join([i.split('=')[1] for i in response.xpath("//div//dt[contains (text(),'Skills needed')]/following-sibling::dd/a/@href").extract() if i]))
        self.data['Group name'].append(response.xpath("//div[@class='ml-4 mt-4']/h3/text()").extract()[0].strip())
        self.data['Country'].append(response.xpath("//div//dt[contains (text(),'Location')]/following-sibling::dd/text()").extract()[0].strip())
        self.data['Featured Image'] = ''
        print('\r Crawled {} out {} urls!'.format(len(self.data['Description']), len(self.df)), end='')

        # save once all the links are processed
        print(len(self.data['Description']), len(self.df))
        if len(self.data['Description']) == len(self.df):
            self.save_data()

    def link_from_text(self, text):
        urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', text)
        emails = re.findall('[\w\.-]+@[\w\.-]+', text)
        return '|||'.join([i.strip(',') for i in urls+emails if i])

    def save_data(self):
        df_n = pd.DataFrame.from_dict(self.data)
        df_n.to_csv(os.path.join(self.data_path, 'helpwithcovid_clean.csv'), header=True, index=False)
        print("******helpwithcovid_clean.csv has been saved to {}!".format(self.data_path))



@defer.inlineCallbacks
def crawl(spyder):
    yield spyder.crawl(EventsSpider)
    yield spyder.crawl(DemoContactSpider)
    reactor.stop()


if __name__ == '__main__':
    configure_logging() # uncomment for scrapy logs
    spyder = CrawlerRunner()
    crawl(spyder)
    reactor.run()
