import pandas as pd

def allocation_analysis(allocation):
    print('Customers accomodated:', allocation['guest_id'].count())
    #it should be the same :) maybe recalculate it just to compare ?
    print('Number of rooms occupied:', allocation['guest_id'].count())
    print('Number of different hotels occupied:', allocation['hotel_id'].nunique())
    print('Average satisfaction:', round(allocation['satisfaction_percentage'].mean(),2))
    total_earnings = allocation[['hotel_id', 'paid_price']].copy()
    print('Total earnings per hotel:', total_earnings.groupby('hotel_id').sum(), sep='\n')


