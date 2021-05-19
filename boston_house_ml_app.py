import pickle

import pandas as pd
import streamlit as st
import shap
import matplotlib.pyplot as plt
from sklearn import datasets
from sklearn.ensemble import RandomForestRegressor
from statistics import mean
st.write("""
# Boston House PRice Prediction App

This app predicts the *Boston House Price* !
""")
st.write('---')

boston = datasets.load_boston()
X = pd.DataFrame(boston.data, columns=boston.feature_names)

st.sidebar.header('User Input Params')
st.set_option('deprecation.showPyplotGlobalUse', False)
def user_input_features():
    CRIM = st.sidebar.slider('CRIM', min(X.CRIM), max(X.CRIM), mean(X.CRIM))
    ZN = st.sidebar.slider('ZN', min(X.ZN), max(X.ZN), mean(X.ZN))
    INDUS = st.sidebar.slider('INDUS', min(X.INDUS), max(X.INDUS), mean(X.INDUS))
    CHAS = st.sidebar.slider('CHAS', min(X.CHAS), max(X.CHAS), mean(X.CHAS))
    NOX = st.sidebar.slider('NOX', min(X.CRIM), max(X.NOX), mean(X.NOX))
    RM = st.sidebar.slider('RM', min(X.CRIM), max(X.RM), mean(X.RM))
    AGE = st.sidebar.slider('AGE', min(X.AGE), max(X.AGE), mean(X.AGE))
    DIS = st.sidebar.slider('DIS', min(X.CRIM), max(X.DIS), mean(X.DIS))
    RAD = st.sidebar.slider('RAD', min(X.RAD), max(X.RAD), mean(X.RAD))
    TAX = st.sidebar.slider('TAX', min(X.TAX), max(X.TAX), mean(X.TAX))
    PTRATIO = st.sidebar.slider('PTRATIO', min(X.PTRATIO), max(X.PTRATIO), mean(X.PTRATIO))
    B = st.sidebar.slider('B', min(X.B), max(X.B), mean(X.B))
    LSTAT = st.sidebar.slider('LSTAT', min(X.LSTAT), max(X.LSTAT), mean(X.LSTAT))

    data = {
        'CRIM': CRIM,
        'ZN': ZN,
        'INDUS': INDUS,
        'CHAS': CHAS,
        'NOX': NOX,
        'RM': RM,
        'AGE': AGE,
        'DIS': DIS,
        'RAD': RAD,
        'TAX': TAX,
        'PTRATIO': PTRATIO,
        'B': B,
        'LSTAT': LSTAT
    }

    features = pd.DataFrame(data, index=[0])
    return features

df = user_input_features()

st.subheader('User Input params')
st.write(df)
st.write('---')

model = pickle.load(open('boston_model.pkl', 'rb'))

prediction = model.predict(df)

st.header('Prediction of MEDV')
st.write(prediction)
st.write('---')

explainer = shap.TreeExplainer(model)
shap_values = explainer.shap_values(X)

st.header('Feature Importance')
plt.title('Feature importance based on SHAP values')
shap.summary_plot(shap_values, X)
st.pyplot(bbox_inches='tight')
st.write('---')

plt.title('Feature importance based on SHAP values (Bar)')
shap.summary_plot(shap_values, X, plot_type='bar')
st.pyplot(bbox_inches='tight')