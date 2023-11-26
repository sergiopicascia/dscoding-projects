# Explore the Financial Markets

The financial world has long been considered a complex reality, accessible only to a chosen few. Nevertheless, it is an integral part of everyday life, and many dynamics that unfold in the surrounding environment originate or develop from financial markets. This project is designed to explore the trends of financial securities listed on NASDAQ without requiring prior knowledge. With the provided guidance, you can intuitively discover the world of financial analysis, even if you are a beginner.

## Overview

Observe monthly value charts over a decade to understand how assets move. Use the key metrics provided:

- Follow Average Returns: See how securities have performed over time. With easily understandable charts, you can quickly assess if your investments are heading in the right direction.

- Understand Volatility: Volatility may seem complicated, but a clear view of price fluctuations is offered. This information will help you better assess the risk associated with your investments.

- Observe Trading Volume: Discover when there is more buying or selling activity. This can give you an idea of how other investors are behaving and guide your decisions.

## Dataset

The dataset used is available on Kaggle: [link](https://www.kaggle.com/code/jacksoncrow/download-nasdaq-historical-data/notebook). Follow the instructions on the webpage. For this project, the first 3000 securities with a decade-long timeframe were considered.

## Project Structure

The project consists of the following main files and folders:

- 'Data': The folder contains the dataset divided into two tables, 'etfs' and 'stocks'.

- 'main.py': This file contains functions used to calculate the necessary financial metrics for analysis.

- 'webbe.py': This file contains the code that enables the Streamlit web page to function.

## Visualizing Interactive Charts

To view the interactive web page, simply run the following command:

```
streamlit run webbe.py
```
Customize your experience: Choose the securities that interest you and discover their trends over time.
