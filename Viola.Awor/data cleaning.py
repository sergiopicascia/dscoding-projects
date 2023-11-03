import pandas as pd
import numpy as np
import matplotlib as plt


# import  by cityCSV file and read
df = pd.read_csv('GlobalLandTemperaturesByCity.csv')
# Display the DataFrame infromation about the dataset
print(df)
print(df.info())
#droping missing values
df.dropna(inplace=True)
# Removing duplicates
df.drop_duplicates(inplace=True)
# Displaing basic statistics after cleaning
print(df.describe())
# Save the cleaned dataset to a new CSV file
df.to_csv('cleaned_GlobalLandTemperaturesByCity.csv', index=False)



# country set

# import  by country file and read
df = pd.read_csv('GlobalLandTemperaturesByCountry.csv')
# Display the DataFrame infromation about the dataset
print(df)
print(df.info())
#droping missing values
df.dropna(inplace=True)
# Removing duplicates
df.drop_duplicates(inplace=True)
# Displaing basic statistics after cleaning
print(df.describe())
# Save the cleaned dataset to a new CSV file
df.to_csv('cleaned_GlobalLandTemperaturesByCountry.csv', index=False)




# cleaning bymajor city file

# import  by by majorcity  file and read
df = pd.read_csv('GlobalLandTemperaturesByMajorCity.csv')
# Display the DataFrame infromation about the dataset
print(df)
print(df.info())
#droping missing values
df.dropna(inplace=True)
# Removing duplicates
df.drop_duplicates(inplace=True)
# Displaing basic statistics after cleaning
print(df.describe())
# Save the cleaned dataset to a new CSV file
df.to_csv('cleaned_GlobalLandTemperaturesByMajorCity.csv', index=False)



#  cleaning bystate  file


# import  bystate file and read
df = pd.read_csv('GlobalLandTemperaturesByState.csv')
# Display the DataFrame infromation about the dataset
print(df)
print(df.info())
#droping missing values
df.dropna(inplace=True)
# Removing duplicates
df.drop_duplicates(inplace=True)
# Displaing basic statistics after cleaning
print(df.describe())
# Save the cleaned dataset to a new CSV file
df.to_csv('cleaned_GlobalLandTemperaturesByState.csv.csv', index=False)





# import  temperature file and read
df = pd.read_csv('GlobalTemperatures.csv')
# Display the DataFrame infromation about the dataset
print(df)
print(df.info())
#droping missing values
df.dropna(inplace=True)
# Removing duplicates
df.drop_duplicates(inplace=True)
# Displaing basic statistics after cleaning
print(df.describe())
# Save the cleaned dataset to a new CSV file
df.to_csv('cleaned_GlobalTemperatures.csv', index=False)