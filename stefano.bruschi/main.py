offset = 0
limit = 3000
period = 'max' # valid periods: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max

import pandas as pd

data = pd.read_csv("http://www.nasdaqtrader.com/dynamic/SymDir/nasdaqtraded.txt", sep='|')
data_clean = data[data['Test Issue'] == 'N']
symbols = data_clean['NASDAQ Symbol'].tolist()
print('total number of symbols traded = {}'.format(len(symbols)))

import yfinance as yf
import os, contextlib

limit = None
offset = 10.0
limit = limit if limit else len(symbols)
end = min(offset + limit, len(symbols))
is_valid = [False] * len(symbols)
# force silencing of verbose API
with open(os.devnull, 'w') as devnull:
    with contextlib.redirect_stdout(devnull):
        for i in range(offset, end):
            s = symbols[i]
            data = yf.download(s, period=period)
            if len(data.index) == 0:
                continue

            is_valid[i] = True
            data.to_csv('hist/{}.csv'.format(s))

print('Total number of valid symbols downloaded = {}'.format(sum(is_valid)))

alid_data = data_clean[is_valid]
valid_data.to_csv('symbols_valid_meta.csv', index=False)
# %%
etfs = valid_data[valid_data['ETF'] == 'Y']['NASDAQ Symbol'].tolist()
stocks = valid_data[valid_data['ETF'] == 'N']['NASDAQ Symbol'].tolist()
# %%
import shutil
from os.path import isfile, join


def move_symbols(symbols, dest):
    for s in symbols:
        filename = '{}.csv'.format(s)
        shutil.move(join('Data', filename), join(dest, filename))


move_symbols(etfs, "etfs")
move_symbols(stocks, "stocks")

import os
import pandas as pd

class RendimentoGiornaliero:
    def __init__(self, cartella_input):
        self.cartella_input = cartella_input
        self.cartella_rendimenti = os.path.join(cartella_input, "rendimenti giornalieri")
        os.makedirs(self.cartella_rendimenti, exist_ok=True)

    def calcola_rendimento_giornaliero(self, nome_file_input):
        # Carica il file CSV
        percorso_file_input = os.path.join(self.cartella_input, nome_file_input)
        df = pd.read_csv(percorso_file_input)

        # Calcola il rendimento giornaliero
        df['rendimento_giornaliero'] = ((df['Open'] / df['Adj Close']) - 1) * 100

        # Salva solo la colonna del rendimento in un nuovo file nella cartella "rendimenti giornalieri"
        nome_file_output = f"rendimento_{nome_file_input}"
        percorso_file_output = os.path.join(self.cartella_rendimenti, nome_file_output)
        df['rendimento_giornaliero'].to_csv(percorso_file_output, index=False, header=['rendimento_giornaliero'])

    def elabora_files_csv(self):
        # Itera attraverso i file nella cartella di input
        for file_csv in os.listdir(self.cartella_input):
            if file_csv.endswith(".csv"):
                # Calcola il rendimento giornaliero e salva il risultato nella cartella "rendimenti giornalieri"
                self.calcola_rendimento_giornaliero(file_csv)

if __name__ == "__main__":
    # Specifica la cartella di input
    cartella_input = r"C:\Users\stebr\DireDSCoding\dscoding-projects\stefano.bruschi\etfs"

    # Crea un'istanza della classe
    rendimento_giornaliero = RendimentoGiornaliero(cartella_input)

    # Elabora i file CSV
    rendimento_giornaliero.elabora_files_csv()

#%%
def calcola_rendimento_medio(self):
    # Lista dei percorsi dei file nella cartella "rendimenti giornalieri"
    percorsi_rendimenti = [os.path.join(self.cartella_rendimenti, file) for file in os.listdir(self.cartella_rendimenti) if file.endswith(".csv")]

    # DataFrame per contenere tutti i rendimenti giornalieri
    df_complessivo = pd.DataFrame()

    # Itera attraverso i file e li unisce in un unico DataFrame
    for percorso_rendimento in percorsi_rendimenti:
        df_file = pd.read_csv(percorso_rendimento)
        df_complessivo = pd.concat([df_complessivo, df_file['rendimento_giornaliero']], axis=1)

    # Calcola la media dei rendimenti giornalieri
    df_complessivo['rendimento_medio'] = df_complessivo.mean(axis=1)

    # Salva il risultato nel file "risultati.csv"
    percorso_risultati = os.path.join(self.cartella_input, "risultati.csv")
    df_complessivo.to_csv(percorso_risultati, index=False)


