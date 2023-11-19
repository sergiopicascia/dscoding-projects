import streamlit as st
import pandas as pd
from utils import filteringName, filteringTask

dataFirstStrategy = pd.read_excel(
    "/Users/vladislavkovalev/Desktop/git/UniMi-DSE-Master/1 year 1 thrimester/Pyhton/dscoding-projects/Vladislav_Kovalev/results_tools/report_display/results/first_strategy.xlsx"
)
dataSecondStrategy = pd.read_excel(
    "/Users/vladislavkovalev/Desktop/git/UniMi-DSE-Master/1 year 1 thrimester/Pyhton/dscoding-projects/Vladislav_Kovalev/results_tools/report_display/results/second_strategy.xlsx"
)
dataThirdStrategy = pd.read_excel(
    "/Users/vladislavkovalev/Desktop/git/UniMi-DSE-Master/1 year 1 thrimester/Pyhton/dscoding-projects/Vladislav_Kovalev/results_tools/report_display/results/third_strategy.xlsx"
)
dataFourthStrategy = pd.read_excel(
    "/Users/vladislavkovalev/Desktop/git/UniMi-DSE-Master/1 year 1 thrimester/Pyhton/dscoding-projects/Vladislav_Kovalev/results_tools/report_display/results/fourth_strategy.xlsx"
)

# Reports generated for strategies
for indexStrategy, dataStrategy in enumerate(
    [
        dataFirstStrategy,
        dataSecondStrategy,
        dataThirdStrategy,
        dataFourthStrategy,
    ]
):
    # Calculate the report metrics
    num_customers = len(dataStrategy.dropna(subset=["GUEST"]))
    num_rooms_occupied = len(dataStrategy.dropna(subset=["HOTEL"]))
    num_hotels_occupied = dataStrategy["HOTEL"].nunique()
    total_earnings = dataStrategy["NETTO"].sum()
    average_satisfaction = dataStrategy["PRIORITY"].mean()

    # Display the report
    st.header(f"{filteringName[indexStrategy]} strategy")
    st.write(f"Type of strategy: {filteringTask[indexStrategy]}")
    st.write(f"Number of customers accommodated: {num_customers}")
    st.write(f"Number of rooms occupied: {num_rooms_occupied}")
    st.write(f"Number of different hotels occupied: {num_hotels_occupied}")
    st.write(f"Total volume of business: {total_earnings:.2f}")
    st.write(f"Average customer satisfaction: {average_satisfaction:.2f}")
