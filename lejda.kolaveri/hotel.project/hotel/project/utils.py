def calculate_satisfaction_percentage(guest_id, hotel_id, preferences):
    guest_preferences = preferences[preferences['guest'] == guest_id].reset_index()

    if guest_preferences.empty:
        # No preferences, so 100% satisfaction
        return 100

    is_hotel_one_of_preferred = hotel_id in guest_preferences['hotel'].values

    if is_hotel_one_of_preferred:
        index_of_preference = guest_preferences['hotel'].eq(hotel_id).idxmax()
        guest_preferences_count = len(guest_preferences)
        return round(((guest_preferences_count - index_of_preference) / guest_preferences_count) * 100)
    else:
        # Guest settled for a not preferred hotel, so 0% satisfaction
        return 0




