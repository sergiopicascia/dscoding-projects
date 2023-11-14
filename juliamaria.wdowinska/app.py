import joblib
import streamlit as st
from UDFs import preprocess

# Load the trained vectorizer and model
vectorizer = joblib.load('vectorizer.joblib')
mnb_classifier = joblib.load('mnb_classifier.joblib')

# User-defined text (app)
st.set_page_config(page_title = 'Humor Detection App', layout = 'wide')

st.markdown("""
            <style>
            .reportview-container {margin-top: -2em;}
            #MainMenu {visibility: hidden;}
            .stDeployButton {display:none;}
            footer {visibility: hidden;}
            #stDecoration {display:none;}
            </style>
            """,
            unsafe_allow_html = True)

st.title('Humor Detection App')
st.markdown('''
            This app uses a Multinomial Naive Bayes classifier to predict if your text is humorous or not.  
            The classifier was trained using a set of 200 000 humorous and unhumorous texts.
            '''
            )

user_text = st.text_input('Enter text:')

# Preprocess 'text', vectorize and predict humor using MNB classifier
user_text1 = vectorizer.transform([preprocess(user_text)])

if st.button('Detect Humor'):
      user_prediction = mnb_classifier.predict(user_text1)
      st.write('Your text is humorous.' if user_prediction[0] == 1 else 'Your text is unhumorous.')

st.markdown('''
            Sample texts:  
            (H) Why don't Calculus majors throw house parties? Because you should never drink and derive.   
            (H) What did the shark say when he ate the clownfish? This tastes a little funny.  
            (NH) There were some heated exchanges on Ukraine and China, but strict moderation limited direct clashes.  
            (NH) Brazilian authorities made two arrests and carried out raids in key cities including Sao Paulo and Brasilia.
            '''
            )