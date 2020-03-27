import json
from fuzzywuzzy import fuzz
from pathlib import Path
import os

data_folder = Path(Path(__file__).resolve().parent, "references")
file_to_open = data_folder / "country.json"

text = open(file_to_open, 'r').read()
countries = json.loads(text)['RECORDS']


def fuzzy_match(s1, s2):
    ratio = fuzz.ratio(s1, s2)
    if ratio > 95:
        return True
    return False


def match_country_id(name):
    for c in countries:
        if fuzzy_match(name, c['name']):
            return c['id']

