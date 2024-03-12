import streamlit as st
from subprocess import call
import pandas as pd


def start_scraping(page):
    call(["python3","scrape.py",f"{page}"])
    return "success"

def download_file(dataframe):
    def convert_df(df):
        return df.to_csv(index=False).encode('utf-8')
    return convert_df(dataframe)

def clear_data(df):
    empty_df=df.iloc[0:0]
    empty_df.to_csv("output.csv", index=False)
    
    return empty_df

st.title('Ebooks toScrape')

df=pd.read_csv("output.csv")

with st.form(key='user_info'):
    page=st.number_input("How many pages you want to scrape ?",1,100)
    submit_from = st.form_submit_button(label="Submit", help="Start scraping")
    if submit_from:
        clear_data(df)
        start_scraping(page)

df=pd.read_csv("output.csv")
 
column1, column2 = st.columns([1,1])

with column1:
    clear_button= st.button('Clear', type='primary')

with column2:
    csv=download_file(df)
    
    st.download_button(
        label="Download csv",
        data=csv,
        file_name=f"Books-data-from-page-1-to-{page}.csv",
        mime='text/csv',
        type='secondary'
    )
    
if clear_button:
    df=clear_data(df)
    st.dataframe(df)
else:
    st.dataframe(df)