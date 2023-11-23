# TRAVEL AROUND THE WORLD
NZKNG
## DATASET
The dataset we've been provided is built so that we can find in each line all the datas needed about the city.
## STRUCTURE OF THE PROJECT
The project is made by 5 different files, four of which are essential for the completion of the task prefixed.
The first file I'm gonna analize is called  `progett.py `. In this we can find the commands used to call the objects created in the other files, and so with this file we can have the "solution" of our work.  
The second file is  `path.py `, this one is the main and most important file in our project. In here I've created the class that allows us to complete the trip around the world, or the trip from one city to another. The final object, the one we "call" in  `progett.py `, returns to us the total distance in kilometers and the total amount of hours needed for this trip.    
Then we can move to  `mapping.py `, here we can find another class that allows us to create and then save the traced map of the cities visited in the process.           
In  `main.py` we find the code written in order to use and show on Streamlit the map or the list of cities studied in the other files.                                           
The last file,  `helpingfunction.py `, contains a single function that just simplifies and makes the code easier to read.
## SOLUTION
The solution I've come up with consist in analyzing the n closest cities on the east of the one I've decided to start with, and among these we're goin to choose the one that has the most similar latitude. With these procedure we're sure that, sooner or later, we're going to come back to the city. As for the time duration, I've decided that the trip takes 2 hours to get to a city among the n/3 closest, 4 hours if it's between n/3 and 2n/3, 6 hours for the lasts. In addition to this time we sum up 2 hours if the destination belongs to another country.