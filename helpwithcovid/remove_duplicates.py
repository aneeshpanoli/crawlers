
__author__ = 'Aneesh Panoli'

from airtable import Airtable
import pandas as pd
from pathlib import Path
import os


class RemoveDuplicates:
    '''
    compares are given csv to airtable main database and
    removes duplicates.
    The script will compare 'Group name' and 'Resources' colums for similarities
    '''
    def __init__(self, csv_name):
        self.api_key = 'keyVuEhB1SvC5cDQj'
        self.base_key = 'app4FKBWUILUmUsE1'
        self.main_table_name = 'Groups' # primary database
        self.main_airtable = None
        self.data_path = Path(Path(__file__).resolve().parent, "csv")
        self.csv_name  = csv_name
        # check if the input table is main_table. if it is exit the script
        # self._is_main_db() # <---*****be careful removing this line****
        self.fetch_tables()

    def _is_main_db(self):
        '''
        Protects the maind db from accidental editing
        '''
        try:
            assert self.in_table_name != self.main_table_name
        except AssertionError as e:
            e.args += ("You're Trying to modify the main database! This is dangerous! Terminated!",)
            raise

    def fetch_tables(self):
        self.main_airtable = Airtable(self.base_key, self.main_table_name, api_key=self.api_key)

    def delete_dupes(self):
        df = pd.read_csv(os.path.join(self.data_path, self.csv_name))
        len_begin = len(df)
        records_to_delete = []
        for page in self.main_airtable.get_iter():
            for record in page:
                url_ids = record['fields'].get('Resources')
                grp_name = record['fields'].get('Group name')
                if url_ids:
                    for url in [self.main_airtable.get(i) for i in url_ids  if i]:
                        df = df[~df['Resources'].str.contains(url['fields'].get('Url'))]
                        df = df[~df['Group name'].str.contains(grp_name)]
        df.to_csv(os.path.join(self.data_path, 'helpwithcovid_clean_no_dupe.csv'), header=True, index=False)
        print('Removed {} duplicate entriies and saved helpwithcovid_clean_no_dupe.csv in {}!'.format((len_begin-len(df)), self.data_path))


if __name__ == '__main__':
    table = 'helpwithcovid_clean.csv'
    data = RemoveDuplicates(table)
    data.delete_dupes()
