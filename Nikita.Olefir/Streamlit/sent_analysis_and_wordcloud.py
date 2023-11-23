from textblob import TextBlob
import pandas as pd
import streamlit as st
from wordcloud import WordCloud, ImageColorGenerator
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

st.header("Sentiment Analysis and WordCloud")

st.subheader("Sentiment Analysis")
with st.expander("Analyze Text"):
    text = st.text_input("Text here: ")
    if text:
        blob = TextBlob(text)
        st.write("Polarity: ", round(blob.sentiment.polarity, 2))
        st.write("Subjectivity: ", round(blob.sentiment.subjectivity, 2))

with st.expander("Analyze CSV"):
    upl = st.file_uploader('Upload file')

    if upl is not None:
        try:
            df = pd.read_csv(upl)
            selected_column = st.selectbox("Select a text column for sentiment analysis", df.columns)

            def score(x):
                if pd.notna(x) and isinstance(x, str):
                    blob1 = TextBlob(x)
                    return blob1.sentiment.polarity
                else:
                    return 0

            def analyze(x):
                if x >= 0.5:
                    return 'Positive'
                elif x <= -0.5:
                    return 'Negative'
                else:
                    return 'Neutral'

            df['score'] = df[selected_column].apply(score)
            df['analysis'] = df['score'].apply(analyze)

            st.write(df.head(10))

            @st.cache_data
            def convert_df(df):
                return df.to_csv().encode('utf-8')

            csv = convert_df(df)

            st.download_button(
                label="Download a CSV file",
                data=csv,
                file_name='sentiment_analysis_results.csv',
                mime='text/csv',
            )

        except pd.errors.EmptyDataError:
            st.error("The uploaded CSV file is empty.")

def generate_colored_wordcloud(dataframe, text_column, shape_image):
     text = ' '.join(dataframe[text_column].astype(str).fillna(''))
     mask = np.array(Image.open(shape_image))
     colormap = ImageColorGenerator(mask)
     wordcloud = WordCloud(mask=mask, background_color='white', width=800, height=400).generate(text)
     wordcloud.recolor(color_func=colormap)
     fig, ax = plt.subplots(figsize=(10, 5))
     ax.imshow(wordcloud, interpolation='bilinear')
     ax.axis('off')
     st.pyplot(fig)

st.subheader("WordCloud")
with st.expander("Generate a WordCloud"):
         uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])
         if uploaded_file is not None:
              df = pd.read_csv(uploaded_file)
              st.write("Uploaded DataFrame:")
              st.write(df)
              selected_column = st.selectbox("Select a text column for Word Cloud", df.columns)
              shape_image = st.file_uploader("Upload a PNG image for Word Cloud shape", type=["png"])
              if shape_image is not None:
                   generate_colored_wordcloud(df, selected_column, shape_image)
         
    