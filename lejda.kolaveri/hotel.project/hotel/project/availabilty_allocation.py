{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 1,
   "id": "c5631147-eff2-436f-89e3-4103397134f9",
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
   "execution_count": 8,
   "id": "d924d449-c9d2-479d-b5fe-2634aea90f0d",
   "metadata": {
    "tags": []
   },
   "outputs": [
    {
     "ename": "NameError",
     "evalue": "name 'preferences' is not defined",
     "output_type": "error",
     "traceback": [
      "\u001b[1;31m---------------------------------------------------------------------------\u001b[0m",
      "\u001b[1;31mNameError\u001b[0m                                 Traceback (most recent call last)",
      "Cell \u001b[1;32mIn[8], line 1\u001b[0m\n\u001b[1;32m----> 1\u001b[0m \u001b[38;5;28;01mclass\u001b[39;00m \u001b[38;5;21;01mAllocationHelper\u001b[39;00m:\n\u001b[0;32m      2\u001b[0m     \u001b[38;5;28;01mdef\u001b[39;00m \u001b[38;5;21mcan_allocate_to_hotel\u001b[39m(hotel_row, guest_id, preferences):\n\u001b[0;32m      3\u001b[0m         \u001b[38;5;28;01mreturn\u001b[39;00m hotel_row[\u001b[38;5;124m'\u001b[39m\u001b[38;5;124mrooms\u001b[39m\u001b[38;5;124m'\u001b[39m] \u001b[38;5;241m>\u001b[39m \u001b[38;5;241m0\u001b[39m \u001b[38;5;129;01mand\u001b[39;00m guest_id \u001b[38;5;129;01mnot\u001b[39;00m \u001b[38;5;129;01min\u001b[39;00m preferences\u001b[38;5;241m.\u001b[39mindex\n",
      "Cell \u001b[1;32mIn[8], line 10\u001b[0m, in \u001b[0;36mAllocationHelper\u001b[1;34m()\u001b[0m\n\u001b[0;32m      7\u001b[0m     \u001b[38;5;28;01mreturn\u001b[39;00m hotel_row[\u001b[38;5;124m'\u001b[39m\u001b[38;5;124mprice\u001b[39m\u001b[38;5;124m'\u001b[39m] \u001b[38;5;241m*\u001b[39m paid_price_coefficient\n\u001b[0;32m      9\u001b[0m \u001b[38;5;28;01mfrom\u001b[39;00m \u001b[38;5;21;01mutils\u001b[39;00m \u001b[38;5;28;01mimport\u001b[39;00m Satisfaction\n\u001b[1;32m---> 10\u001b[0m Satisfaction\u001b[38;5;241m.\u001b[39mcalculate_satisfaction_percentage(preferences, guest_id, hotel_id)\n",
      "\u001b[1;31mNameError\u001b[0m: name 'preferences' is not defined"
     ]
    }
   ],
   "source": [
    "class AllocationHelper:\n",
    "    def can_allocate_to_hotel(hotel_row, guest_id, preferences):\n",
    "        return hotel_row['rooms'] > 0 and guest_id not in preferences.index\n",
    "\n",
    "    def calculate_paid_price(hotel_row, guest_row):\n",
    "        paid_price_coefficient = 1 - guest_row['discount']\n",
    "        return hotel_row['price'] * paid_price_coefficient\n",
    "\n",
    "    from utils import Satisfaction\n",
    "    Satisfaction.calculate_satisfaction_percentage(preferences, guest_id, hotel_id)\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 9,
   "id": "9d8df26c-6c09-44ce-8ae4-a59b3bc00ecf",
   "metadata": {
    "tags": []
   },
   "outputs": [],
   "source": [
    "class AvailabilityBasedAllocator:\n",
    "    def __init__(self, hotels, guests, preferences):\n",
    "        # Use copies to avoid modifying the original DataFrames\n",
    "        self.hotels = hotels.copy()\n",
    "        self.guests = guests.copy()\n",
    "        self.preferences = preferences.copy()\n",
    "\n",
    "    def allocate_and_calculate(self):\n",
    "        allocation_list = []\n",
    "\n",
    "        # Sort hotels based on available rooms (desc order)\n",
    "        sorted_hotels = self.hotels.sort_values(by='rooms', ascending=False)\n",
    "\n",
    "        for hotel_row in sorted_hotels.iterrows():\n",
    "            allocated_guests = set()  # Track guests already allocated to the current hotel\n",
    "            for guest_row in self.guests.iterrows():\n",
    "                guest_id = guest_row['guest_id']\n",
    "\n",
    "                # Check if the guest can be allocated to the current hotel\n",
    "                if AllocationHelper.can_allocate_to_hotel(hotel_row, guest_id, self.preferences) and guest_id not in allocated_guests:\n",
    "                    paid_price = AllocationHelper.calculate_paid_price(hotel_row, guest_row)\n",
    "                    satisfaction = AllocationHelper.calculate_satisfaction_percentage(guest_id, hotel_row.name, self.preferences)\n",
    "                    allocation_entry = [guest_id, hotel_row.name, satisfaction, paid_price]\n",
    "                    allocation_list.append(allocation_entry)\n",
    "\n",
    "                    # Update the set of allocated guests for the current hotel\n",
    "                    allocated_guests.add(guest_id)\n",
    "\n",
    "        return pd.DataFrame(allocation_list, columns=['guest_id', 'hotel_id', 'satisfaction', 'paid_price'])\n",
    "\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "805b3f24-c227-4284-be08-76c3936016d9",
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
