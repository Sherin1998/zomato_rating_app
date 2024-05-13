import streamlit as st
import numpy as np
import pandas as pd
import string
import pickle
from places import l, m
import sklearn
import geoloc
import folium
from geopy.geocoders import Nominatim
import logging

st.set_page_config(layout="wide")

Random_model = pickle.load(open('Randomforest.pkl', 'rb'))

# Configure logging for the main module
logging.basicConfig(filename='app.log', level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)

def fare(inputs):
    prediction = Random_model.predict(inputs)
    return prediction

def main():
    st.title('Restaurant Rating Prediction')
    st.sidebar.header('Input Parameters')

    # Configure logging for the main function
    logging.basicConfig(filename='main_function.log', level=logging.INFO, format='%(asctime)s - %(message)s')
    logger = logging.getLogger(__name__)

    online_order = int(st.sidebar.selectbox('Online Order', [True, False]))
    book_table = int(st.sidebar.selectbox('Book Table', [True, False]))
    votes = st.sidebar.number_input('Votes', min_value=0, max_value=17000, step=1)
    cost = st.sidebar.number_input('Cost', min_value=0, max_value=7000, step=1)

    location = st.sidebar.selectbox('Location', l)
    places_df = pd.DataFrame(columns=l)
    places_df.loc[0, location] = 1
    places_df.fillna(0, inplace=True)
    places_df = places_df.values[0]

    geolocator = Nominatim(user_agent="streamlit_app")
    lat, long = geoloc.details(location)
    data_dict = {'latitude': lat, 'longitude': long}
    data_df = pd.DataFrame(data_dict, index=[0])
    st.write(f"Map for {location}:")
    st.map(data_df, zoom=10)

    rest_type = st.sidebar.selectbox('Rest_type', m)
    rest_df = pd.DataFrame(columns=m)
    rest_df.loc[0, rest_type] = 1
    rest_df.fillna(0, inplace=True)
    rest_df = rest_df.values[0]

    type = st.sidebar.selectbox('Type', ['Buffet', 'Cafes', 'Delivery', 'Desserts', 'Dine-out',
                                          'Drinks & nightlife', 'Pubs and bars'])
    type_df = pd.DataFrame(columns=['Buffet', 'Cafes', 'Delivery', 'Desserts', 'Dine-out', 'Drinks & nightlife',
                                     'Pubs and bars'])
    type_df.loc[0, type] = 1
    type_df.fillna(0, inplace=True)
    type_df = type_df.values[0]

    inputs = [online_order, book_table, votes, cost]
    inputs.extend(places_df)
    inputs.extend(rest_df)
    inputs.extend(type_df)
    inputs = np.array(inputs).reshape(1, -1)
    st.write(inputs)

    if st.button('Compute Rate'):
        pred = fare(inputs)
        st.write(f'The rate for {rest_type} category at {location} location is ', str(np.round(pred * 1, 2)))
        
        if(np.round(pred * 1, 2) > 3):
            st.write('The location  is reccomended')
        else:
            st.write('The location is not prefered')

if __name__ == '__main__':
    main()
