# app.py
import streamlit as st
import pandas as pd
import os

# Funzione per caricare i dati dal file CSV selezionato
def load_data(folder, filename):
    file_path = os.path.join('Data', folder, filename)
    data = pd.read_csv(file_path)
    # Converti la colonna 'Date' in tipo datetime
    data['Date'] = pd.to_datetime(data['Date'])
    return data

# Funzione per generare e mostrare il grafico in base alla selezione
def generate_chart(data, chart_type):
    if chart_type == 'performance':
        # Grafico a linee spezzate (line plot) sui valori di 'monthly_mean'
        st.line_chart(data[['Date', 'monthly_mean']].set_index('Date'))

    elif chart_type == 'RMSE':
        # Istogramma basato sui valori di 'RMSE'
        st.bar_chart(data[['Date', 'RMSE']].set_index('Date'))

    elif chart_type == 'performance and RMSE':
        # Scatter plot basato su 'RMSE' e 'monthly_mean'
        st.scatter_chart(data[['RMSE', 'monthly_mean']])

# Pagina principale Streamlit
def main():
    st.title('Visualizzazione dati interattiva con Streamlit')

    # Selettore per la cartella (etfs o stocks)
    folder = st.sidebar.selectbox('Seleziona la cartella', ['etfs', 'stocks'])
    # Lista dei file nella cartella selezionata
    file_list = os.listdir(os.path.join('Data', folder))

    # Selettore per il file
    filename = st.sidebar.selectbox('Seleziona il file', file_list)
    # Carica i dati dal file selezionato
    data = load_data(folder, filename)

    # Selettore per il tipo di grafico
    chart_type = st.sidebar.selectbox('Seleziona il tipo di grafico', ['performance', 'RMSE', 'performance and RMSE'])

    # Chiamare la funzione generate_chart per mostrare il grafico
    generate_chart(data, chart_type)

if __name__ == '__main__':
    main()
