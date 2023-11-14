import pandas as pd

# import the data


def convert(db, column):
    if column == 'Latitude':
        for x in range(len(db[column].index)):
            if db.at[x, column][-1] == 'N':
                db.at[x, column] = '+' + db.at[x, column][0:len(db.at[x, column]) - 1]
            elif db.at[x, column][-1] == 'S':
                db.at[x, column] = '-' + db.at[x, column][0:len(db.at[x, column]) - 1]

    elif column == 'Longitude':
        for x in range(len(db[column].index)):
            if db.at[x, column][-1] == 'E':
                db.at[x, column] = '+' + db.at[x, column][0:len(db.at[x, column]) - 1]
            elif db.at[x, column][-1] == 'W':
                db.at[x, column] = '-' + db.at[x, column][0:len(db.at[x, column]) - 1]

    return db


def clean_data(path):
    tem_dataframe = pd.read_csv(path, sep=',')

    # cleaning the data
    tfp_dataframe = tem_dataframe.drop(['AverageTemperatureUncertainty', 'Country'], axis=1)

    # run the functions to change the coordinates data
    tfp_dataframe = convert(tfp_dataframe, 'Latitude')
    tfp_dataframe = convert(tfp_dataframe, 'Longitude')
    # upload the modifications
    tfp_dataframe.to_csv('venv/data/data_cities.csv', index=False)
    return tfp_dataframe


