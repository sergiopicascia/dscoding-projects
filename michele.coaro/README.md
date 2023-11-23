# Weather Project
#### Michele Coaro

## Task

The task consisted in, once given a dataset containing average temperatures for
different cities and countries around the world, to provide effective visualization of the data.

## Solution
My solution consists in a web application, which allows the user to select the database he/she wants to use, and then provides a series of visualizations of the data.
It is composed of different parts, mostly coded through the use of python libraries such as Pandas, Numpy, Seaborn and others.
It is then shaped as a web application through the use of Streamlit.

## Structure

The project is written in different files, which are:

* **main.py**: contains the code used to run the web application
* **classes.py**: contains the classes used to structure the data
* **The Datasets** used for the project

The project is structured in the following way:

#### Introductory page

A very basic, yet effective, landing page, which allows the user to select it's preferred database.

#### Data selection
Data selection is done through the use of a sidebar, which allows the user to select between **Major Cities**, **All Cities** and **Countries**.

#### Cities Page
The Major Cities and All (obviously hyperbolic) Cities pages are structured the same way, as they display the same type of data, just extracted from
different datasets.

The first choice for the user is whether to display the **dataframe** and/or the **map**, which is the main course of this pages.

Moreover, the page is enriched with a series of visualizations, which are intended to emphasize the distribution of data, rather than individual
specificities. This is due to the size of the dataset, which allows for confrontation over vast timeframes, while lacking granularity in shorter timeframes.

These visualizations are:

1. Histogram comparison
2. Scatter plot
3. Bee Swarm plot
4. Line Plot

#### Countries Page
The Countries page is structured similarly to the cities pages.
The data visualzations available are:

1. Histogram comparison
2. Monthly Temperature Line Plot
3. A ridge plot for yearly temperature distribution across continents


## How to run
Once the project has been setup to poetry through the use of the command `poetry install`, it can be run using `streamlit run main.py`

## Datasets
The datasets used are retrieved from the following sources:
https://www.kaggle.com/datasets/berkeleyearth/climate-change-earth-surface-temperature-data/
(Specifically, GlobalLandTemperaturesByMajorCity, GlobalLandTemperaturesByCity and GlobalLandTemperaturesByCountry)




