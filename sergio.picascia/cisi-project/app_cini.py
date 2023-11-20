import streamlit as st
import pandas as pd
from cisi.data import CISIData
from cisi.methods import TermFrequencyRetrieval

def show_results(dataframe: pd.DataFrame):
    for _, row in dataframe.iterrows():
        st.write('---')
        st.markdown(f'**{row["title"]}**')
        st.write(f'{row["text"]}')
        st.markdown(f'*- {row["author"]}*')

PAGE_TITLE = 'CINI Search Engine'
PATH = '/Users/sergiopicascia/Downloads/archive'

st.set_page_config(
    page_title=PAGE_TITLE,
    layout='wide'
)
st.title(PAGE_TITLE)

search_field = st.selectbox(
    label='Search field',
    index=None,
    options=['title', 'author', 'text', 'query'],
    placeholder='Choose an option',
    label_visibility='hidden'
)

search_text = st.text_input(
    label='Search documents',
    value='',
    placeholder='Search documents...',
    label_visibility='collapsed'
)

data = CISIData(PATH)
tfretr = TermFrequencyRetrieval(method='topn', n=20)
tfretr.fit(data.documents['text'])

if search_field == 'query' and search_text:
    y_pred = tfretr.predict([search_text])[0]
    search_results = data.documents['id'].isin(y_pred)
    show_results(data.documents[search_results].head(20))
elif search_field and search_text:
    search_results = data.documents[search_field].str.contains(search_text)
    show_results(data.documents[search_results].head(20))
else:
    show_results(data.documents.head(20))
