import pandas as pd

# Read the TSV file
tsv_file_path = "C:\\Users\\Samaher\\Desktop\\Folder of folders\\Courses\\Coding\\Python\\IMDb\\name.basics.tsv"
df = pd.read_csv(tsv_file_path, delimiter='\t')

# Display the first few rows of the DataFrame
print(df.head())

