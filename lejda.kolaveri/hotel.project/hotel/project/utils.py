import pandas as pd
import numpy as np

class Satisfaction:
    def calculate_satisfaction_percentage(preferences, guest_id, hotel_id):
        guest_preferences = preferences[preferences['guest'] == guest_id].reset_index() #filter preferences for the given guest
        if guest_preferences.empty:
            return 100  # No preferences, 100% satisfaction

        index_of_preference = (guest_preferences['hotel'] == hotel_id).idxmax() # Find the index of the allocated hotel in the guest's preferences
        satisfaction = round(((len(guest_preferences) - index_of_preference) / len(guest_preferences)) * 100)
        return satisfaction if satisfaction >= 0 else 0



