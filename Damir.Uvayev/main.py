from modules.TemperatureDataProcessor import TemperatureDataProcessor
from modules.RouteFinder import RouteFinder
from modules.TemperatureVisualizer import TemperatureVisualizer


def main():
    file_path = 'GlobalLandTemperaturesByMajorCity.csv'
    start_date = input("Enter the start date (YYYY-MM-DD): ")
    end_date = input("Enter the end date (YYYY-MM-DD): ")

    data_processor = TemperatureDataProcessor(file_path)

    
    filtered_data = data_processor.filter_data_by_period(start_date, end_date)

    avg_temperatures = data_processor.compute_city_avg_temperature(filtered_data)

    
    merged_data = data_processor.merge_avg_with_original(avg_temperatures)

    
    visualizer = TemperatureVisualizer(filtered_data)
    visualizer.plot_temperature_trends()
    visualizer.plot_average_temperatures(avg_temperatures)

    
    route_finder = RouteFinder(filtered_data)
    warmest_route = route_finder.find_warmest_route(merged_data, "London", "Cape Town")
    print(f"Warmest route from London to Cape Town: {warmest_route}")


if __name__ == "__main__":
    main()

