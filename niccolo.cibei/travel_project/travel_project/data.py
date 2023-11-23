import pycountry_convert as pc
import pandas as pd
import numpy as np


class TravelData:
    def __init__(self, path, admin=True, primary=True, minor=False, num=300):
        """
        Initialize the TravelData class.

        Parameters
        ----------
        path : str
            The file path to the Excel file containing travel data.
        admin : bool, optional
            Whether to include administrative cities (capitals), by default True.
        primary : bool, optional
            Whether to include primary cities, by default True.
        minor : bool, optional
            Whether to include minor cities, by default False.
        num : int, optional
            The number of rows to return from the head of the DataFrame, by default 300.
        """

        self.df = None
        self.path = path
        self.load_data()
        self.add_continent_column()
        self.filter_cities(admin=admin, primary=primary, minor=minor)
        self.drop_last_rows(num=num)

    def load_data(self):
        """
        Load travel data from an Excel file, cleaning and processing it.

        Returns
        -------
        pd.DataFrame
            The cleaned DataFrame with travel data.
        """

        # Columns to drop during data loading
        columns_to_drop = ['city', 'iso3', 'admin_name']

        # Load data from Excel, drop specified columns, and handle missing values
        df_city = pd.read_excel(self.path).drop(columns=columns_to_drop).dropna()

        # Modify 'city_ascii' by combining city name and country
        df_city['city_ascii'] = df_city.apply(lambda row: f"{row['city_ascii']}_{row['iso2']}", axis=1)

        self.df = df_city

    def filter_cities(self, admin=False, primary=False, minor=False):
        """
        Filter the DataFrame based on administrative, primary, and/or minor cities and drop a specific number of
        rows if specified.

        Parameters
        ----------
        admin : bool, optional
            Whether to include administrative cities (capitals), by default False.
        primary : bool, optional
            Whether to include primary cities, by default False.
        minor : bool, optional
            Whether to include minor cities, by default False.
        """
        if not admin and not primary and not minor:
            # If no option is selected, do not filter
            return

        # Create a list of filter conditions
        filter_conditions = []

        if admin:
            # Add condition to include administrative cities
            filter_conditions.append(self.df['capital'] == 'admin')

        if primary:
            # Add condition to include primary cities
            filter_conditions.append(self.df['capital'] == 'primary')

        if minor:
            # Add condition to include minor cities
            filter_conditions.append(self.df['capital'] == 'minor')

        # Combine filter conditions using logical OR
        combined_condition = np.any(filter_conditions, axis=0)

        # Apply the combined condition to the DataFrame
        self.df = self.df[combined_condition]

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

        def country_to_continent(country):
            try:
                if country not in country_continent_mapping:
                    # Get country code and continent code, then convert to continent name
                    alpha2_country = pc.country_name_to_country_alpha2(country)

                    country_continent_code = pc.country_alpha2_to_continent_code(alpha2_country)

                    country_continent_name = pc.convert_continent_code_to_continent_name(country_continent_code)

                    country_continent_mapping[country] = country_continent_name
                else:
                    country_continent_name = country_continent_mapping[country]

            except (KeyError, ValueError):
                country_continent_name = None

            return country_continent_name

        if country_column not in self.df.columns:
            raise KeyError(f"The specified country column '{country_column}' does not exist in the DataFrame.")

        # Apply the country_to_continent function to create a new 'continent' column
        self.df.loc[:, 'continent'] = self.df[country_column].apply(country_to_continent)

    def drop_last_rows(self, num=300):
        """
        Return the first n rows of the DataFrame.

        Parameters
        ----------
        num : int
            The number of rows to return from the head.

        Returns
        -------
        pd.DataFrame
            The DataFrame with the first n rows.
        """
        if num == 0:
            return self.df
        elif len(self.df) < num:
            raise ValueError(f"The DataFrame only has {len(self.df)} rows, which is less than the specified number "
                             f"of rows to return ({num}).")
        else:
            self.df = self.df.head(num)
            return self.df
