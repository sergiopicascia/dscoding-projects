import pandas as pd
import openpyxl

file=open('/Users/tesi/Downloads/hotels/hotels.xlsx','r')
def import_data(path):
	with open ("/Users/tesi/Downloads/hotels/hotels.xlsx","r") as file:
		data=file.readlines()
	return data


pd.read_excel(r"/Users/tesi/Downloads/hotels/guests.xlsx")
