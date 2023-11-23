import sys
import os
# Assuming this is the correct path to your project root
project_root = "/Users/zhanatnurlayeva/Documents/GitHub/dscoding-projects/zhanat.nurlayeva/Weather_project/weather_project"

sys.path.append(os.path.dirname(os.path.abspath(project_root)))

import streamlit as st
from datetime import datetime
from modules.data_processor import DataProcessor
from modules.visualization import Visualization
from modules.routing import Routing

def main():
    import matplotlib
    matplotlib.use('Agg')  # Set the backend to 'Agg'

    st.title("Temperature Analysis and Routing")

    # Sidebar for user input
    st.sidebar.header("Date Range Selection")

    # User input for start date
    start_date_input = st.sidebar.text_input("Enter the start date (YYYY-MM-DD):")
    if not start_date_input:
        st.warning("Please enter the start date.")
        return

    try:
        start_date = datetime.strptime(start_date_input, "%Y-%m-%d").date()  # Parse user input
    except ValueError:
        st.warning("Invalid start date format. Please use the format YYYY-MM-DD.")
        return

    # User input for end date
    end_date_input = st.sidebar.text_input("Enter the end date (YYYY-MM-DD):")
    if not end_date_input:
        st.warning("Please enter the end date.")
        return

    try:
        end_date = datetime.strptime(end_date_input, "%Y-%m-%d").date()  # Parse user input
    except ValueError:
        st.warning("Invalid end date format. Please use the format YYYY-MM-DD.")
        return

    # Check if the end date is greater than the start date
    if end_date <= start_date:
        st.warning("End date must be greater than the start date.")
        return

    # Specify the file path for your CSV file
    file_path = 'GlobalLandTemperaturesByMajorCity.csv'

    data_processor = DataProcessor(file_path)
    original_data = data_processor.data
    filtered_data = data_processor.filter_data_by_period(start_date, end_date)
    avg_temperatures = data_processor.compute_city_avg_temperature()

    visualization = Visualization()

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

    # Find the warmest route from the selected starting city to the destination city
    st.header("Routing")
    end_city = st.selectbox("Select the destination city:", avg_temperatures['City'].unique())
    st.info("Select the destination city from the dropdown to find the warmest route from the starting city.")

    # Use st.cache decorator for the routing function
    @st.cache
    def find_warmest_route(avg_temperatures, start_city, end_city="Cape Town"):
        routing = Routing()
        return routing.find_warmest_route(avg_temperatures, start_city=start_city, end_city=end_city)

    route = find_warmest_route(avg_temperatures, start_city=start_city, end_city=end_city)
    st.subheader(f"Warmest route from {start_city} to {end_city}:")
    st.success(f"The suggested route is: {route}")

    # Visualize temperature ranges for cities during different historical periods
    st.header("Temperature Ranges Over Time")
    st.subheader("Cities with Largest Temperature Ranges")
    st.info("The map below highlights cities with the largest temperature ranges during different historical periods.")

    visualization.plot_temperature_trends(filtered_data)

if __name__ == "__main__":
    main()

