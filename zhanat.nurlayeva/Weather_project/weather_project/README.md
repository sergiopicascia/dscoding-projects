# Weather Project

## Overview

The Weather Project is a Python application designed for analyzing and visualizing temperature data for major cities over time. The project includes modules for data processing, routing, visualization, and a main script that integrates these modules into a Streamlit application.

## Project Structure

The project is organized into the following modules and packages:

### 1. Data Processing

- **Module:** `data_processor.py`
  - Contains functions for processing temperature data.
  
- **Module:** `utils.py`
  - Provides utility functions for data conversion.

### 2. Routing

- **Module:** `routing.py`
  - Defines the `Routing` class for calculating distances, finding closest cities, and determining the warmest route.

### 3. Visualization

- **Module:** `visualization.py`
  - Defines the `Visualization` class for plotting temperature data on a world map and creating temperature trend visualizations.

### 4. Main Application

- **Script:** `app.py`
  - Main script integrating data processing, routing, and visualization modules.
  - Utilizes Streamlit for creating a user interface and displaying visualizations.

## Project Packages

- **Package:** `packages`
  - Contains external data and resources.
    - `ne_110m_admin_0_countries.shp`: Shapefile for world map.
    - `GlobalLandTemperaturesByMajorCity.csv`: Dataset containing temperature data for major cities.

## Environment Setup

### 1. Python Virtual Environment

1. **Activate the virtual environment:**


   - On Windows:

     ```bash
     .\venv\Scripts\activate
     ```

   - On macOS/Linux:

     ```bash
     source venv/bin/activate
     ```

2. **Install required Python packages:**

   ```bash
   pip install -r requirements.txt

## Dependencies

To run this project, make sure you have the following dependencies installed:

- **pandas:** Data manipulation and analysis library. Install it using:

  ```bash
  pip install pandas
  
- **numpy:**  Numerical operations library. Install it using:

  ```bash
  pip install numpy

- **matplotlib:**  Plotting library. Install it using:

  ```bash
  pip install matplotlib

- **streamlit:**  Framework for creating web applications with minimal effort. Install it using:

  ```bash
  pip install streamlit

## Running the Application

1. **Navigate to the project directory:**

   ```bash
   cd path/to/weather_project

2. **Run the Streamlit application:**

   ```bash
   streamlit run app.py

3. **Open your browser and go to the provided URL (usually http://localhost:8501).**


**Notes:**

- The project may display performance warnings related to legend creation. Refer to the README for optimization suggestions.

**Author:**

- Zhanat Nurlayeva
- zhanat.nurlayeva@studenti.unimi.it
