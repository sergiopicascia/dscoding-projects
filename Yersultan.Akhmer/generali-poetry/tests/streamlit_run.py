import streamlit as st
import pandas as pd
from data_manager import DataManager
from allocator import Allocator
import matplotlib.pyplot as plt
data_manager = DataManager(
    '/Users/yersultanakhmer/Downloads/hotels/hotels.xlsx', 
    '/Users/yersultanakhmer/Downloads/hotels/guests.xlsx', 
    '/Users/yersultanakhmer/Downloads/hotels/preferences.xlsx'
)

# Initialize Allocator with the DataManager
allocator = Allocator(data_manager)

# Function to run an allocation strategy and get its report
def run_and_get_report(strategy):
    if strategy == "Price":
        allocator.price_allocation()
    elif strategy == "Random":
        allocator.random_allocation()
    elif strategy == "Preference":
        allocator.customer_preference_allocation()
    elif strategy == "Availability":
        allocator.availability_allocation()
    else:
        raise ValueError("Unknown strategy")
    
    detailed_report_df, summary_df, hotel_earnings = allocator.display_report()
    summary_df['Strategy Name'] = strategy
    return detailed_report_df, summary_df, hotel_earnings


def run_all_strategies():
    strategies = ["Price", "Random", "Preference", "Availability"]
    reports = {}
    for strategy in strategies:
        report = run_and_get_report(strategy)
        reports[strategy] = report
    return reports

# Add a new option in the Streamlit interface
with st.sidebar:
    add_radio = st.radio("Choose an option", ("View Data", "Run Allocation Strategy", "Run All Strategies"))

# Main area of the app
if add_radio == "View Data":
    data_selection = st.selectbox("Select Data", ["Hotels", "Guests", "Preferences"])
    if data_selection == "Hotels":
        st.dataframe(data_manager.get_hotels())
    elif data_selection == "Guests":
        st.dataframe(data_manager.get_guests())
    elif data_selection == "Preferences":
        st.dataframe(data_manager.get_preferences())

elif add_radio == "Run Allocation Strategy":
    allocation_method = st.selectbox("Select Allocation Method", ["Price", "Random", "Preference", "Availability"])
    if st.button("Run Strategy"):
        detailed_report_df, summary_df, hotel_earnings = run_and_get_report(allocation_method)

        
        # Display detailed allocation results
        st.subheader(f"Detailed Results for {allocation_method} Strategy")
        st.dataframe(detailed_report_df)

        # Display summary statistics
        st.subheader("Summary Statistics")
        st.dataframe(summary_df)

        st.subheader(f"Earnings by Hotel for {allocation_method} Strategy")
        hotel_earnings_df = pd.DataFrame(list(hotel_earnings.items()), columns=["Hotel", "Earnings"])
        st.dataframe(hotel_earnings_df)

        # Save the detailed report to Excel
        excel_file = f"./OOP_3/All_function/excels/{allocation_method.lower()}_allocation_strategy.xlsx"
        detailed_report_df.to_excel(excel_file, index=False)
        st.success(f"Detailed report saved to {excel_file}")

elif add_radio == "Run All Strategies":
    if st.button("Execute All Strategies"):
        all_detailed_reports = pd.DataFrame()
        all_summary_reports = pd.DataFrame()
        all_hotel_earnings = {}
        top_earning_hotels_all_strategies = {}

        for strategy in ["Price", "Random", "Preference", "Availability"]:
            detailed_report_df, summary_df, hotel_earnings = run_and_get_report(strategy)
            all_detailed_reports = pd.concat([all_detailed_reports, detailed_report_df.assign(Strategy=strategy)])
            all_summary_reports = pd.concat([all_summary_reports, summary_df.assign(Strategy=strategy)])
            all_hotel_earnings[strategy] = hotel_earnings
            top_earning_hotels_all_strategies[strategy] = allocator.get_top_earning_hotels()

        # Plotting total volume of business for each strategy
        plt.figure(figsize=(10, 6))
        for i, row in all_summary_reports.iterrows():
            plt.bar(row['Strategy Name'], row['Total volume of business'], label=row['Strategy Name'])

        plt.xlabel('Strategy')
        plt.ylabel('Total Volume of Business')
        plt.title('Total Volume of Business by Strategy')
        plt.legend()
        st.pyplot(plt)

        # Plot customer satisfaction rates for each strategy
        plt.figure(figsize=(10, 6))
        strategies = all_summary_reports['Strategy Name'].unique()
        satisfaction_rates = [float(row['Customer satisfaction rate'].strip('%')) for _, row in all_summary_reports.iterrows()]

        plt.plot(strategies, satisfaction_rates, marker='o', linestyle='-', color='blue')
        plt.xlabel('Strategy')
        plt.ylabel('Customer Satisfaction Rate (%)')
        plt.title('Customer Satisfaction Rate by Strategy')
        plt.grid(True)
        plt.xticks(rotation=45)
        plt.tight_layout()
        st.pyplot(plt)

        for strategy, top_earning_hotels in top_earning_hotels_all_strategies.items():
            st.subheader(f"Top 10 Earning Hotels for {strategy} Strategy")
            top_earnings_df = pd.DataFrame(top_earning_hotels, columns=["Hotel", "Earnings"])
            st.dataframe(top_earnings_df)

            # Plot for Top Earning Hotels
            hotels, earnings = zip(*top_earning_hotels)
            plt.figure(figsize=(12, 6))
            plt.bar(hotels, earnings, color='blue')
            plt.xlabel('Hotels')
            plt.ylabel('Earnings')
            plt.title(f'Top 10 Earning Hotels for {strategy} Strategy')
            plt.xticks(rotation=45)
            plt.tight_layout()
            st.pyplot(plt)