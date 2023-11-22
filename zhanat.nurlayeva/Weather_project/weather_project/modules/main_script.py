from modules.data_processor import DataProcessor
from modules.visualization import Visualization
from modules.routing import Routing

class MainScript:
    def __init__(self):
        self.data_processor = DataProcessor('GlobalLandTemperaturesByMajorCity.csv')
        self.visualization = Visualization()
        self.routing = Routing()

    def run(self):
        start_date = input("Enter the start date (YYYY-MM-DD): ")
        end_date = input("Enter the end date (YYYY-MM-DD): ")
        start_city = input("Enter the starting city: ")  # Updated prompt

        self.data_processor.load_data()
        original_data = self.data_processor.data
        filtered_data = self.data_processor.filter_data_by_period(start_date, end_date)
        avg_temperatures = self.data_processor.compute_city_avg_temperature()

        # Visualize temperature trends
        self.visualization.plot_temperature_trends(filtered_data)
        self.visualization.plot_city_temperature_trend(original_data, start_city)

        new_data = self.data_processor.merge_avg_with_original(avg_temperatures)

        # Find warmest route
        route = self.routing.find_warmest_route(new_data, start_city=start_city)
        print(f"Warmest route from {start_city} to Cape Town: {route}")

if __name__ == "__main__":
    main_script = MainScript()
    main_script.run()
