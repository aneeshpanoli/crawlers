
from helper import GoogleTranslate
from airtable import Airtable
import pandas as pd
from helper import AirtableHelper



class AirtableProcessor(AirtableHelper):

    def __init__(self, table_name):
        super().__init__()
        self.run_checks()
        self.is_working_db(table_name)
        self.table = self.fetch_table(table_name)
        self.table_name = table_name

    def run_checks(self):
        response = input('Before proceeding please make sure the columns names of your \
         table matches with the table at https://airtable.com/tblY84n8azSqbpaux/viwvBcBYXVugRIukX?blocks=show. Poceed? (y/n): ')
        if str(response).lower() != 'y':
            raise ValueError("Your reponse was '{}'. Script terminated!".format(response))


    def to_df(self):
        # coverts airtable to pandas dataframe
        print('Processing {}...'.format(self.table_name))
        record_list = self.table.get_all()
        df = pd.DataFrame([record['fields'] for record in record_list])
        df.fillna("", inplace=True)
        return df
    
    def df_to_airtable(self, df):
        # always writes to 'working_table'
        # make sure that your df and the airtable has the same column names
        self.to_airtable(df)
        
    def df_to_csv(self, df, csv_path):
        df.to_csv(csv_path, index=None, header=True)


if __name__ == '__main__':
    air_table = AirtableProcessor('helpwithcovid')
    df = air_table.to_df()
