
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

# Define functions for data loading and preprocessing
def load_data():
    # Loading the dataset from the CSV file (zoo.csv)
    data = pd.read_csv('zoo.csv')

    # Split data into features (X) and target labels (y)
    X = data.drop(columns=['class_type', 'animal_name'])
    y = data['class_type']

    return X, y

