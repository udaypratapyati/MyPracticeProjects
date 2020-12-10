'''
@Author : uday pratap yati
'''
import streamlit as st
from PIL import Image
logo = Image.open('img/logo.jpg')

PAGE_CONFIG = {
            "page_title":"EDA App using streamlit",
            "page_icon": logo, #"smiley:",
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
from MovieRecomendation import movie_recommendation

df = pd.DataFrame()
regression_projects = ["Car-Price-Prediction"]
classification_projects = [""]
recommendation_projects = ["Movie Recommendation System"]
type_of_project = ["Regression", "Classification", "Recommendation System"]


def main():

    global df
    global regression_projects
    global type_of_project

    utility.local_css()     # load custom ui settings

    project_type = st.sidebar.radio("Select type of project", type_of_project)
    if project_type == "Regression":
        choice = st.sidebar.selectbox("Regression Projects", regression_projects)

        if choice == "Car-Price-Prediction":
            utility.print_message("Car-Price-Prediction")
            car_prediction()

    elif project_type == "Classification":
        choice = st.sidebar.selectbox("Classification Projects", classification_projects)
        if choice == "Car-Price-Prediction":
            utility.print_message("Feature Selection")
    
    elif project_type == "Recommendation System":
        choice = st.sidebar.selectbox("Recommendation System", recommendation_projects)
        if choice == "Movie Recommendation System":
            utility.print_message("Movie Recommendation System")
            movie_recommendation()

    for _ in range(15):
        st.sidebar.write("")

    html_about = """<div style="background-color:grey;padding:2px"><h3 style="color:black;text-align:left;"> About </h3></div>""" 
    st.sidebar.markdown(html_about, unsafe_allow_html=True)
    # st.sidebar.info("Developed using awesome streamlit\n\nDeveloper : Uday Pratap Yati")
    st.sidebar.info("Developed using awesome streamlit \n\n {}".format(__doc__))
    # st.sidebar.info("Developer : Uday Pratap Yati")

if __name__ == "__main__":
    main()