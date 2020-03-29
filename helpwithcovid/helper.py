
__author__= 'Aneesh Panoli'


import spacy
from collections import Counter


def get_country(text):
    countries = []
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text)
    for entity in doc.ents:
        if entity.label_ == 'GPE':
            countries.append(entity.text)
    if countries:
        return max(countries, key=countries.count)
    return ''

def get_keywords(text):
    nlp = spacy.load("en_core_web_sm")
    key_words = []
    doc = nlp(text)
    for chunk in doc.noun_chunks:
        key_words.append(chunk.root.text)
    return [a.title() for a, _ in Counter(key_words).most_common(3)]

if __name__ == '__main__':
    t = 'The COVID Tracking Project collects information from 50 US states, \
    the District of Columbia, and 5 other US territories to provide the most\
     comprehensive testing data we can collect for the novel coronavirus, \
     SARS-CoV-2. We currently attempt to include positive and negative results,\
      hospitalizations, and total people tested for each state or district \
      currently reporting that data.'
    # print(extract(t))
    print(get_keywords(t))
