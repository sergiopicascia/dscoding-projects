{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 3,
   "id": "7f8bee54-72ce-4ac1-83cd-0d74e17b8724",
   "metadata": {},
   "outputs": [],
   "source": [
    "import pandas as pd\n",
    "import numpy as np"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "c250f539-9e8d-4bb3-b903-0fa77c41cdd3",
   "metadata": {},
   "outputs": [],
   "source": [
    "def allocate_and_calculate(hotels, guests, preferences):\n",
    "    \"\"\" this function allocates guests to their preferred hotels,\n",
    "    calculates the paid price, satisfaction, and returns the allocation information as a list\n",
    "    \"\"\"\n",
    "    allocation_list = []\n",
    "\n",
    "    for guest_id, guest_row in guests.iterrows():\n",
    "        guest_preferred_hotels = preferences[preferences['guest'] == guest_id]['hotel']\n",
    "\n",
    "        for _, preferred_hotel_id in guest_preferred_hotels.items():\n",
    "            preferred_hotel_row = hotels.loc[preferred_hotel_id]\n",
    "\n",
    "            if preferred_hotel_row['rooms'] > 0:\n",
    "                preferred_hotel_row['rooms'] -= 1\n",
    "\n",
    "                paid_price_coefficient = 1 - guest_row['discount']\n",
    "                paid_price = preferred_hotel_row['price'] * paid_price_coefficient\n",
    "\n",
    "                satisfaction = calculate_satisfaction_percentage(guest_id, preferred_hotel_id, preferences)\n",
    "\n",
    "                allocation_entry = [guest_id, preferred_hotel_id, satisfaction, paid_price]\n",
    "                allocation_list.append(allocation_entry)\n",
    "\n",
    "                break  # Break to the next guest after successful allocation\n",
    "\n",
    "    return allocation_list"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3 (ipykernel)",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.11.4"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
