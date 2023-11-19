import string 
from nltk.corpus import stopwords

class TextPreprocessor:
     
     def __init__(self, dataframe):
        self.dataframe = dataframe
     
     def text_to_lower_case(dataframe, column_name):
         dataframe[column_name] = dataframe[column_name].str.lower()
         return dataframe
     
     def remove_punctuations(dataframe, column_name):
         punctuations = string.punctuation
         additional_chars = ['…', '\\']
         all_chars_to_remove = punctuations + ''.join(additional_chars)
         dataframe[column_name] = dataframe[column_name].apply(lambda x: x.translate(str.maketrans('', '', all_chars_to_remove)))
         return dataframe
     
     def preprocess_text(dataframe, column_name):
          STOPWORDS = set(stopwords.words('english'))
          def remove_stopwords(text):
              return " ".join([word for word in text.split() if word not in STOPWORDS])
          dataframe[column_name] = dataframe[column_name].apply(remove_stopwords)
          return dataframe