'''
IMPORTARE I PACCHETTI CHE MI SERVONO PER IL PROGETTO
'''
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

'''
IMPORTARE I DATASET E PULIRLI, METTENDO SOLO I CAMPI CHE MI SERVONO
'''
title_basics = pd.read_csv("//Users/ariannagirotto/Desktop/dataset/title.basics.tsv", sep="\t", quoting=3,
                           encoding='utf-8', engine='python', nrows=100000)
info_person = pd.read_csv("//Users/ariannagirotto/Desktop/dataset/name.tsv", sep="\t", quoting=3, encoding='utf-8',
                          engine='python', nrows=100000)

title_basics = title_basics[(title_basics['startYear'] != '\\N') &
                            (title_basics['tconst'] != '\\N') &
                            (title_basics['genres'] != '\\N')]
info_person = info_person[(info_person['birthYear'] != '\\N') &
                          (info_person['primaryName'] != '\\N') &
                          (info_person['primaryProfession'] != '\\N')]

difficult_title_basics = title_basics[
    (title_basics['startYear'].astype(int) >= 1800) &
    (title_basics['startYear'].astype(int) < 1940)]
difficult_title_basics = difficult_title_basics.sort_values(by='startYear', ascending=True)

print(difficult_title_basics)
