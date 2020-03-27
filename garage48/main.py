from bs4 import BeautifulSoup as BS
import requests as rq
import json
import lxml

import country
import tools

url = "http://garage48.org/hackthecrisis/"

res = rq.get(url)
soup = BS(res.content, 'lxml')
events = soup.findAll('div', {"class": "gr-event"})

def parse_event(e):
    infolist = e.findAll('div', 'gr-flex')
    title = str.strip(e.find('h4', {"class": "gr-event__title"}).text)
    img = e.find('div', {"class": "gr-event__image"})

    #country name could not be there
    c = infolist[1].find('strong').text if len(infolist)>0 else ''
    country_id = country.match_country_id(c)

    #may not have image
    img_url = tools.parse_bg_image(img['data-bg']) if img else ''
    # det_url = img.find('a')['href']

    data = {
        "name": title,
        "logo_url": img_url,
        "country_id": country_id
    }
    return []
    # return data


l = [parse_event(event) for event in events]
target = json.dumps(l)
with open('output/group_list.json', 'w') as f:
    f.write(target)
