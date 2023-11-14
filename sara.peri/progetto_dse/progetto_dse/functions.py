import pandas as pd
import numpy as np


# Converting Latitude 
def change_latitude(value):
    if 'N' in value:
        return float(value.replace('N', ''))
    elif 'S' in value:
        return -float(value.replace('S', ''))
    return float(value)



# Converting Longitude
def change_longitude(value):
    if 'E' in value:
        return float(value.replace('E', ''))
    elif 'W' in value:
        return -float(value.replace('W', ''))
    return float(value)


def calcola_valori_mancanti(dataset):
    valori_mancanti_totali = dataset.isna().sum().sum()
    valori_mancanti_per_colonna = dataset.isna().sum()
    
    print("Totale di valori mancanti nel DataFrame:", valori_mancanti_totali)
    print("Valori mancanti per colonna:")
    print(valori_mancanti_per_colonna)



def split_dataframes_by_country(data, country_column='Country'):
    """
    Split a DataFrame into a list of DataFrames, one for each unique country in the specified column.

    Args:
        data (pd.DataFrame): The DataFrame to split.
        country_column (str): The column containing country information.

    Returns:
        list: A list of DataFrames, one for each unique country.
    """
    unique_countries = data[country_column].unique()
    dataframes_per_country = [data[data[country_column] == country] for country in unique_countries]
    return dataframes_per_country


def get_dataframe_for_country(dataframes_per_country, country_name):
    for df in dataframes_per_country:
        if df['Country'].iloc[0] == country_name:
            return df
    return None




def get_country_info(data, dataframes_per_country, city_column='City'):
    modalita_country = data['Country'].unique().tolist()
    informazioni_paesi = []

    for country_df, country_name in zip(dataframes_per_country, modalita_country):
        numerosita_dataframe = len(country_df)
        valori_mancanti = country_df.isna().sum().sum()
        percentuale_valori_mancanti = (valori_mancanti / numerosita_dataframe) * 100
        
        if city_column in country_df.columns:
            numero_citta = country_df[city_column].nunique()
        else:
            numero_citta = None
        
        informazioni_paese = {
            'Paese': country_name,
            'Numerosità': numerosita_dataframe,
            'Valori Mancanti': valori_mancanti,
            'Percentuale Valori Mancanti': percentuale_valori_mancanti,
            'Numero di Città': numero_citta
        }
        informazioni_paesi.append(informazioni_paese)

    informazioni_paesi = pd.DataFrame(informazioni_paesi)
    return informazioni_paesi