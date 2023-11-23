import streamlit as st
import os
import pandas as pd
import plotly.express as px

# Function to load data based on selected files and year
def load_data(selected_files, selected_folder_path, selected_year):
    data = pd.DataFrame()

    for file in selected_files:
        file_path = os.path.join(selected_folder_path, file)
        df = pd.read_csv(file_path)
        df['Date'] = pd.to_datetime(df['Date'])
        df = df.set_index('Date')
        df['File'] = file  # Add 'File' column with the file name
        df = df.loc[f'{selected_year[0]}-01-01':f'{selected_year[1]}-12-31']

        data = pd.concat([data, df])

    return data

# Function to calculate monthly mean for each column and file
def calculate_monthly_mean(data):
    return data.groupby(['File', pd.Grouper(freq='M')]).mean().reset_index()

# Function to get the file description
def get_file_description(selected_file, symbols_meta_df):
    file_name = os.path.splitext(selected_file)[0]  # Extract file name (without extension)
    description_row = symbols_meta_df[symbols_meta_df['NASDAQ Symbol'] == file_name]  # Find corresponding row in 'symbols_valid_meta.csv'

    if not description_row.empty:
        return description_row['Security Name'].values[0]  # Return description from the 'Security Name' column
    else:
        return "Description not available"

# Path to the "Data" folder
data_folder = "C:\\Users\\stebr\\DireDSCoding\\dscoding-projects\\stefano.bruschi\\Data"

# Load the 'symbols_valid_meta.csv' file
symbols_meta_path = "../symbols_valid_meta.csv"
symbols_meta_df = pd.read_csv(symbols_meta_path)

# List of subfolders within "Data"
subfolders = [f.name for f in os.scandir(data_folder) if f.is_dir()]

# Add a title
st.title("Explore the Financial Markets")

# Add a brief description
st.markdown("This dashboard provides a visual analysis of financial data and the possibility to compare them mutually. It includes the most used economic metrics such as returns, volatility, and volume")

# Select the folder
selected_folder = st.radio("Select a financial instrument", subfolders)

# Full path of the selected folder
selected_folder_path = os.path.join(data_folder, selected_folder)

# List of files in the selected folder
files = [f.name for f in os.scandir(selected_folder_path) if f.is_file()]

# Multi-selection of files
selected_files = st.multiselect("Select asset/s", files)

# Get file descriptions
file_descriptions = [get_file_description(file, symbols_meta_df) for file in selected_files]

# Display descriptions of selected files with file names
st.write("Asset/s Description:")
for filename, description in zip(selected_files, file_descriptions):
    st.write(f"Asset Name: {filename}")
    st.write(f"Description: {description}")
    st.write("---")  # Add a dividing line between file descriptions for better readability

# Selector for the chart type
chart_type = st.selectbox("Choose your analysis", ["Returns", "Returns and Volatility", "Volume", "Volatility", "Return and Volume"])

# Yearly time frame selector
start_year = 2013
end_year = 2023
selected_year = st.slider("", start_year, end_year, (start_year, end_year), step=1)

# Load the data
data = load_data(selected_files, selected_folder_path, selected_year)

# Calculate monthly mean
monthly_data = calculate_monthly_mean(data)

# Generate and display the chart based on the selection
if chart_type == "Returns":
    fig = px.line(monthly_data, x='Date', y='monthly_mean', color='File', title='Returns')
    fig.update_xaxes(title_text='Date')
    fig.update_yaxes(title_text='return per month')
    st.plotly_chart(fig)
elif chart_type == "Returns and Volatility":
    fig = px.scatter(monthly_data, x='monthly_mean', y='volatility', color='File', title='Returns and Volatility')
    fig.update_xaxes(title_text='return per month')
    fig.update_yaxes(title_text='Volatility (%)')
    st.plotly_chart(fig)
elif chart_type == "Volatility":
    fig = px.area(monthly_data, x='Date', y='volatility', color='File', title='Volatility')
    fig.update_xaxes(title_text='Date')
    fig.update_yaxes(title_text='Volatility (%)')
    st.plotly_chart(fig)
elif chart_type == "Volume":
    fig = px.bar(monthly_data, x='Date', y='Vol_month_mean', color='File', title='Volume')
    fig.update_xaxes(title_text='Date')
    fig.update_yaxes(title_text='volume per month')
    st.plotly_chart(fig)
elif chart_type == "Return and Volume":
    fig = px.scatter(monthly_data, x='Vol_month_mean', y='monthly_mean', color='File', labels={'monthly_mean': 'Return per month', 'Vol_month_mean': 'Volume'}, title='Return and Volume Analysis')
    fig.update_xaxes(title_text='Volume')
    fig.update_yaxes(title_text='Return per month')
    st.plotly_chart(fig)

# Display comments based on the chart type selection
if chart_type == "Returns":
    st.write("AVARAGE RETURN")
    st.write("The average return is the mean of observed returns on a financial asset over a specific period of time. It is a useful indicator as it provides an overall view of performance over time.")
    st.write("  - An investor can use the average return to assess the potential profitability of an investment")
elif chart_type == "Returns and Volatility":
    st.write("RETURNS AND VOLATILITY")
    st.write("The relationship between returns and volatility can take various forms:")
    st.write("- Positive correlation: Periods of high returns may coincide with periods of high volatility, and vice versa. This could indicate that when the market is more active, there are greater opportunities for both gains and losses")
    st.write("- Negative correlation: If returns are higher during periods of low volatility and vice versa, it might suggest that there are periods of calm where investments tend to perform better")
    st.write("      - This visualization helps investors assess the consistency of performance and understand how risk may vary over time")
elif chart_type == "Volatility":
    st.write("VOLATILITY")
    st.write("Volatility is a measure of the variability of returns on a financial asset. It is expressed as a percentage and represents the magnitude of variations in returns around the mean. Higher volatility indicates that the returns of the asset are more variable, while lower volatility indicates that the returns are more stable.")
    st.write("  - An investor can use volatility to assess the risk of an investment")
elif chart_type == "Volume":
    st.write("VOLUME ANALYSIS")
    st.write("Volume analysis in financial markets looks at the amount of trading activity for a stock. It can be used to confirm trends or as a signal of change.")
    st.write("- If the price is rising and there is a lot of trading activity (high volume), it may mean that the upward trend")
elif chart_type == "Return and Volume":
    st.write("RETURN AND VOLUME")
    st.write("Understanding the relationship between volume and returns is important for several reasons, including trend confirmation, identification of trend changes, or assessment of market interest.")
    st.write("- Positive correlation: An increase in trading volume may be associated with more significant price movements")
    st.write("- Negative correlation: In some cases, an increase in volume might occur during periods of price consolidation or market indecision. In these cases, there could be an increase in volume without a corresponding significant price movement")