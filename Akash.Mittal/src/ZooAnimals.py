#!/usr/bin/env python
# coding: utf-8

# In[1]:


# This File is for extracting feature data-points from the excel file using openpyxl and pandas.  


# In[2]:


import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


# In[3]:


class DataProcessor():                    # DataProcessor class for importing the data and processing the initial files
    def __init__(self, file_path):
        self.file_path = file_path
        self.data = None                  # Initialization the blank dataframe in class
        
    def import_data(self):                # Improting the data file
        try:
            self.data = pd.read_excel(self.file_path)
            print("File Read OK.")
        except Exception as e:
            print(f"Error in File Read: {e}")
            
    def output_data_structure(self):      # Function to Output the Column Names and a Brief Overview of the DataSet
        if self.data is not None:         # This can be skipped also as the self.data dataframe can be used for same purpose
            print("The Columns/ Attributes/ Features are :")
            for column_name in self.data.columns:
                print(column_name)
            print("A short Summary of Data Table: ")
            data_tibble = self.data
        else:
            print("Check input data.")
            data_tibble = None
        return data_tibble

    def drop_column(self, column_name):    #Function to Drop a specific Column
        if self.data is not None:
            self.data = self.data.drop(column_name, axis = 1)
            print(f"Column '{column_name}' dropped successfully")
        else:
            print("data not available or wrong column name.")
        
    def create_pair_plot(self):            # Function to create Pair-Wise Scatter PLots
        if self.data is not None:
            sns.pairplot(self.data, kind='scatter', plot_kws={'alpha':0.5})
            plt.suptitle('Pair Plot of Animal Features', y=1.03)
            plt.show()
        else:
            print("Check input data.")


# In[4]:


class DataValidation():                    # Class to load the class types for comaprison with our output, not part of current project, will use later on.
    def __init__(self, file_path):
        self.file_path = file_path
        self.data = None
    def import_data(self):
        try:
            self.data = pd.read_excel(self.file_path)
            print("File Read OK.")
        except Exception as e:
            print(f"Error in File Read: {e}")


# In[ ]:





# In[5]:


#file_path = r"C:\Users\Akash Mittal\Documents\Zoo_Lab\zoo.xlsx" #File Path of the Input File with Features of Animals


# In[6]:


#dataprocess = DataProcessor(file_path) #Creating an Object of the DataProcessor Class with data used for analysis


# In[7]:


#dataprocess.import_data() # Imporitng Data


# In[8]:


#dataprocess.output_data_structure() # Data Structure Output 


# In[ ]:





# In[9]:


#dataprocess.drop_column('class_type') # Dropping the Class_type column


# In[10]:


#print(dataprocess.data)


# In[11]:


#dataprocess.output_data_structure() # Data Structure Output 


# In[12]:


#print(dataprocess.data)


# In[13]:


# dataprocess.create_pair_plot() # It creates a Pairwise Scatter Plot of the Data Points


# In[ ]:




