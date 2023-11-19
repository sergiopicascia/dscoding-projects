# Main Script
# Use the classes to perform the main tasks.
from modules import data_processor as dp
from modules import visualization as viz
from modules import routing

class ClimateAnalyzer:
    # ClimateAnalyzer class that encapsulates the steps of the analysis.
    def __init__(self, data_file):
        self.data_file = data_file
        self.original_data = None
        self.filtered_data = None
        self.avg_temperatures = None
        self.new_data = None
        self.route = None

    def run_analysis(self):
        self.get_date_range()
        self.load_original_data()
        self.filter_data()
        self.compute_avg_temperatures()
        self.visualize_temperature_trends()
        self.visualize_city_temperature_trend("London")
        self.merge_avg_with_original()
        self.find_warmest_route("London")

    def get_date_range(self):
        self.start_date = input("Enter the start date (YYYY-MM-DD): ")
        self.end_date = input("Enter the end date (YYYY-MM-DD): ")

    def load_original_data(self):
        self.original_data = dp.load_data(self.data_file)

    def filter_data(self):
        self.filtered_data = dp.filter_data_by_period(self.original_data, self.start_date, self.end_date)

    def compute_avg_temperatures(self):
        self.avg_temperatures = dp.compute_city_avg_temperature(self.filtered_data)

    def visualize_temperature_trends(self):
        viz.plot_temperature_trends(self.filtered_data)

    def visualize_city_temperature_trend(self, city):
        viz.plot_city_temperature_trend(self.filtered_data, city)

    def merge_avg_with_original(self):
        self.new_data = dp.merge_avg_with_original(self.avg_temperatures, self.filtered_data)

    def find_warmest_route(self, start_city):
        self.route = routing.find_warmest_route(self.new_data, start_city=start_city)
        print(f"Warmest route from {start_city} to Cape Town: {self.route}")

def main():
    analyzer = ClimateAnalyzer('../GlobalLandTemperaturesByMajorCity.csv')
    analyzer.run_analysis()

if __name__ == "__main__":
    main()
