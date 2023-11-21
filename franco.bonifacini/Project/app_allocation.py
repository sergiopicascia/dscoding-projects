import streamlit as st
import pandas as pd
import numpy as np
from data import Hotelsdata
from methods import Strategy

# Setting page configuration
st.set_page_config(layout='wide')

# General title
st.title('Allocation strategies of guests into hotels')

# 1st subheader: introduction of the project
st.header('_Introduction to the project_')
st.write('**Based on a dataset containing information about guests, hotels and guests´ preferences, this program outputs 4 different allocation strategies:**')
st.caption(':small_blue_diamond: :blue[**Random strategy:**] guests are allocated randomly into hotels.')
st.caption(':small_blue_diamond: :blue[**Preference strategy:**] guests are allocated into hotels based on their list of preference and room availability.')
st.caption(':small_blue_diamond: :blue[**Price strategy:**] guests are allocated into hotels based on price (from cheapest to most expensive), guests´s preferences and room availiability.')
st.caption(':small_blue_diamond: :blue[**Rooms strategy:**] guests are allocated into hotels based on number of rooms per hotel (from most rommy to least roomy), guests´s preferences and room availiability.')
st.write('---')  

# DataFrames
path = 'Datasets'
data = Hotelsdata(path)
df_guests = data.guests
df_hotels = data.hotels
df_preference = data.preference

# Assigning the DataFrames to the strategy class
strategy = Strategy(df_guests, df_hotels, df_preference)

# 2nd subheader: possibility to select strategy to see data visualization
st.header('_Strategy results_')

# Select box: for selecting a strategy from the list of strategies
select_strategy = st.selectbox(
    label='_Select a strategy to see detailed results of the allocation:_',
    options=["Random strategy", "Preference strategy", "Price strategy", "Rooms strategy"], 
    index=None, 
    placeholder="Select strategy...")

# Conditional function to output the result of the strategy selected in the select box
# Random strategy
if select_strategy == 'Random strategy':
    random = strategy.random
    st.subheader('_Summary_')
    
    # Metrics
    col1, col2, col3, col4, col5, col6, col7 = st.columns(7)
    col1.metric("Guests allocated", f"{random['guest'].count():,}")
    col2.metric("Guests allocated (%)", f"{round((random['guest'].count()/data.guests['guest'].count())*100,2)}%")
    col3.metric("Average satisfaction", int(round((random['guest_satisfaction'].mean()),0)))
    col4.metric("Hotels occupied", random['hotel'].nunique())
    col5.metric("Hotels occupied (%)", f"{round((random['hotel'].nunique()/data.hotels['hotel'].count())*100,2)}%")
    col6.metric("Strategy´s total earnings", f"€{int(random['net_earning'].sum()):,}")
    col7.metric("Average earnings per hotel", f"€{int(round(random['net_earning'].sum() / random['hotel'].nunique(), 0)):,}")
    st.caption('_* Satisfaction is measured from 1 (completely satisfied) to 5 (very dissatisfied)_')
    
    # DataFrame with the details about the allocation
    st.subheader('_DataFrame with allocations_')
    st.dataframe(random.set_index('guest'))
    
    # DataFrame with level of satisfaction
    st.subheader('_Number of guests by level of satisfaction_')
    st.caption('_* Satisfaction is measured from 1 (completely satisfied) to 5 (very dissatisfied)_')
    satisfaction_levels = [1, 2, 3, 4, 5]
    Results = pd.DataFrame(['Random strategy'], columns=['Strategy'])
    for level in satisfaction_levels:
        column_name = [level]
        Results[column_name] = [f"{random['guest_satisfaction'].eq(level).sum():,}"]
    st.dataframe(Results.set_index('Strategy'))
    
    # Bar chart to visualize number of guests by level of satisfaction
    satisfaction = random.groupby('guest_satisfaction')['guest'].count().reset_index()
    st.bar_chart(data = satisfaction, x='guest_satisfaction', y='guest', color="#5f9ea0", width=100, height=400)

# Preference strategy
elif select_strategy == 'Preference strategy':
    preference = strategy.preference
    st.subheader('_Summary_')
    
    # Metrics
    col1, col2, col3, col4, col5, col6, col7 = st.columns(7)
    col1.metric("Guests allocated", f"{preference['guest'].count():,}")
    col2.metric("Guests allocated (%)", f"{round((preference['guest'].count()/data.guests['guest'].count())*100,2)}%")
    col3.metric("Average satisfaction", int(round((preference['guest_satisfaction'].mean()),0)))
    col4.metric("Hotels occupied", preference['hotel'].nunique())
    col5.metric("Hotels occupied (%)", f"{round((preference['hotel'].nunique()/data.hotels['hotel'].count())*100,2)}%")
    col6.metric("Strategy´s total earnings", f"€{int(preference['net_earning'].sum()):,}")
    col7.metric("Average earnings per hotel", f"€{int(round(preference['net_earning'].sum() / preference['hotel'].nunique(), 0)):,}")
    st.caption('_* Satisfaction is measured from 1 (completely satisfied) to 5 (very dissatisfied)_')
    
    # DataFrame with the details about the allocation
    st.subheader('_DataFrame with allocations_')
    st.dataframe(preference.set_index('guest'))
    
    # DataFrame with level of satisfaction
    st.subheader('_Number of guests by level of satisfaction_')
    st.caption('_* Satisfaction is measured from 1 (completely satisfied) to 5 (very dissatisfied)_')
    satisfaction_levels = [1, 2, 3, 4, 5]
    Results = pd.DataFrame(['Preference strategy'], columns=['Strategy'])
    for level in satisfaction_levels:
        column_name = [level]
        Results[column_name] = [f"{preference['guest_satisfaction'].eq(level).sum():,}"]
    st.dataframe(Results.set_index('Strategy'))
    
    # Bar chart to visualize number of guests by level of satisfaction
    satisfaction = preference.groupby('guest_satisfaction')['guest'].count().reset_index()
    st.bar_chart(data = satisfaction, x='guest_satisfaction', y='guest', color="#5f9ea0", width=100, height=400)

