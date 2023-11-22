import pandas as pd
import numpy as np
from statistics import NormalDist
import matplotlib.pyplot as plt
from pandasgui import show

class rating:
    def __init__(self, path):
        self.bgg = pd.read_csv(path)  # Read the data from the CSV file into a Pandas DataFrame
        # Drop rows with missing values and sort the DataFrame by game id
        self.bgg = self.bgg.dropna().sort_values(by= ['game']).reset_index(drop = True)
        self.bgg = self.bgg[0:100000] # Select the first 100,000 rows
        self.counting = self.bgg.groupby(['game']).count() # Count number of votes for each game.
        self.title = self.bgg.groupby('game')['title'].first()

    def compute_avg_rating (self):
        self.avg_rating = self.bgg.groupby(['game']).mean('rating') # Compute the average rating for each game
        self.avg_rating = self.avg_rating.sort_values(by=['rating'], ascending = False)

    def compute_geek_rating (self):
        self.l= int(self.bgg.shape[0]) # Save the number of rows
        c = self.l
        bgg1 = self.bgg
        for i in range (0, self.l): # For each game, add 5.5 as the rating for the current game, 5 times
            if bgg1.game.loc[i] != bgg1.game.loc[i+1]:
                for j in range (0,5):
                    bgg1.loc[c] = [bgg1.game.loc[i],bgg1.title.loc[i], 5.5]
                    c += 1
        self.geek_rating = bgg1.groupby(['game']).mean('rating')  # Calculate the mean rating for each game
        self.geek_rating = self.geek_rating.sort_values(by = ['rating'], ascending = False)
        self.bgg = self.bgg[0:self.l] # Reset the original DataFrame to the original length

    def compute_new_rating(self):
        K = 20 # Number of possible ratings
        sk = np.arange(start = 0.5, stop = 10.5, step = 0.5) # List of possible ratings
        alfa = 0.1
        z = NormalDist().inv_cdf(1-alfa/2)
        start = 0
        self.bgg.loc[self.l] = [0,0,0]
        self.new_rating = []
        for x in range (0,self.l):
            if self.bgg.game.loc[x] == self.bgg.game.loc[x+1]:
                continue
            else:
                bgg2 = self.bgg[start:x+1] # Extract a subset of the DataFrame for the current game
                nk = [] # Number of votes for each value in sk
                for i in sk: # Count occurrences of ratings in sk for the current game
                    counter = 0
                    for j in range (start,x+1):
                        if i == bgg2.rating.loc[j]:
                           counter += 1
                    nk.append(counter)
                N = bgg2.groupby(['game']).count().rating.to_numpy()[0] # Total number of ratings for the current game
                sum = 0 # Apply the formula for Bayesian approximation
                for i in range (0,K):
                    a = sk[i]*((nk[i]+1)/(N+K))
                    sum += a
                sum1 = 0
                for i in range (0,K):
                    b = (sk[i]**2)*((nk[i]+1)/(N+K))
                    sum1 += b
                S = sum - z * (np.sqrt((sum1-(sum**2))/(N+K+1))) # Calculate new rating for the current game
                self.new_rating.append([self.bgg.game.loc[x],S]) # Append the new rating for the current game to the list
                start = x+1
        # Convert the list to a NumPy array and then to a DataFrame
        self.new_rating = np.array(self.new_rating)
        self.new_rating = pd.DataFrame(self.new_rating)
        self.new_rating[0] = self.new_rating[0].astype(int)
        self.new_rating = self.new_rating.set_index(0)
        self.new_rating.columns = ['New_rating']
        self.new_rating = self.new_rating.sort_values(by = 'New_rating',ascending = False)

    def create_ranking(self, sort_by = 'Average_rating'):
        # Combine relevant attributes into a new DataFrame
        self.result = pd.concat([self.title, self.avg_rating, self.geek_rating, self.new_rating, self.counting.rating], axis=1)
        self.result.columns = ['Game','Average_rating','Geek_rating', 'New_rating','Number_of_ratings'] # Rename columns
        # Sort the DataFrame based on the specified column and in descending order
        self.result = self.result.sort_values(by=sort_by, ascending=False).reset_index(drop = True)
        # Reset the index and increment it by 1 for a more intuitive ranking display starting from 1 instead of 0
        self.result.index += 1

    def visualize_ranking(self):
        self.table = show(self.result)

    def get_info(self, identifier, by='index'):
        try:
            if by == 'index': # Retrieve information based on the specified ranking position
                row = self.result.loc[identifier]
                return(f"{identifier}° position:\n{row}")
            elif by == 'title': # Retrieve information based on the specified game title
                row = self.result.loc[self.result.Game == identifier]
                position = row.index[0]
                row = row.iloc[0]
                return(f"{position}° position:\n{row}")
            else: # Return an error message for an invalid 'by' parameter
                return("Error: Invalid value for 'by' parameter. Use 'index' or 'title'.")
        except: # Return an error message if the identifier doesn't exist in the DataFrame
            return(f"Error: {identifier} doesn't exist in DataFrame.")

