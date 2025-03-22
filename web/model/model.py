import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

#* eğitim
#! data = pd.read_excel('resmiyet.xlsx')
#! data = pd.read_excel('resmiyet.xlsx')
data = pd.read_excel('dataset/release/resmiyetV2.xlsx')
vector = TfidfVectorizer()

x = vector.fit_transform(data['Cümle'])
y = data["Resmiyet"]

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

model = LinearRegression()
model.fit(x_train,y_train)

simulator = model.predict(x_test)

print(mean_squared_error(y_test,simulator))
model.score(x_test,y_test)

def prediction(x):
     print(model.predict(vector.transform(x)))

#* örnek
prediction(["Merhaba arkadaşlar nasılsınız"])