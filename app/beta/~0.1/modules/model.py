import pickle
from google import genai

try:
    pkl = 'app/alpha/~0.1/modules/model.pkl'
    with open(pkl, 'rb') as file:
        down = pickle.load(file)
    model = down['model']
    vectorizer = down['vektorleyici']
except FileNotFoundError:
    pkl = 'model.pkl'
    with open(pkl, 'rb') as file:
        down = pickle.load(file)
    model = down['model']
    vectorizer = down['vektorleyici']

client = genai.Client(api_key="AIzaSyDVN386y_WYLyzuV3iygXVdaUJJvRHZs4Y")
def suggestNew(text,word):
    response = client.models.generate_content(
      model="gemini-2.0-flash",
      contents=f'''SANA AZ SONRA VERECEĞİM CÜMLEYİ, ANALİZ ET,
      VE VERDİĞİM KELİME YERİNE CÜMLE İÇİN DAHA İYİ ALTERNATİF SUN,
      YENİ KELİME ÖNERİSİNİ DOĞRUDAN CEVAP OLARAK DÖNDÜR, YANİ YENİ KELİME DIŞINDA BİR CEVAP DÖNDÜRME, TEK CEVAP OLSUN
      EĞER KELİMEYİ CÜMLEDEN SİLMEK DAHA UYGUN İSE '#' CEVAP OLARAK GÖNDER
      cümlenin tamamı : {text}
      alternatif sunman gereken kelime : {word}
      ''',
  )

## indirgeme modülü
futures = vectorizer.get_feature_names_out()

from difflib import get_close_matches

def reWrite(cumle, futures, esik=0.85):
    kelimeler = cumle.split()
    duzeltilmis_kelimeler = []

    for kelime in kelimeler:
        yakin_kelimeler = get_close_matches(kelime, futures, n=1, cutoff=esik)
        if yakin_kelimeler:
            duzeltilmis_kelimeler.append(yakin_kelimeler[0])
        else:
            duzeltilmis_kelimeler.append(kelime)

    return " ".join(duzeltilmis_kelimeler)



##? temel model
def prediction(text): ##* model kullanımı
    temp = vectorizer.transform([text])
    return model.predict(temp)[0]


'''
def radar(text):
    while True:
        search_phrase = text
        search_words = search_phrase.split()
        
        temp = 0 
        for word in search_words:
            temp += prediction(reWrite(word, futures))
            print(temp)
        
        ort = temp / len(search_words) #* ortalama ağırlık değeri
        
        for word in search_words:
            if abs(prediction(vectorizer.transform([reWrite(word, futures)])) - ort) >= 1:
                #!print(f"yakalanan kelime >> '{word}'") 
                #!print(f"alternatif >> '{suggestNew(search_words,word)}'")
                return suggestNew(search_words,word)
'''

def radar(text):
    search_phrase = text
    search_words = search_phrase.split()
    num_words = len(search_words)
    if num_words == 0:
        return text

    temp = 0
    predictions = []
    for word in search_words:
        prediction_value = prediction(vectorizer.transform([reWrite(word, futures)]))[0]
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