class graphs:
    def __init__(self):
        pass

    def compare_methods (self,result):
        lenght = int(result.shape[0]) # Calculate the length of the result DataFrame
        x_values = np.arange(start=1, stop=lenght+1, step=1) # Generate x-axis values from 1 to the length of the DataFrame
        # Extract rating values for each method from the result DataFrame
        y1_values = result.Average_rating.to_numpy()
        y2_values = result.Geek_rating.to_numpy()
        y3_values = result.New_rating.to_numpy()
        # Plot the ratings for each method
        plt.figure(figsize=(15, 10))
        plt.plot(x_values, y1_values, label='Average rating')
        plt.plot(x_values, y2_values, label='Geek rating')
        plt.plot(x_values, y3_values, label='New rating')
        # Add labels, title, legend, and grid to the plot
        plt.xlabel('Position')
        plt.ylabel('Rating')
        plt.title('Rating methods comparison')
        plt.legend()
        plt.grid(True)
        plt.show()

    def create_scatterplot(self, result, plot_avg=True, plot_avg_geek=True, plot_new=True):
        # Create a scatter plot comparing ratings against the number of ratings
        plt.figure(figsize=(8, 6))
        # Plot specified rating method
        if plot_avg:
            plt.scatter(result.Average_rating, result.Number_of_ratings, s=15, c='blue', alpha=0.5, label='Average Rating')
        if plot_avg_geek:
            plt.scatter(result.Geek_rating, result.Number_of_ratings, s=15, c='red', alpha=0.5, label='Geek Rating')
        if plot_new:
            plt.scatter(result.New_rating, result.Number_of_ratings, s=15, c='green', alpha=0.5, label='New Rating')
        # Add labels, title, grid, and legend to the plot
        plt.xlabel('Rating')
        plt.ylabel('Number of Ratings')
        plt.title('Rating vs. Number of Ratings')
        plt.grid(True)
        plt.legend()
        plt.show()

    def create_pie_chart(self,result,selected):
        try:
            avg = result[selected].to_numpy() # Extract the selected values from the result DataFrame
            # Define parameters for ranges
            num_ranges = 10
            max_value = max(avg)
            min_value = min(avg)
            range_width = (max_value - min_value) / num_ranges
            rating_ranges = [(min_value + i * range_width, min_value + (i + 1) * range_width) for i in range(num_ranges)]
            categories = [0] * len(rating_ranges)
            for rating in avg: # Count games in each range
                for i, (start, end) in enumerate(rating_ranges):
                    if start <= rating < end:
                        categories[i] += 1
                        break
            total_games = len(avg)
            percentages = []  # Calculate the percentage of games in each range
            for category in categories:
                percentages.append(category / total_games * 100)
            # Create labels for the ranges and define colors for the pie chart
            labels = [f"{round(start,3)}-{round(end,3)}" for start, end in rating_ranges]
            colors = ['red', 'lightgreen', 'yellow', 'blue', 'purple', 'orange', 'lightblue', 'pink', 'silver', 'green']
            # Create the pie chart
            plt.pie(percentages, labels=None, colors=colors, autopct='', startangle=140)
            plt.axis('equal')
            # Create legend labels with range and percentage and add it to the plot
            legend_labels = [f"{label} - {percent:.1f}%" for label, percent in zip(labels, percentages)]
            plt.legend(legend_labels, loc='best', bbox_to_anchor=(1, 1))
            if selected == 'Number_of_ratings':
                plt.title('Distribution of Games by number of ratings')
            else:
                plt.title('Distribution of Games by rating range')
            plt.show()
        except:
            print("Error: Invalid value for 'selected' parameter. Use 'Average_rating', 'Geek_rating', 'New_rating' or 'Number_of_ratings'")
