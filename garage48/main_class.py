from bs4 import BeautifulSoup
import requests
import json
import os
import pandas as pd
import lxml
import re
import country
import tools
from pathlib import Path
from collections import defaultdict


class EventScrapper:
    def __init__(self, csv_name):
        # add the url below
        self.garage48 = 'http://garage48.org/hackthecrisis/'
        self.helpwithcovid = 'https://helpwithcovid.com/'

        # path to the data folder
        self.data_path = Path(Path(__file__).resolve().parent, "output")

        # dataframe to populate
        self.columns = ['name', 'event_url', 'logo_url', 'summary', 'country_id']
        self.df = pd.DataFrame(columns=self.columns)

        #csv filename
        self.csv_name = csv_name


    def scrape_garage48(self):
        '''
        Scrape event from garage48
        '''
        soup = self.get_soup(self.garage48)
        events = soup.findAll('div', {"class": "gr-event"})
        for event in events:
            data = defaultdict(str)
            infolist = event.findAll('div', 'gr-flex')
            data['name'] = str.strip(event.find('h4', {"class": "gr-event__title"}).text)
            data['event_url'] = event.find('a').get('href')
            logo_url = event.find('div', {"class": "gr-event__image"})
            data['logo_url'] = logo_url.get('data-bg') if logo_url else ''
            country_name = infolist[1].find('strong').text if infolist else ''
            data['summary'] = self.get_summary(data['event_url'])
            data['country_id'] = country.match_country_id(country_name)
            self.df = self.df.append(data, ignore_index=True)

    def scrape_helpwithcovid(self):
        soup = self.get_soup(self.helpwithcovid)
        # print(soup)
        events = soup.findAll('li', {"class": "border-t border-gray-200"})
        for event in events:
            data = defaultdict(str)
            data['name'] = event.find('a').text
            data['event_url'] = event.find('a').get('href')
            data['logo_url'] = ''
            country_name = 'usa'
            data['country_id'] = country.match_country_id(country_name)
            data['summary'] = '\n'.join([e.text for e in event.findAll('p')])
            self.df = self.df.append(data, ignore_index=True)


    def get_summary(self, url):
        '''
        extract all texts from a given url
        '''
        if url[:4] == 'http':
            soup = self.get_soup(url)
            [s.extract() for s in soup(['style', 'script', '[document]', 'head', 'title'])]
            return re.sub(r'(\n\s*)+\n+', '\n\n', soup.getText())
        return ""

    def get_soup(self, url):
        try:
            page = requests.get(url)
        except ConnectionError:
            page = ""
        contents = page.content
        return BeautifulSoup(contents, 'lxml')

    def save_csv(self, name):
        self.df.to_csv(os.path.join(self.data_path, name))

    def run(self):
        self.scrape_garage48()
        self.scrape_helpwithcovid()
        self.save_csv(self.csv_name)


if __name__=='__main__':
    csv_name = 'events.csv'
    scrapper = EventScrapper(csv_name)
    scrapper.run()
