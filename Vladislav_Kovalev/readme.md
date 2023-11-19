# Task:
## Hotels

### Dataset description: 
The dataset chosen for the project contains the following information:

- hotels.xlsx: number of vacant rooms and unit cost of each room for 400 hotels;
- guests.xlsx: discount fraction for 4000 potential customers;
- preferences.xlsx: order of hotel preference for each customer.

The program must calculate the allocation of customers at hotels, considering the number of available rooms, the fact that each customer occupies exactly one room, and that each stay lasts only one night. The price paid by the customer is the unit price of the room discounted by the fraction of the discount to which the customer is entitled.


### Program description
The program must implement four different allocation strategies:

- random: customers are randomly distributed to the rooms until the seats or customers are exhausted;
- customer preference: customers are served in order of reservation (the customer number indicates the order) and are allocated to the hotel based on their preference, until the seats or customers are exhausted;
- price: the places in the hotel are distributed in order of price, starting with the cheapest hotel and following in order of reservation and preference until the places or customers are exhausted;
- availability: places in hotels are distributed in order of room availability, starting with the most roomy hotel and subordinately in order of reservation and preference until places or clients are exhausted.

Finally, the program must present and display a report of the result obtained, showing for each strategy:
- the number of customers accommodated, 
- the number of rooms occupied, 
- the number of different hotels occupied, 
- the total volume of business (total earnings of each hotel)
- the degree of customer satisfaction (calculated according to the location of the hotel assigned to them with respect to their preferences).

### Project Requirements
Each project should present the following characteristics:

1. usage of *GitHub* - Done
2. correct modularization - Done
3. import and output of data - Main.py + utils.py - Done
4. usage of *pandas* (or alternative data manipulation library) - Done
5. usage of *numPy* (or alternative scientific computing library) - ./strategies/first_strategy/tools/random/random_choice_key_dict.py
6. usage of *matplotlib* (or alternative data visualization library) - ./viewer.ipynb
7. BONUS - usage of *streamlit* (or alternative web app creation framework) - ./results_tools/report_display/streamlit_display.py

## Execution
To execute this task, you need Python installed on your computer along with necessary libraries such as pandas, numpy, matplotlib, seaborn, etc.

### Calculation
vladislavkovalev@Vladislavs-Air dscoding-projects % cd vladislav_kovalev 
vladislavkovalev@Vladislavs-Air vladislav_kovalev % source venv/bin/activate
vladislavkovalev@Vladislavs-Air vladislav_kovalev % python3 main.py
10/18/2023 07:06:35 - WARNING - root -   Start 1 strategy calculating
10/18/2023 07:06:36 - WARNING - root -   Calculating is completed
10/18/2023 07:06:36 - WARNING - root -   Start 2 strategy calculating
10/18/2023 07:06:36 - WARNING - root -   Calculating is completed
10/18/2023 07:06:36 - WARNING - root -   Start 3 strategy calculating
10/18/2023 07:06:47 - WARNING - root -   Calculating is completed
10/18/2023 07:06:47 - WARNING - root -   Start 4 strategy calculating
10/18/2023 07:06:57 - WARNING - root -   Calculating is completed
10/18/2023 07:06:57 - WARNING - root -   Construct and save resulting files
10/18/2023 07:07:07 - WARNING - root -   Script completed
vladislavkovalev@Vladislavs-Air vladislav_kovalev % 

### Plot the streamlit report
vladislavkovalev@Vladislavs-Air vladislav_kovalev % streamlit run ./results_tools/report_display/streamlit_display.py
