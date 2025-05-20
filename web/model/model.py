##! *
##! Bu kısım inceleme modellerinden birinin örneğidir, bu api ile entegre çalışacak olan 
##! modellerin her birinin neye benzeyeceğini anlamanız için yardımcı olacaktır.

import sklearn

#* eğitim kısmı 
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

#data = pd.read_excel('resmiyet.xlsx')
# data = pd.read_excel('resmiyetV2.xlsx')
print("verileri okunuyor")
data = pd.read_excel('web/model/resmiyetV2.xlsx')
print("veriler okundu")

print("örnek model eğitiliyor")
vector = TfidfVectorizer()
x = vector.fit_transform(data['Cümle'])
y = data["Resmiyet"]
print("resmiyet modeli hazır durumda")

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

model = LinearRegression()
model.fit(x_train,y_train)

model.predict(vector.transform(["selam dostum"])) # örnek giriş

def prediction(x):
    return model.predict(x)

#* uygulama kısmı

from google import genai
from key import APIKEY #* api anahtarı buradan çekilir

#! API erişimidir
#! Yürütülebilir versiyonlarda hazır girilidir
#! Eğer kendiniz derliyorsanız, googleGenai API anahtarınızı buraya girin
client = genai.Client(api_key=APIKEY)

futures = vector.get_feature_names_out()

from difflib import get_close_matches

def reWrite(cumle, futures, esik=0.85): ## indirgeme modülü
    kelimeler = cumle.split()
    duzeltilmis_kelimeler = []

    for kelime in kelimeler:
        yakin_kelimeler = get_close_matches(kelime, futures, n=1, cutoff=esik)
        if yakin_kelimeler:
            duzeltilmis_kelimeler.append(yakin_kelimeler[0])
        else:
            duzeltilmis_kelimeler.append(kelime)

    return " ".join(duzeltilmis_kelimeler)



def suggestNew(text,word):
    print('öneri modülü çalışıyor')
    response = client.models.generate_content(
      model="gemini-2.0-flash",
      contents=f'''SANA AZ SONRA VERECEĞİM CÜMLEYİ, ANALİZ ET,
      VE VERDİĞİM KELİME YERİNE CÜMLE İÇİN DAHA İYİ ALTERNATİF SUN,
      YENİ KELİME ÖNERİSİNİ DOĞRUDAN CEVAP OLARAK DÖNDÜR, YANİ YENİ KELİME DIŞINDA BİR CEVAP DÖNDÜRME, TEK CEVAP OLSUN
      EĞER KELİMEYİ CÜMLEDEN SİLMEK DAHA UYGUN İSE '#' CEVAP OLARAK GÖNDER

      ipucu : mutlaka gelen kelimeden farklı bir kelimeyi alternatif olarak döndür yani asla gelen kelimeyi aynı döndürme !

      cümlenin tamamı : {text}
      alternatif sunman gereken kelime : {word}

      ''',
    )
    print(f"cümle : {text}")
    print(f"kelime : {word}")
    print(f"çıktı : {response.text}")

    return response.text

def radar(text):
    search_phrase = text
    search_words = search_phrase.split()
    num_words = len(search_words)
    if num_words == 0:
        return text

    temp = 0
    predictions = []
    for word in search_words:
        prediction_value = prediction(vector.transform([reWrite(word, futures)]))[0]
        predictions.append(prediction_value)
        temp += prediction_value
        print(temp)

    ort = temp / num_words if num_words > 0 else 0

    for i, word in enumerate(search_words):
        if abs(predictions[i] - ort) >= 1:
            alternatif = suggestNew(search_words, word)
            if alternatif:
                new_sentence_list = list(search_words)
                new_sentence_list[i] = alternatif
                return " ".join(new_sentence_list)
            else:
                return text

    return text