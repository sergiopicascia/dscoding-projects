import pandas as pd

class DataProcessor:
    @staticmethod
    def change_latitude(value):
        if 'N' in value:
            return float(value.replace('N', ''))
        elif 'S' in value:
            return -float(value.replace('S', ''))
        return float(value)

    @staticmethod
    def change_longitude(value):
        if 'E' in value:
            return float(value.replace('E', ''))
        elif 'W' in value:
            return -float(value.replace('W', ''))
        return float(value)

    def __init__(self, folder_path):
        self.folder_path = folder_path

    def _read_data(self, file_path):
        return pd.read_csv(file_path)

    def _clean_data(self, data, has_coordinates=True):
        data['dt'] = pd.to_datetime(data['dt'], format='%Y-%m-%d')
        
        if has_coordinates:
            data['Latitude'] = data['Latitude'].apply(self.change_latitude)
            data['Longitude'] = data['Longitude'].apply(self.change_longitude)
        
        return data

    def load_city_data(self):
        city_path = f"{self.folder_path}/data/GlobalLandTemperaturesByCity.csv"
        city_data = self._read_data(city_path)
        return self._clean_data(city_data)

    def load_country_data(self):
        country_path = f"{self.folder_path}/data/GlobalLandTemperaturesByCountry.csv"
        country_data = self._read_data(country_path)
        return self._clean_data(country_data, has_coordinates=False)

    def load_majorcity_data(self):
        major_path = f"{self.folder_path}/data/GlobalLandTemperaturesByMajorCity.csv"
        major_data = self._read_data(major_path)
        return self._clean_data(major_data)

    def load_state_data(self):
        state_path = f"{self.folder_path}/data/GlobalLandTemperaturesByState.csv"
        state_data = self._read_data(state_path)
        return self._clean_data(state_data, has_coordinates=False)




class GetDataInfo:
    def __init__(self, city, country, major, state, folder_path):
        self.city = city
        self.country = country
        self.major = major
        self.state = state
        self.folder_path = folder_path

    def split_dataframes_by_country(self, data, country_column='Country'):
        return [data[data[country_column] == country] for country in data[country_column].unique()]

    def get_country_info(self, data, dataframes_per_country, city_column='City'):
        informazioni_paesi = []

        for country_df, country_name in zip(dataframes_per_country, data['Country'].unique()):
            numerosita_dataframe = len(country_df)
            valori_mancanti = country_df.isna().sum().sum()
            percentuale_valori_mancanti = (valori_mancanti / numerosita_dataframe) * 100
            numero_citta = country_df[city_column].nunique() if city_column in country_df.columns else None

            informazioni_paese = {
                'Paese': country_name,
                'Numerosità': numerosita_dataframe,
                'Valori Mancanti': valori_mancanti,
                'Percentuale Valori Mancanti': percentuale_valori_mancanti,
                'Numero di Città': numero_citta
            }
            informazioni_paesi.append(informazioni_paese)

        return pd.DataFrame(informazioni_paesi)

    def save_country_info_to_csv(self, info_country, file_path):
        info_country.to_csv(file_path, index=False)

    def process_and_save_info(self):
        for data_type in ['city', 'country', 'major', 'state']:
            data = getattr(self, data_type)
            df_per_country = self.split_dataframes_by_country(data)
            info_country = self.get_country_info(data, df_per_country, city_column='City' if data_type == 'major' else None)
            file_path = f"{self.folder_path}/data/InfoCountry_{data_type}.csv"
            self.save_country_info_to_csv(info_country, file_path)

