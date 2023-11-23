# Sentiment Analysis and WordCloud App Documentation

## Description

This Streamlit app combines sentiment analysis and word cloud generation to provide insights into textual data. Users can perform sentiment analysis on a provided text or upload a CSV file for sentiment analysis on a specific column. Additionally, users can generate a word cloud based on the uploaded CSV data and have it in colors of the uploaded image.

## Instructions

### Sentiment Analysis

#### Analyze Text

1) Users can input any custom text of preference in the provided text box. Enter text in the "Text here" box for direct analysis.
2) Clicking on the "Analyze Text" button will display the polarity and subjectivity of the provided text using the TextBlob library.

#### Analyze CSV

1) Users can upload a CSV file using the file uploader. Upload the final CSV(s) that we get after performing all operations with preprocessing of data (as it is written in the Jupyter Notebook). Upload a CSV file in the "Upload file" section for sentiment analysis on a column.
2) The app performs sentiment analysis on the chosen column of the CSV.
3) The sentiment score and analysis (Positive, Negative, Neutral) are added to the DataFrame and displayed.
4) Users can download the results as a CSV file. Download the results as a CSV file using the provided button.

### WordCloud Generation

#### Generate a WordCloud

1) Users can upload a CSV file containing text data. Upload a CSV file in the "Upload a CSV file" section.
2) After uploading, users select a text column for word cloud generation and upload a PNG image to define the word cloud shape. Upload a PNG image to define the shape of the word cloud.
3) The app generates a colored word cloud using the specified text column and shape image. The generated word cloud is displayed in an expandable section.

## Additional Instructions

1) During the execution of code in the Jupyter, I mentioned the need to download the data frames as CSV files for performing sentiment analysis and generating wordclouds. Use those files.
2) In this folder there is an png picture called "AC_Milan_Colors" which is used as a mask for wordcloud. Use this picture.

There might appear some problems with the opening of this app. I describe problems that I've encountered and how to deal with them to open the app without any problems.

1) Streamlit does not allow to open the app simply by writing `streamlit run sent_analysis_and_wordcloud.py`. Instead of the name of the file insert the path to the file. It worked for me.
2) Streamlit might also say that some packages (in my case it was `wordcloud`) are not imported. Just close the app by shuting donwn the app, writning `pip install name_of_the_package`, and opening app once again.

In case you do not want to open the app or you encounter problems, I add another Markdown file (`Results.md`) with screenshots of the app so you can view how it works.