# Price strategy
elif select_strategy == 'Price strategy':
    price = strategy.price
    st.subheader('_Summary_')
    
    # Metrics
    col1, col2, col3, col4, col5, col6, col7 = st.columns(7)
    col1.metric("Guests allocated", f"{price['guest'].count():,}")
    col2.metric("Guests allocated (%)", f"{round((price['guest'].count()/data.guests['guest'].count())*100,2)}%")
    col3.metric("Average satisfaction", int(round((price['guest_satisfaction'].mean()),0)))
    col4.metric("Hotels occupied", price['hotel'].nunique())
    col5.metric("Hotels occupied (%)", f"{round((price['hotel'].nunique()/data.hotels['hotel'].count())*100,2)}%")
    col6.metric("Strategy´s total earnings", f"€{int(price['net_earning'].sum()):,}")
    col7.metric("Average earnings per hotel", f"€{int(round(price['net_earning'].sum() / price['hotel'].nunique(), 0)):,}")
    st.caption('_* Satisfaction is measured from 1 (completely satisfied) to 5 (very dissatisfied)_')
    
    # DataFrame with the details about the allocation
    st.subheader('_DataFrame with allocations_')
    st.dataframe(price.set_index('guest'))
    
    # DataFrame with level of satisfaction
    st.subheader('_Number of guests by level of satisfaction_')
    st.caption('_* Satisfaction is measured from 1 (completely satisfied) to 5 (very dissatisfied)_')
    satisfaction_levels = [1, 2, 3, 4, 5]
    Results = pd.DataFrame(['Price strategy'], columns=['Strategy'])
    for level in satisfaction_levels:
        column_name = [level]
        Results[column_name] = [f"{price['guest_satisfaction'].eq(level).sum():,}"]
    st.dataframe(Results.set_index('Strategy'))
    
    # Bar chart to visualize number of guests by level of satisfaction
    satisfaction = price.groupby('guest_satisfaction')['guest'].count().reset_index()
    st.bar_chart(data = satisfaction, x='guest_satisfaction', y='guest', color="#5f9ea0", width=100, height=400)

# Rooms strategy
elif select_strategy == 'Rooms strategy':
    rooms = strategy.rooms
    st.subheader('_Summary_')
    
    # Metrics
    col1, col2, col3, col4, col5, col6, col7 = st.columns(7)
    col1.metric("Guests allocated", f"{rooms['guest'].count():,}")
    col2.metric("Guests allocated (%)", f"{round((rooms['guest'].count()/data.guests['guest'].count())*100,2)}%")
    col3.metric("Average satisfaction", int(round((rooms['guest_satisfaction'].mean()),0)))
    col4.metric("Hotels occupied", rooms['hotel'].nunique())
    col5.metric("Hotels occupied (%)", f"{round((rooms['hotel'].nunique()/data.hotels['hotel'].count())*100,2)}%")
    col6.metric("Strategy´s total earnings", f"€{int(rooms['net_earning'].sum()):,}")
    col7.metric("Average earnings per hotel", f"€{int(round(rooms['net_earning'].sum() / rooms['hotel'].nunique(), 0)):,}")
    st.caption('_* Satisfaction is measured from 1 (completely satisfied) to 5 (very dissatisfied)_')
    
    # DataFrame with the details about the allocation
    st.subheader('_DataFrame with allocations_')
    st.dataframe(rooms.set_index('guest'))
    
    # DataFrame with level of satisfaction
    st.subheader('_Number of guests by level of satisfaction_')
    st.caption('_* Satisfaction is measured from 1 (completely satisfied) to 5 (very dissatisfied)_')
    satisfaction_levels = [1, 2, 3, 4, 5]
    Results = pd.DataFrame(['Rooms strategy'], columns=['Strategy'])
    for level in satisfaction_levels:
        column_name = [level]
        Results[column_name] = [f"{rooms['guest_satisfaction'].eq(level).sum():,}"]
    st.dataframe(Results.set_index('Strategy'))
    
    # Bar chart to visualize number of guests by level of satisfaction
    satisfaction = rooms.groupby('guest_satisfaction')['guest'].count().reset_index()
    st.bar_chart(data = satisfaction, x='guest_satisfaction', y='guest', color="#5f9ea0", width=100, height=400)

# If no strategy is selected in the select box, then a message is shown
else:
    st.subheader(':red[_**No strategy selected**_]')
    