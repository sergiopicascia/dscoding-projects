from modules.TemperatureDataProcessor import TemperatureDataProcessor
from modules.RouteFinder import RouteFinder
from modules.TemperatureVisualizer import TemperatureVisualizer

def main():
    file_path = 'GlobalLandTemperaturesByMajorCity.csv'
    start_date = input("Enter the start date (YYYY-MM-DD): ")
    end_date = input("Enter the end date (YYYY-MM-DD): ")

    # Create an instance of TemperatureDataProcessor and load data
    data_processor = TemperatureDataProcessor(file_path)

    # Filter data based on the provided date range
    filtered_data = data_processor.filter_data_by_period(start_date, end_date)

    # Create an instance of TemperatureVisualizer for visualizations
    visualizer = TemperatureVisualizer(filtered_data)
    visualizer.plot_temperature_trends()

    # Create an instance of RouteFinder for routing
    route_finder = RouteFinder(filtered_data)
    warmest_route = route_finder.find_warmest_route(start_city="London", end_city="Cape Town")
    print(f"Warmest route from London to Cape Town: {warmest_route}")

if __name__ == "__main__":
    main()
