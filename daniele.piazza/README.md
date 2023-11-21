# Weather Dataset Visualization

This dataset captures temperature records worldwide dating back to 1750. The project's objective is to create a graphical representation of the temperature changes over the years.

  

## Web Application Overview

The web application comprises fours distinct pages, each serving a unique purpose:

  

### 1. Overview Cities Page

This page provides a comprehensive view of temperature trends by city. Users can explore the temperature range and observe how temperatures have fluctuated across the world since 1750.

  

### 2. City-specific Page

On this page, users can select a specific city to access detailed information. The available data includes the city's location, temperature trends over the years, predictions, monthly temperature variations, and the ability to focus on a particular year.

### 3. Overview Countries Page

This page provides a comprehensive view of temperature trends by country. Users can explore the temperature range and observe how temperatures have fluctuated across the world since 1750.
  

### 4. Country-specific Page

On this page, users can select a specific country to access detailed information. The available data includes temperature trends over the years, predictions, monthly temperature variations, and the ability to focus on a particular year.


## Installation

To set up the project and install all required dependencies, use the following Poetry command:

```
poetry install
```

  

## Running the Application

Execute the following command to launch the web application:

```

streamlit run app.py

```

  

## Dataset


The dataset used in this project is available on Kaggle: https://www.kaggle.com/datasets/berkeleyearth/climate-change-earth-surface-temperature-data/data add it to the `Data` folder.

  

## First Steps

The first time you run the application change to true update and html variable. After that, change it back to false and run the application again.

  

## Project Structure

The project comprises the following files and folders:

-  `stream.py`: This is the main Python file that contains the Streamlit code to run the web application.

-  `data`: This folder contains the dataset used in the project.

-  `visualize.py`: This file contains the code to generate the visualizations.

-  `location.py`: This file contains the code to generate the coordinates of the cities and transform the dataset.


## Change theme

To change the theme of the application, go to the folder .streamlit and change the file config.toml, the app will automatically update the theme, also for the graphs.