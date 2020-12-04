'''
@Author : uday pratap yati
'''
import streamlit as st
PAGE_CONFIG = {
            "page_title":"EDA App using streamlit",
            "page_icon":"smiley:",
            # "layout":"wide",
            "initial_sidebar_state":"expanded"
            }
st.set_page_config(**PAGE_CONFIG)
# st.set_page_config(page_title="EDA App using streamlit", 
#                     page_icon=":smiley:",
#                     layout="wide",
#                     initial_sidebar_state="expanded")
import numpy as np
import pandas as pd 
import base64
import utility

from CarPricePrediction import car_prediction

df = pd.DataFrame()
projects = ["Car-Price-Prediction"]

def main():

    global df
    global projects
    utility.local_css()

    
    choice = st.sidebar.selectbox("Select an acitivity", projects)

    if choice == "Car-Price-Prediction":
        utility.print_message("Car-Price-Prediction")
        car_prediction()

        # performEDA(df)

    elif choice == "Feature Selection":
        utility.print_message("Feature Selection")
    

    for _ in range(15):
        st.sidebar.write("")

    html_about = """<div style="background-color:grey;padding:1px"><h3 style="color:black;text-align:left;"> About </h3></div>""" 
    st.sidebar.markdown(html_about, unsafe_allow_html=True)
    st.sidebar.info("Developed using awesome streamlit\n\nDeveloper : Uday Pratap Yati")

if __name__ == "__main__":
    main()