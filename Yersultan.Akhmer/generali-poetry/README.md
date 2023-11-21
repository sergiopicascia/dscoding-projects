
### Overview
This Streamlit application is designed to optimize hotel room allocations based on various strategies. It effectively manages hotel booking data, guest preferences, and available rooms to maximize both revenue and customer satisfaction. The system offers an interactive interface to view data, run allocation strategies, and compare results across different methodologies.

### Features
- **Data Visualization**: View detailed information about hotels, guests, and their preferences through an intuitive interface.
- **Allocation Strategies**: Implement four distinct strategies for room allocation - Price, Random, Preference, and Availability.
- **Strategy Execution**: Run individual allocation strategies and view detailed reports on allocations, earnings, and customer satisfaction.
- **Comparative Analysis**: Execute all strategies simultaneously for a comprehensive comparison. Analyze total business volume, customer satisfaction rates, and hotel earnings across strategies.
- **Top Performers**: Identify the top 10 earning hotels for each strategy and visualize their performance through bar plots.

### Allocation Strategies
1. **Price-Based Allocation**: Prioritizes room allocation based on the price of the hotels.
2. **Random Allocation**: Assigns rooms randomly, disregarding preferences or pricing.
3. **Preference-Based Allocation**: Allocates rooms according to guest preferences.
4. **Availability-Based Allocation**: Focuses on maximizing room occupancy.

### Running the Application
To start the application:
1. Ensure you have Streamlit installed.
2. Navigate to the application directory.
3. Run `streamlit run streamlit_run.py`.

### Navigating the Interface
- Use the sidebar to select between viewing data or running allocation strategies.
- Choose an individual strategy to see its specific outcomes or select "Run All Strategies" for a comprehensive analysis.
- Explore detailed dataframes and visualizations for insights on strategy performance.

### Technology Stack
- **Streamlit**: For creating the web application interface.
- **Pandas**: For data manipulation and analysis.
- **Matplotlib**: For generating plots and visualizations.
- **Numpy**: For analysis of large arrays.
