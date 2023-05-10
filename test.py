import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression


titanic_data = pd.read_csv("data_transform/transformed.csv")

x = np.loadtxt('data_transform/transformed.csv', skiprows=2, delimiter=';', usecols=(2, 5, 6, 7, 8, 10, 11, 15))

y = np.loadtxt('data_transform/transformed.csv', skiprows=2, delimiter=';', usecols=1)

model = LogisticRegression(solver='liblinear', random_state=0)
