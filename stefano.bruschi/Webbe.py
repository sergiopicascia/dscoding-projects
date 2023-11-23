import streamlit as st
import os
import pandas as pd
import plotly.express as px

# Funzione per caricare i dati in base ai file selezionati e al periodo selezionato
def load_data(selected_files, selected_folder_path, selected_year):
    data = pd.DataFrame()

    for file in selected_files:
        file_path = os.path.join(selected_folder_path, file)
        df = pd.read_csv(file_path)
        df['Date'] = pd.to_datetime(df['Date'])
        df = df.set_index('Date')
        df['File'] = file  # Aggiungi la colonna 'File' con il nome del file
        df = df.loc[f'{selected_year[0]}-01-01':f'{selected_year[1]}-12-31']

        data = pd.concat([data, df])

    return data

# Funzione per calcolare la media mensile per ogni colonna e file
def calculate_monthly_mean(data):
    return data.groupby(['File', pd.Grouper(freq='M')]).mean().reset_index()

# Percorso della cartella "Data"
data_folder = "Data"

# Lista delle cartelle all'interno di "Data"
subfolders = [f.name for f in os.scandir(data_folder) if f.is_dir()]

# Selezione della cartella
selected_folder = st.radio("Seleziona una cartella", subfolders)

# Percorso completo della cartella selezionata
selected_folder_path = os.path.join(data_folder, selected_folder)

# Lista dei file nella cartella selezionata
files = [f.name for f in os.scandir(selected_folder_path) if f.is_file()]

# Selezione multipla dei file
selected_files = st.multiselect("Seleziona i file", files)

# Selezionatore per il tipo di grafico
chart_type = st.selectbox("Seleziona il tipo di grafico", ["Performance", "Performance and Volatility", "Volume", "Volatility"])

# Selezionatore per l'arco temporale annuale
start_year = 2013
end_year = 2023
selected_year = st.slider("Seleziona l'anno", start_year, end_year, (start_year, end_year), step=1)

# Carica i dati
data = load_data(selected_files, selected_folder_path, selected_year)

# Calcola la media mensile
monthly_data = calculate_monthly_mean(data)

# Genera e visualizza il grafico in base alla selezione
if chart_type == "Performance":
    fig = px.line(monthly_data, x='Date', y='monthly_mean', color='File', title='Performance')
    st.plotly_chart(fig)

elif chart_type == "Performance and Volatility":
    fig = px.scatter(monthly_data, x='monthly_mean', y='RMSE', color='File', title='Performance and Volatility')
    st.plotly_chart(fig)

elif chart_type == "Volatility":
    fig = px.area(monthly_data, x='Date', y='RMSE', color='File', title='Volatility')
    st.plotly_chart(fig)

elif chart_type == "Volume":
    fig = px.bar(monthly_data, x='Date', y='Vol_month_mean', color='File', title='Volume')
    st.plotly_chart(fig)

