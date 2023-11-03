import pandas as pd
import matplotlib.pyplot as plt

# Load the data
df = pd.read_csv('GLT_ByMajorCity.csv')

# Display info about the dataset
print("\nDataset shape:", df.shape)
print("Unique cities:", df['City'].nunique())
print("Unique countries:", df['Country'].nunique())
print("Missing values:\n", df.isnull().sum())

# Drop rows with missing values
df.dropna(inplace=True)
print("\nNew dataset shape:", df.shape)

# Filter the dataset for New York
df_ny = df[df['City'] == 'New York']

# Smoothing the data with 12-Month Rolling Average
df_ny['RollingAvg'] = df_ny['AverageTemperature'].rolling(window=12).mean()

# Plot the smoothed data for New York
plt.figure(figsize=(14, 7))
plt.plot(df_ny['dt'], df_ny['RollingAvg'], label='12-Month Rolling Average', color='red')
plt.title('Temperature Trend for New York', fontsize=16)
plt.xlabel('Year', fontsize=14)
plt.ylabel('Temperature (°C)', fontsize=14)
plt.grid(True, which="both", ls="--", c='0.7')
plt.legend()
plt.tight_layout()
plt.show()

# Example data for Temperature Change from 1900 to 2000
years = [1900, 2000]
avg_temperatures = [15, 17]  # Average temperatures for 1900 and 2000

plt.figure(figsize=(8, 6))
plt.plot(years, avg_temperatures, marker='o', linestyle='-', color='blue')
for i, txt in enumerate(years):
    plt.annotate(txt, (years[i], avg_temperatures[i] + 0.1))
plt.title("Temperature Change from 1900 to 2000")
plt.xlabel("Year")
plt.ylabel("Average Temperature (°C)")
plt.grid(True, which="both", ls="--", c='0.7')
plt.tight_layout()
plt.show()