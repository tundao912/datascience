import pandas as pd
import streamlit as st
import pickle
import numpy as np
from sklearn.ensemble import RandomForestClassifier

st.write("""
# Penguins Prediction App

This app predicts the **Palmer Penguins** species!
""")

st.sidebar.header('User Input Params')

st.sidebar.markdown("""
[Example CSV input file](https://raw.githubusercontent.com/dataprofessor/streamlit_freecodecamp/main/app_8_classification_penguins/penguins_cleaned.csv)
""")

uploader = st.sidebar.file_uploader('Upload your input file', type=['csv'])

if uploader is not None:
    input_df = pd.read_csv(uploader)
else:
    def user_input_features():
        island = st.sidebar.selectbox('Island', ('Biscoe', 'Dream', 'Torgersen'))
        sex = st.sidebar.selectbox('Sex', ('male','female'))
        bill_length_mm = st.sidebar.slider('Bill length (mm)', 32.1, 59.6, 43.9)
        bill_depth_mm = st.sidebar.slider('Bill depth (mm)', 13.1, 21.5, 17.2)
        flipper_length_mm = st.sidebar.slider('Flipper length (mm)', 172.0, 231.0, 201.0)
        body_mass_g = st.sidebar.slider('Body mass (g)', 2700.0, 6300.0, 4207.0)

        data = {
            'island': island,
            'sex': sex,
            'bill_length_mm': bill_length_mm,
            'bill_depth_mm': bill_depth_mm,
            'flipper_length_mm': flipper_length_mm,
            'body_mass_g': body_mass_g
        }

        features = pd.DataFrame(data, index=[0])
        return features

    input_df = user_input_features()

penguins_raw = pd.read_csv('penguins_cleaned.csv')
penguins = penguins_raw.drop(columns=['species'])
df = pd.concat([input_df, penguins], axis=0)

encode = ['sex', 'island']
for col in encode:
    dummy = pd.get_dummies(df[col], prefix=col)
    df = pd.concat([df, dummy], axis=1)
    del df[col]
df = df[:1]

st.subheader('User Input params')
if uploader is not None:
    st.write(df)
else:
    st.write('Awaiting CSV file to be uploaded. Currently using example input params')
    st.write(df)

load_clf = pickle.load(open('penguins_clf.pkl', 'rb'))

prediction = load_clf.predict(df)
prediction_proba = load_clf.predict_proba(df)

st.subheader('Prediction')
penguins_species = np.array(['Adelie', 'Chinstrap', 'Gentoo'])
st.write(penguins_species[prediction])

st.subheader('Prediction Probability')
st.write(prediction_proba)