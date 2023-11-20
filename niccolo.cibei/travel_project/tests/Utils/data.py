import pycountry_convert as pc
import pandas as pd


class TravelData:
    def __init__(self, path):
        """
        Initialize the TravelData class.

        Parameters
        ----------
        path : str
            The file path to the Excel file containing travel data.
        """
        self.path = path
        self.df = self.load_data()

    def load_data(self):
        """
        Load travel data from an Excel file, cleaning and processing it.

        Returns
        -------
        pd.DataFrame
            The cleaned DataFrame with travel data.
        """

        columns_to_drop = ['city', 'iso3', 'admin_name']
        df_city = pd.read_excel(self.path).drop(columns=columns_to_drop)
        df_cleaned = df_city.dropna()
        return df_cleaned

    def add_continent_column(self, country_column='country'):
        """
        Add a 'continent' column to the DataFrame based on the 'country' column.

        Parameters
        ----------
        country_column : str, optional
            The name of the column containing country names, by default 'country'.

        Raises
        ------
        KeyError
            If the specified country column does not exist in the DataFrame.
        """
        country_continent_mapping = {}

        def country_to_continent(country_name):
            try:
                if country_name not in country_continent_mapping:
                    country_alpha2 = pc.country_name_to_country_alpha2(country_name)
                    country_continent_code = pc.country_alpha2_to_continent_code(country_alpha2)
                    country_continent_name = pc.convert_continent_code_to_continent_name(country_continent_code)
                    country_continent_mapping[country_name] = country_continent_name
                else:
                    country_continent_name = country_continent_mapping[country_name]

            except (KeyError, ValueError):
                country_continent_name = None

            return country_continent_name

        if country_column not in self.df.columns:
            raise KeyError(f"The specified country column '{country_column}' does not exist in the DataFrame.")

        self.df.loc[:, 'continent'] = self.df[country_column].apply(country_to_continent)

    def get_data(self):
        """
        Get the DataFrame containing travel data.

        Returns
        -------
        pd.DataFrame
            The DataFrame with travel data.
        """
        return self.df
