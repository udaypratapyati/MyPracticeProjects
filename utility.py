'''
@Author : uday pratap yati
'''

import streamlit as st
import numpy as np
import pandas as pd 
import base64

CSS_FILE = 'css/style.css'

def get_multiple_download_links(df):
    MAX_RECORDS = 50000
    length = df.shape[0]
    st.write(df.shape)

    length = df.shape[0] // MAX_RECORDS
    if df.shape[0] % MAX_RECORDS :
        length = length + 1

    st.write(f'len = {length}')

    string = ""
    for i in range(length):
        start = i * MAX_RECORDS
        end = start + MAX_RECORDS + 1
        csv = df.iloc[start:end, :].to_csv(index=False)
        string = string + (f'<a href="data:file/csv;base64,{base64.b64encode(csv.encode()).decode()}" download="myfilename_{i+1}.csv">Download csv file {i+1}</a>')
    
    st.markdown(string, unsafe_allow_html=True)

def get_table_download_link(data):
    """Generates a link allowing the data in a given panda dataframe to be downloaded
    in:  dataframe
    out: href string
    """
    csv = data.to_csv(index=False)
    b64 = base64.b64encode(
        csv.encode()
    ).decode()  # some strings <-> bytes conversions necessary here

    return f'<a href="data:file/csv;base64,{b64}" download="myfilename.csv">Download csv file</a>'

def print_message(msg):
    html_temp = """
    <div style="background-color:blue;padding:2px">
    <h3 style="color:white;text-align:center;">{} </h3>
    </div>
    """
    st.markdown(html_temp.format(msg), unsafe_allow_html=True)

def local_css():
    with open(CSS_FILE) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)