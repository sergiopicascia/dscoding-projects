# app.py

import streamlit as st
from modules.data_processor import DataProcessor
from modules.visualization import Visualization
from modules.routing import Routing
from modules.utils import convert_to_decimal

def main():
    st.title("Temperature Analysis and Routing")

    # Sidebar for user input
    st.sidebar.header("Date Range Selection")
    start_date = st.sidebar.text_input("Enter the start date (YYYY-MM-DD):", "1750-01-01")
    end_date = st.sidebar.text_input("Enter the end date (YYYY-MM-DD):", "2023-01-01")

    # Specify the file path for your CSV file
    file_path = 'GlobalLandTemperaturesByMajorCity.csv'

    data_processor = DataProcessor(file_path)
    #data_processor.load_data()  # Pass the file path to load_data method
    data_processor.load_data(file_path)  # Pass the file path to load_data method
    original_data = data_processor.data
    filtered_data = data_processor.filter_data_by_period(start_date, end_date)
    avg_temperatures = data_processor.compute_city_avg_temperature()

    visualization = Visualization()
    routing = Routing()

    # ... rest of your code ...


    # Visualize temperature trends
    st.header("Temperature Trends")
    st.subheader("Average Temperature for Cities on Map")
    st.info("The map below shows the average temperature for cities around the world. Use the sidebar to select the date range.")

    visualization.plot_data(avg_temperatures)

    # Automatically set the starting city as "Beijing" for the best route suggestion
    start_city = st.text_input("Enter the starting city:", "Beijing")
    st.subheader(f"Temperature Trend for {start_city}")
    st.info(f"The line chart below displays the temperature trend for {start_city} over time.")

    visualization.plot_city_temperature_trend(original_data, start_city)

    # Find warmest route from the selected starting city to the destination city
    st.header("Routing")
    end_city = st.selectbox("Select the destination city:", avg_temperatures['City'].unique())
    st.info("Select the destination city from the dropdown to find the warmest route from the starting city.")

    route = routing.find_warmest_route(avg_temperatures, start_city=start_city, end_city=end_city)
    st.subheader(f"Warmest route from {start_city} to {end_city}:")
    st.success(f"The suggested route is: {route}")

    # Visualize temperature ranges for cities during different historical periods
    st.header("Temperature Ranges Over Time")
    st.subheader("Cities with Largest Temperature Ranges")
    st.info("The map below highlights cities with the largest temperature ranges during different historical periods.")

    visualization.plot_temperature_trends(filtered_data)

if __name__ == "__main__":
    main()
