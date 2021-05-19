import pandas as pd
from sklearn import datasets
from sklearn.ensemble import RandomForestRegressor
import pickle

boston = datasets.load_boston()
bos = pd.DataFrame(boston.data, columns = boston.feature_names)
bos['PRICE'] = boston.target

X = bos.drop('PRICE', axis = 1)
Y = bos['PRICE']

model = RandomForestRegressor()
model.fit(X, Y)

pickle.dump(model, open('boston_model.pkl', 'wb'))