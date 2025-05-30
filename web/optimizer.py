from google import genai
from key import APIKEY #* api anahtarı buradan çekilir
from model.modelR import radar


#! API erişimidir
#! Yürütülebilir versiyonlarda hazır girilidir
#! Eğer kendiniz derliyorsanız, googleGenai API anahtarınızı buraya girin
client = genai.Client(api_key=APIKEY)

#* düzenleyici mdodülü
def hex(text):
    # return text #! debug: sorun boşluk bırakması deilmiş gereksiz satır atlamasıymış, yani textte sorun yok
    # front-end yönünden incelenmesi gerekiyor **** önemli --- güncelleme : sorun çözüldü

    flex = text.split(' ')
    fullText = ''
    for word in flex:
        fullText += word + ' '
        print(f"düzenlenmiş: {fullText}")
    return fullText


# optimizator fonksiyonu
def optimizeThis(text):
    print("Optimizer çalışıyor")
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=f'''
        SANA AZ SONRA VERECEĞİM CÜMLEYİ, OPTİMİZE ET,
        NOKTALAMA İŞARETLİNİ VE YAZIM KURALLARINI DÜZELT,
        CÜMLEYİ ANLAM BAKIMINDAN VE YAPI BAKIMINDAN İNCELE, 
        VE GÖRDÜĞÜN KELİMELERİ EĞER GEREKİYORSA DEĞİŞTİR,
        EN AZ KELİMEYİ DEĞİŞTİREREK ANLAMDA EN YÜKSEK OPTİMİZASYONU SAĞLA, 
        SONUÇ OLABİLDİĞİNCE DİL VE ANLATIM BAKIMINDAN UYGUN OLMALI VE DUYGU,RESMİYET DURUMUNU İYİCE YANSITMALI,
        ANLAŞILIR BİR CÜMLE YAPISI KURMAK TEMEL AMACIN
        CÜMLENİN DÜZELTİLMİŞ HALİNİ SADECE CEVAP OLARAK DÖNDÜR
        ASLA KELİMELERİ ES GEÇME 
        düzletilecek cümle : {text}
        ''',
    )

    print(hex(radar(response.text))) # debug
    return hex(radar(response.text))
    # return radar(response.text) ##! BURAYLA DAHA SONRA İLGİLEN -- MODEL GEÇİTİ
    #return response.text

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
    print(f"çıktı : '{response.text}'")

    if response.text != '''#
''': # alternatif yoksa backup <==
        return response.text
    else:
        return word    