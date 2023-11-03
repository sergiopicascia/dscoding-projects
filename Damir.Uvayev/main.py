from modules import data_processing as dp
from modules import visualization as viz
from modules import routing

def main():
    start_date = input("Enter the start date (YYYY-MM-DD): ")
    end_date = input("Enter the end date (YYYY-MM-DD): ")
    original_data = dp.load_data('GlobalLandTemperaturesByMajorCity.csv')
    filtered_data = dp.filter_data_by_period(original_data, start_date, end_date)
    avg_temperatures = dp.compute_city_avg_temperature(filtered_data)

    viz.plot_temperature_trends(filtered_data)
    viz.plot_city_temperature_trend(filtered_data, "London")

    new_data = dp.merge_avg_with_original(avg_temperatures, filtered_data)
    route = routing.find_warmest_route(new_data, start_city="London")
    print(f"Warmest route from London to Cape Town: {route}")



if __name__ == "__main__":
    main()
