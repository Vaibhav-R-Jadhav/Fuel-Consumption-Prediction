import numpy as np
import pandas as pd
import pickle as pk
import streamlit as st
import base64

loaded_model = pk.load(
    open("trained_model_rf.sav","rb"))
scaled_data = pk.load(
    open("scaled_data.sav","rb"))





def input_converter(inp):
    vcl = ['Two-seater', 'Minicompact', 'Compact', 'Subcompact', 'Mid-size', 'Full-size', 'SUV: Small', 'SUV: Standard',
           'Minivan', 'Station wagon: Small', 'Station wagon: Mid-size', 'Pickup truck: Small',
           'Special purpose vehicle', 'Pickup truck: Standard']
    trans = ['AV', 'AM', 'M', 'AS', 'A']
    fuel = ["D", "E", "X", "Z"]
    lst = []
    for i in range(6):
        if (type(inp[i]) == str):
            if (inp[i] in vcl):
                lst.append(vcl.index(inp[i]))
            elif (inp[i] in trans):
                lst.append(trans.index(inp[i]))
            elif (inp[i] in fuel):
                if (fuel.index(inp[i]) == 0):
                    lst.extend([1, 0, 0, 0])
                    break
                elif (fuel.index(inp[i]) == 1):
                    lst.extend([0, 1, 0, 0])
                    break
                elif (fuel.index(inp[i]) == 2):
                    lst.extend([0, 0, 1, 0])
                    break
                elif (fuel.index(inp[i]) == 3):
                    lst.extend([0, 0, 0, 1])
        else:
            lst.append(inp[i])

    arr = np.asarray(lst)
    arr = arr.reshape(1, -1)
    arr = scaled_data.transform(arr)
    prediction = loaded_model.predict(arr)

    return (f"The Fuel Consumption L/100km is {round(prediction[0], 2)}")





def main():
    
    st.markdown(
    """
    <style>
    body {
        background-image: url('https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSf_E3V1THqjF1EBlz_pdjLLtqVaoZsjZBWzA&usqp=CAU');
        background-repeat: no-repeat;
        background-size: cover;
    }
    </style>
    """,
    unsafe_allow_html=True)
    
    
    # giving a title    
    _left, mid, _right = st.columns(3)
    with mid:
       st.image("output-onlinegiftools.gif")
    st.markdown("<h1 style='text-align: center; color: red;'>Fuel Consumption Prediction</h1>", unsafe_allow_html=True)        
    # getting the input data from user    
    result = 0
    vehicle = ['Two-seater','Minicompact','Compact','Subcompact','Mid-size','Full-size','SUV: Small','SUV: Standard','Minivan','Station wagon: Small','Station wagon: Mid-size','Pickup truck: Small','Special purpose vehicle','Pickup truck: Standard']
    transmission = ['AV', 'AM', 'M', 'AS', 'A']
    fuel = ["D", "E", "X", "Z"]
    Vehicle_class = st.selectbox("Select the vehicle class",vehicle)
    Engine_size = st.number_input("Enter Engine Size (please enter value in this range[1-7])")
    Cylinders = st.number_input("Enter number of Cylinders (please enter value in this range[1-16]",min_value = 1, max_value = 16)
    Transmission = st.selectbox("Select the Transmission",transmission)
    Co2_Rating = st.number_input("Enter CO2 Rating (please enter value in this range[1-10]",min_value = 1, max_value = 10)
    Fuel_type = st.selectbox("Select the Fuel type",fuel)

    # code for prediction

    # creating a button for prediction
    if st.button("Predict 🔍"):
        result = input_converter([Vehicle_class,Engine_size,Cylinders,Transmission,Co2_Rating,Fuel_type])

    st.success(result)


if __name__ == "__main__":
    main()
