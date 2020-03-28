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


class EventScrapper:
    def __init__(self):
        self.garage48 = 'http://garage48.org/hackthecrisis/'
        self.data_path = data_folder = Path(Path(__file__).resolve().parent, "output")
        # dataframe to populate
        self.columns = ['name', 'event_url', 'logo_url', 'summary', 'country_id']
        self.df = pd.DataFrame(columns=self.columns)


    def scrape_garage48(self):
        soup = self.get_soup(self.garage48)
        events = soup.findAll('div', {"class": "gr-event"})
        for event in events:
            infolist = event.findAll('div', 'gr-flex')
            name = str.strip(event.find('h4', {"class": "gr-event__title"}).text)
            event_url = event.find('a').get('href')
            logo_url = event.find('div', {"class": "gr-event__image"})
            logo_url = logo_url.get('data-bg') if logo_url else ''
            country_name = infolist[1].find('strong').text if infolist else ''
            summary = self.get_summary(event_url)
            country_id = country.match_country_id(country_name)
            # print([name, logo_url, summary, country_id, event_url])
            row = {'name':name, 'event_url':event_url, 'logo_url':logo_url,\
             'summary':summary, 'country_id':country_id}
            self.df = self.df.append(row, ignore_index=True)
        print(self.df.head())

    def get_summary(self, url):
        if url[:4] == 'http':
            soup = self.get_soup(url)
            [s.extract() for s in soup(['style', 'script', '[document]', 'head', 'title'])]
            return re.sub(r'(\n\s*)+\n+', '\n\n', soup.getText())
        return ""

    def get_soup(self, url):
        page = requests.get(self.garage48)
        contents = page.content
        return BeautifulSoup(contents, 'lxml')

    def save_csv(self, name):
        self.df.to_csv(os.path.join(self.data_path, name))


if __name__=='__main__':
    csv_name = 'event.csv'
    scrapper = EventScrapper()
    scrapper.scrape_garage48()
    scrapper.save_csv(csv_name)
