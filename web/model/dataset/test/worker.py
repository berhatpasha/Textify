import re
import pandas as pd

# CSV dosyasını okuma
df = pd.read_csv('cumleler.csv')

# Metin temizleme fonksiyonu
def temizle(metin):
    # Noktalama işaretlerini ve sayıları kaldırma, metni küçük harfe çevirme
    metin = re.sub(r'[^\w\s]', '', metin)  # Noktalama işaretlerini kaldır
    metin = re.sub(r'\d+', '', metin)      # Sayıları kaldır
    return metin.lower()                   # Küçük harfe çevir

# 'Cümleler' sütunundaki her bir cümleyi temizle
df['Cümleler'] = df['Cümleler'].apply(temizle)

# Temizlenmiş veriyi yeni bir CSV dosyasına kaydetme
df.to_csv('cumleler_temizlenmis.csv', index=False, encoding='utf-8')

print("Veri başarıyla temizlendi ve kaydedildi!")
