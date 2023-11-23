from data_processor import DataProcessor
from visualization import Visualization
from routing import Routing

class MainScript:
    def __init__(self):
        self.data_processor = DataProcessor('GlobalLandTemperaturesByMajorCity.csv')
        self.visualization = Visualization()
        self.routing = Routing()
        self.start_city = "Beijing"  # Set default starting city

    def run(self):
        start_date = input("Enter the start date (YYYY-MM-DD): ")
        end_date = input("Enter the end date (YYYY-MM-DD): ")

        # Use the default starting city or prompt the user to enter a different one
        start_city = input(f"Enter the starting city (default is {self.start_city}): ")
        start_city = start_city.strip() or self.start_city

        # Provide the file_path argument when calling load_data
        self.data_processor.load_data(file_path='GlobalLandTemperaturesByMajorCity.csv')
        original_data = self.data_processor.data
        filtered_data = self.data_processor.filter_data_by_period(start_date, end_date)
        avg_temperatures = self.data_processor.compute_city_avg_temperature()

        # Visualize temperature trends
        try:
            self.visualization.plot_temperature_trends(filtered_data)
            self.visualization.plot_city_temperature_trend(original_data, start_city)
        except Exception as e:
            print(f"Error: {e}")
            print("There was an issue rendering the plots. Please check your data and try again.")

        new_data = self.data_processor.merge_avg_with_original(avg_temperatures)

        # Find warmest route
        route = self.routing.find_warmest_route(new_data, start_city=start_city)
        print(f"Warmest route from {start_city} to Cape Town: {route}")

if __name__ == "__main__":
            main_script = MainScript()
            main_script.run()

