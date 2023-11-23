# Import necessary libraries
import os
import pandas as pd
import numpy as np

# Define a class for processing ETF data
class ETFProcessor:
    def __init__(self, folder_path):
        self.folder_path = folder_path

    def daily_return_calculation(self):
        # Loop through all files in the specified folder
        for filename in os.listdir(self.folder_path):
            # Check if the file has a '.csv' extension
            if filename.endswith(".csv"):
                # Construct the full file path
                file_path = os.path.join(self.folder_path, filename)
                # Read the ETF data from the CSV file into a Pandas DataFrame
                df = pd.read_csv(file_path)

                # Calculate the 'daily_return' column and multiply by 100
                df['daily_return'] = (df['Adj Close'].shift(0) / df['Adj Close'].shift(1) - 1) * 100

                # Save the updated DataFrame back to the CSV file without including the index
                df.to_csv(file_path, index=False)

    def calculate_monthly_mean(self):
        # Loop through all files in the specified folder
        for filename in os.listdir(self.folder_path):
            # Check if the file has a '.csv' extension
            if filename.endswith(".csv"):
                # Construct the full file path
                file_path = os.path.join(self.folder_path, filename)
                # Read the ETF data from the CSV file into a Pandas DataFrame
                df = pd.read_csv(file_path)

                # Convert the 'Date' column to datetime format
                df['Date'] = pd.to_datetime(df['Date'])

                # Calculate the monthly average of daily returns for each month
                monthly_mean = df.groupby(df['Date'].dt.to_period('M'))['daily_return'].mean()

                # Create a new 'monthly_mean' column in the original DataFrame and assign the monthly average values
                df['monthly_mean'] = df['Date'].dt.to_period('M').map(monthly_mean)

                # Save the modified DataFrame back to the original CSV file
                df.to_csv(file_path, index=False)

    def calculate_rmse(self):
        # Loop through all files in the specified folder
        for filename in os.listdir(self.folder_path):
            # Check if the file has a '.csv' extension
            if filename.endswith(".csv"):
                # Construct the full file path
                file_path = os.path.join(self.folder_path, filename)
                # Read the ETF data from the CSV file into a Pandas DataFrame
                df = pd.read_csv(file_path)

                # Convert the 'Date' column to datetime format
                df['Date'] = pd.to_datetime(df['Date'])

                # Group the data by month
                monthly_group = df.groupby(df['Date'].dt.to_period("M"))

                # Calculate the Root Mean Squared Error (RMSE) for each month and add the 'RMSE' column
                for month_name, month_data in monthly_group:
                    rmse_month = np.sqrt(np.mean((month_data['daily_return'] - month_data['monthly_mean'])**2))
                    df.loc[df['Date'].dt.to_period("M") == month_name, 'RMSE'] = rmse_month

                # Save the updated DataFrame back to the CSV file
                df.to_csv(file_path, index=False)

    def calculate_volume_monthly_mean(self):
        # Loop through all files in the specified folder
        for filename in os.listdir(self.folder_path):
            # Check if the file has a '.csv' extension
            if filename.endswith(".csv"):
                # Construct the full file path
                file_path = os.path.join(self.folder_path, filename)
                # Read the ETF data from the CSV file into a Pandas DataFrame
                df = pd.read_csv(file_path)

                # Convert the 'Date' column to datetime format
                df['Date'] = pd.to_datetime(df['Date'])

                # Calculate the monthly average of daily volume for each month
                vol_monthly_mean = df.groupby(df['Date'].dt.to_period('M'))['Volume'].mean()

                # Create a new 'Vol_month_mean' column in the original DataFrame and assign the monthly average values
                df['Vol_month_mean'] = df['Date'].dt.to_period('M').map(vol_monthly_mean)

                # Save the modified DataFrame back to the original CSV file
                df.to_csv(file_path, index=False)


# Example of using the ETFProcessor class
if __name__ == "__main__":
    # Replace 'path_della_tua_cartella' with the actual path to your 'etfs' folder
    processor = ETFProcessor('C:\\Users\\stebr\\DireDSCoding\\dscoding-projects\\stefano.bruschi\\Data\\etfs')
    # Call the methods to process the ETF data
    processor.daily_return_calculation()
    processor.calculate_monthly_mean()
    processor.calculate_rmse()
    processor.calculate_volume_monthly_mean()


