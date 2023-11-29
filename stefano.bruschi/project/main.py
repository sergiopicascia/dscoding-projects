import os
import pandas as pd
import numpy as np

class DataProcessor:
    def __init__(self, folder_path):
        self.folder_path = folder_path

    def process_file(self, file_path):
        df = pd.read_csv(file_path)
        df['Date'] = pd.to_datetime(df['Date'])
        return df

    def save_to_csv(self, df, file_path):
        df.to_csv(file_path, index=False)

    def calculate_volatility(self, df):
        monthly_group = df.groupby(df['Date'].dt.to_period("M"))
        df['volatility'] = np.nan
        for month_name, month_data in monthly_group:
            volatility_month = np.sqrt(np.mean((month_data['daily_return'] - month_data['monthly_mean'])**2))
            df.loc[df['Date'].dt.to_period("M") == month_name, 'volatility'] = volatility_month
        return df

    def calculate_monthly_mean(self, df, column_name):
        monthly_mean = df.groupby(df['Date'].dt.to_period('M'))[column_name].mean()
        df['monthly_mean'] = df['Date'].dt.to_period('M').map(monthly_mean)
        return df

    def calculate_volume_monthly_mean(self, df):
        vol_monthly_mean = df.groupby(df['Date'].dt.to_period('M'))['Volume'].mean()
        df['Vol_month_mean'] = df['Date'].dt.to_period('M').map(vol_monthly_mean)
        return df

    def process_data(self, column_name):
        for filename in os.listdir(self.folder_path):
            if filename.endswith(".csv"):
                file_path = os.path.join(self.folder_path, filename)
                df = self.process_file(file_path)
                df['daily_return'] = (df['Adj Close'].shift(0) / df['Adj Close'].shift(1) - 1) * 100
                df = self.calculate_monthly_mean(df, 'daily_return')
                df = self.calculate_volatility(df)
                df = self.calculate_volume_monthly_mean(df)
                self.save_to_csv(df, file_path)

class ETFProcessor(DataProcessor):
    def __init__(self, folder_path):
        super().__init__(folder_path)

class STOCKProcessor(DataProcessor):
    def __init__(self, folder_path):
        super().__init__(folder_path)

if __name__ == "__main__":
    # Example usage for ETFProcessor
    etf_processor = ETFProcessor('/Data/etfs')
    etf_processor.process_data('daily_return')

    # Example usage for STOCKProcessor
    stock_processor = STOCKProcessor('/Data/stocks')
    stock_processor.process_data('daily_return')
