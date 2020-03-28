import scrapy
from scrapy.crawler import CrawlerProcess
from collections import defaultdict
import pandas as pd
import country
import tools
from pathlib import Path
import os

class EventsSpider(scrapy.Spider):
    name = 'events'
    start_urls = []

    # 12 pages of projects
    for i in range(1, 16):
        start_urls.append('https://helpwithcovid.com/projects/p/{}'.format(i))

    def __init__(self):
        self.data = defaultdict(list)
        # path to the data folder
        self.data_path = Path(Path(__file__).resolve().parent, "output")

    def parse(self, response):
        if 'helpwithcovid' in response.url:
            self.helpwithcovid(response)
        df = pd.DataFrame.from_dict(self.data, orient='index')
        df.transpose().to_csv(os.path.join(self.data_path, 'helpwithcovid_events.csv'))

    def helpwithcovid(self, response):
        helpwithcovid_pattern = {
            'names':'//div[@class="text-sm leading-5 font-medium text-indigo-600 truncate"]/a/text()',
            'elinks':'//div[@class="text-sm leading-5 font-medium text-indigo-600 truncate"]/a/@href',
            'country_id':'//div[@class="mt-2 flex items-center text-sm leading-5 text-gray-500 sm:mt-0"]/text()',
            'summary':'//div[@class="text-sm leading-5 text-gray-500"]/p/text()',
            'image':'//div[@class="noimageshere"]'
        }
        for key, value in helpwithcovid_pattern.items():
            parsed = response.xpath(value).extract()
            if key == 'elinks':
                parsed = ['https://helpwithcovid.com'+i for i in parsed]
            elif key == 'country_id':
                parsed = [i.rstrip() for i in parsed]
            self.data[key].extend(parsed)

if __name__ == '__main__':
    spyder = CrawlerProcess({
        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
    })
    spyder.crawl(EventsSpider)
    spyder.start()