# Define a class for processing stock data
class STOCKProcessor:
    def __init__(self, folder_path):
        self.folder_path = folder_path

    def daily_return_calculation(self):
        # Loop through all files in the specified folder
        for filename in os.listdir(self.folder_path):
            # Check if the file has a '.csv' extension
            if filename.endswith(".csv"):
                # Construct the full file path
                file_path = os.path.join(self.folder_path, filename)
                # Read the stock data from the CSV file into a Pandas DataFrame
                df = pd.read_csv(file_path)

                # Calculate the 'daily_return' column and multiply by 100
                df['daily_return'] = (df['Adj Close'].shift(0) / df['Adj Close'].shift(1) - 1) * 100

                # Save the updated DataFrame back to the CSV file without including the index
                df.to_csv(file_path, index=False)

    def calculate_monthly_mean(self):
        # Loop through all files in the specified folder
        for filename in os.listdir(self.folder_path):
            # Check if the file has a '.csv' extension
            if filename.endswith(".csv"):
                # Construct the full file path
                file_path = os.path.join(self.folder_path, filename)
                # Read the stock data from the CSV file into a Pandas DataFrame
                df = pd.read_csv(file_path)

                # Convert the 'Date' column to datetime format
                df['Date'] = pd.to_datetime(df['Date'])

                # Calculate the monthly average of daily returns for each month
                monthly_mean = df.groupby(df['Date'].dt.to_period('M'))['daily_return'].mean()

                # Create a new 'monthly_mean' column in the original DataFrame and assign the monthly average values
                df['monthly_mean'] = df['Date'].dt.to_period('M').map(monthly_mean)

                # Save the modified DataFrame back to the original CSV file without including the index
                df.to_csv(file_path, index=False)

    def calculate_rmse(self):
        # Loop through all files in the specified folder
        for filename in os.listdir(self.folder_path):
            # Check if the file has a '.csv' extension
            if filename.endswith(".csv"):
                # Construct the full file path
                file_path = os.path.join(self.folder_path, filename)
                # Read the stock data from the CSV file into a Pandas DataFrame
                df = pd.read_csv(file_path)

                # Convert the 'Date' column to datetime format
                df['Date'] = pd.to_datetime(df['Date'])

                # Group the data by month
                monthly_group = df.groupby(df['Date'].dt.to_period("M"))

                # Calculate the Root Mean Squared Error (RMSE) for each month and add the 'RMSE' column
                for month_name, month_data in monthly_group:
                    rmse_month = np.sqrt(np.mean((month_data['daily_return'] - month_data['monthly_mean'])**2))
                    df.loc[df['Date'].dt.to_period("M") == month_name, 'RMSE'] = rmse_month

                # Save the updated DataFrame back to the CSV file without including the index
                df.to_csv(file_path, index=False)

    def calculate_volume_monthly_mean(self):
        # Loop through all files in the specified folder
        for filename in os.listdir(self.folder_path):
            # Check if the file has a '.csv' extension
            if filename.endswith(".csv"):
                # Construct the full file path
                file_path = os.path.join(self.folder_path, filename)
                # Read the stock data from the CSV file into a Pandas DataFrame
                df = pd.read_csv(file_path)

                # Convert the 'Date' column to datetime format
                df['Date'] = pd.to_datetime(df['Date'])

                # Calculate the monthly average of daily volume for each month
                vol_monthly_mean = df.groupby(df['Date'].dt.to_period('M'))['Volume'].mean()

                # Create a new 'Vol_month_mean' column in the original DataFrame and assign the monthly average values
                df['Vol_month_mean'] = df['Date'].dt.to_period('M').map(vol_monthly_mean)

                # Save the modified DataFrame back to the original CSV file without including the index
                df.to_csv(file_path, index=False)


# Example of using the STOCKProcessor class
if __name__ == "__main__":
    # Replace 'path_della_tua_cartella' with the actual path to your 'stocks' folder
    processor = STOCKProcessor('C:\\Users\\stebr\\DireDSCoding\\dscoding-projects\\stefano.bruschi\\Data\\stocks')
    # Call the methods to process the stock data
    processor.daily_return_calculation()
    processor.calculate_monthly_mean()
    processor.calculate_rmse()
    processor.calculate_volume_monthly_mean()
