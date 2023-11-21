{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 1,
   "id": "e422890e-5612-4a44-8e3c-f7a6ed3b46a2",
   "metadata": {
    "tags": []
   },
   "outputs": [],
   "source": [
    "import pandas as pd"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 2,
   "id": "7a9c82f7-122f-4d94-8e19-1e869af5cf54",
   "metadata": {
    "tags": []
   },
   "outputs": [],
   "source": [
    "class PriceBasedAllocator:\n",
    "    def __init__(self, hotels, guests, preferences):\n",
    "        self.hotels = hotels\n",
    "        self.guests = guests\n",
    "        self.preferences = preferences\n",
    "\n",
    "    def allocate_and_calculate(self):\n",
    "        allocation_list = []\n",
    "\n",
    "        # Sort hotels based on price (ascending order)\n",
    "        sorted_hotels = self.hotels.sort_values(by='price')\n",
    "\n",
    "        for hotel_id, hotel_row in sorted_hotels.iterrows():\n",
    "            for guest_id, guest_row in self.guests.iterrows():\n",
    "                if self.can_allocate_to_hotel(hotel_row, guest_id):\n",
    "                    paid_price = self.calculate_paid_price(hotel_row, guest_row)\n",
    "                    satisfaction = self.calculate_satisfaction_percentage(guest_id, hotel_id)\n",
    "                    allocation_entry = [guest_id, hotel_id, satisfaction, paid_price]\n",
    "                    allocation_list.append(allocation_entry)\n",
    "                    break  # Break to the next hotel after successful allocation\n",
    "\n",
    "        return pd.DataFrame(allocation_list, columns=['guest_id', 'hotel_id', 'satisfaction', 'paid_price'])\n",
    "\n",
    "    def can_allocate_to_hotel(self, hotel_row, guest_id):\n",
    "        # Check if the hotel has available rooms and guest has not been allocated yet\n",
    "        return hotel_row['rooms'] > 0 and guest_id not in self.preferences.index\n",
    "\n",
    "    def calculate_paid_price(self, hotel_row, guest_row):\n",
    "        paid_price_coefficient = 1 - guest_row['discount']\n",
    "        return hotel_row['price'] * paid_price_coefficient\n",
    "\n",
    "    def calculate_satisfaction_percentage(self, guest_id, hotel_id):\n",
    "        pass\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "05554c94-bdd8-4124-b52b-d002fd9adbd2",
   "metadata": {},
   "outputs": [],
   "source": []
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
