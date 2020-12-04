import numpy as np
import pandas as pd 
import joblib
import streamlit as st
import datetime
# Fuel_Type has 3 values : {'Diesel', 'CNG', 'Petrol'}
# Seller_Type has 2 values : {'Dealer', 'Individual'}
# Transmission has 2 values : {'Automatic', 'Manual'}
# df['car_age'] = df['current_year'] -  df['Year']

def car_prediction():

    model = joblib.load('saved_models/rf_modle.pkl')

    present_price = st.text_input("Present price in lakhs")
    km_driven = st.text_input('KM driven')
    year = st.text_input("Year")
    car_age = 0
    owner = st.selectbox("Owner", [i for i in range(0, 6)])
    
    petrol_type = st.selectbox("Fuel type", ["Petrol","Diesel","CNG"])
    fueltype_petrol = 0
    fueltype_diesle = 0
    if petrol_type == "Petrol":
        fueltype_petrol = 1
        fueltype_diesle = 0
    elif petrol_type == "Diesel":
        fueltype_petrol = 0
        fueltype_diesle = 1

    seller_type = st.selectbox("Seller type", ["Dealer","Individual"])
    if seller_type == "Dealer":
        seller_type = 1
    else:
        seller_type = 0

    transmission_type = st.selectbox("Transmission type", ["Automatic","Manual"])
    if transmission_type == "Manual":
        transmission_type = 1
    else:
        transmission_type = 0

    if st.button("Predict Selling Price"):
        if present_price is None:
            st.error("Enter Present Price")
        elif km_driven is None:
            st.error("Enter KM Driven")
        elif year is None:
            st.error("Enter Year")
        else:
            car_age = datetime.datetime.now().year - int(year)
            prediction=model.predict([[present_price, km_driven, owner,car_age, fueltype_diesle, fueltype_petrol, seller_type, transmission_type]])
            output=round(prediction[0],2)
            if output < 0:
                st.error("Sorry you cannot sell this car")
            else:
                st.success("You Can Sell The Car at {}".format(output))