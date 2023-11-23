import pandas as pd
import re

class CISIData:

    #initialize dataset as an attribute
    def __init__(self):
        self.dataset = None
    
    #load dataset from csv file
    def load_data_from_csv(self, file_path):
        import pandas as pd
        self.dataset = pd.read_csv(file_path) 

    #show dataset
    def retrieve_data(self):
        return self.dataset
        
    #show how much rows loadd dataset contains
    def data_info(self):
        return f"Dataset information: {len(self.dataset)} rows loaded"
        
    #panda's head method to show first 5 rows
    def get_head(self, rows = 5):
        return self.dataset.head(rows)
    
    #panda's tail method to show last 5 rows
    def get_tail(self, rows = 5):
        return self.dataset.tail(rows)
    
    #delete all ", id, name and othe non-word characters
    def clean_column(self, column_name):
        self.dataset[column_name] = self.dataset[column_name].apply(lambda x: re.sub(r'\W', '', str(x)))
        self.dataset[column_name] = self.dataset[column_name].apply(lambda x: re.sub(r'\d', '', str(x)))
        self.dataset[column_name] = self.dataset[column_name].apply(lambda x: x.replace('name', ' '))
        self.dataset[column_name] = self.dataset[column_name].apply(lambda x: x.replace('id', ''))
    
    #delete specidied column
    def drop_column(self, column_name):
        self.dataset = self.dataset.drop(column_name, axis = 1)
    
    #show rows that have '0' or 'NaN' as attribute
    def show_incorrect_rows(self, column_name):
        incorrect_rows = self.dataset[(self.dataset[column_name] == 0) | (self.dataset[column_name].isna())]
        return incorrect_rows
        
    #delete rows from dataset that have '0' or 'NaN' as attribute
    def remove_incorrect_rows(self, column_name):
        self.dataset = self.dataset[(self.dataset[column_name] != 0) & (~self.dataset[column_name].isna())]
        return self.dataset
    
    #save modified dataset to new csv file
    def new_csv(self, file_path):
        self.dataset.to_csv(file_path, index = False)
    
    #convert release date from format YYYY-MM-DD to YYYY and convert from 'object' to 'int'
    def clean_and_convert_release_date(self, column_name):
        self.dataset[column_name] = pd.to_datetime(self.dataset[column_name]).dt.year.astype(int)
    
    #duplicates column of a datset
    def duplicate_column(self, column_name):
        self.dataset[f'{column_name}_duplicate'] = self.dataset[column_name]
    
    #shows type of column of dataset
    def get_type(self):
        return self.dataset.dtypes