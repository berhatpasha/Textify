from PyQt5.QtWidgets import (
    QApplication, QWidget, QTextEdit, QVBoxLayout, QSystemTrayIcon, QStyle,
    QMenu, QAction, QLabel, QPushButton
)
from PyQt5.QtGui import QFont, QColor, QIcon, QPainter
from PyQt5.QtCore import Qt, QTimer, QPropertyAnimation
from google import genai

#! API erişimidir
#! Yürütülebilir versiyonlarda hazır girilidir
#! Eğer kendiniz derliyorsanız, googleGenai API anahtarınızı buraya girin
client = genai.Client(api_key="AIzaSyDVN386y_WYLyzuV3iygXVdaUJJvRHZs4Y")

# optimizator fonksiyonu
def optimizeThis(text):
    print("Optimizer çalışıyor")
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=f'''
        SANA AZ SONRA VERECEĞİM CÜMLEYİ, OPTİMİZE ET,
        NOKTALAMA İŞARETLİNİ VE YAZIM KURALLARINI DÜZELT,
        CÜMLENİN DÜZELTİLMİŞ HALİNİ SADECE CEVAP OLARAK DÖNDÜR
        düzletilecek cümle : {text}
        ''',
    )
    
    #return radar(response.text) ##! BURAYLA DAHA SONRA İLGİLEN -- MODEL GEÇİTİ
    return response.text

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
