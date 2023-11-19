# Humor Detection Project

## Overview

The Humor Detection Project aims to predict whether a given text is humorous or not using machine learning techniques. The project includes data loading, preprocessing, vectorization, model training, and a Streamlit web application for user interaction.

## Data

The project utilizes a dataset with 200,000 observations, each containing a text sample and a flag indicating whether the text is humorous or not.

## Project Structure

The project is structured as follows:

- **main.py**: Script for:
  - loading and visualizing data,
  - preprocessing and vectorizing text using Count Vectorizer and TF-IDF Vectorizer,
  - training and evaluating two machine learning models, i.e., Multinomial Naive Bayes and Logistic Regression with Stochastic Gradient Descent,
  - saving the trained vectorizers and models.

- **main-jupyter.ipynb**: Jupyter Notebook version of `main.py`.

- **UDFs.py**: Script containing two classes:
  - `TextPreprocessor`: class for preprocessing text data,
  - `AppTextClassifier`: class for text classification using pre-trained models.

- **app.py**: Script for the Humor Detection App.

## Humor Detection App

The Humor Detection App allows users to interactively predict the humor in a given text. Users can choose between different classifiers (Logistic Regression or Multinomial Naive Bayes) and vectorizers (Count Vectorizer or TF-IDF Vectorizer). The app leverages machine learning models trained on a dataset of 200,000 observations to provide predictions.