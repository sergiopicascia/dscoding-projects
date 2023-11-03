import pandas as pd

data_1 = pd.read_excel('/Users/yersultanakhmer/Downloads/hotels/guests.xlsx')
data_2 = pd.read_excel('/Users/yersultanakhmer/Downloads/hotels/hotels.xlsx')
data_3 = pd.read_excel('/Users/yersultanakhmer/Downloads/hotels/preferences.xlsx')

print(data_1.head(5))

print(round(16%5,2))

a = 1/6
print(a)
print(round(a, 2))