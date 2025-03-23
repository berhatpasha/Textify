import os
import colorama
from colorama import Fore
colorama.init(autoreset=True)

print(f"{Fore.CYAN} Veri seti yükleniyor.")
import pandas as pd
splits = {'train': 'train.csv', 'test': 'test.csv'}
df = pd.read_csv("hf://datasets/winvoker/turkish-sentiment-analysis-dataset/" + splits["train"])
os.system("clear")
print(f"{Fore.CYAN} Veri seti yükleniyor..")


import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

os.system("clear")
print(f"{Fore.CYAN} Veriler vektörize ediliyor.")

df = df[['text','label']]
df['label'] = df['label'].map({'Positive': 1, 'Negative': 0, 'Notr': 2})
from sklearn.feature_extraction.text import TfidfVectorizer
os.system("clear")
print(f"{Fore.CYAN} Veriler vektörize ediliyor..")
vectorizer = TfidfVectorizer(max_features=5000)  
X = vectorizer.fit_transform(df['text']).toarray()  
y = df['label']  
os.system("clear")
print(f"{Fore.CYAN} Veriler vektörize ediliyor...")

#! Naive Bayes modeli
os.system("clear")
print(f"{Fore.CYAN} Model başlatıldı")
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score

nb_model = MultinomialNB()
nb_model.fit(X_train, y_train)

y_pred_nb = nb_model.predict(X_test)
print(f"Naive Bayes Doğruluk: {accuracy_score(y_test, y_pred_nb):.2f}")
