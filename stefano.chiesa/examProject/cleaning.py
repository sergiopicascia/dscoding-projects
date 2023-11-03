import pandas as pd
import functions as fun

# import the data
tem_dataframe = pd.read_csv('venv/data/data_cities.csv', sep=',')

# cleaning the data
tfp_dataframe = tem_dataframe.drop(['AverageTemperatureUncertainty', 'Country'], axis=1)

# run the functions to change the coordinates data
tfp_dataframe = fun.convert(tfp_dataframe, 'Latitude')
tfp_dataframe = fun.convert(tfp_dataframe, 'Longitude')


# upload the modifications
tfp_dataframe.to_csv('venv/data/data_cities.csv', index=False)