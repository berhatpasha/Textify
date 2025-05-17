
#*****************
#! POP-UP kısmıdır
from google import genai
client = genai.Client(api_key="AIzaSyDVN386y_WYLyzuV3iygXVdaUJJvRHZs4Y") ##! API anahtarı
def checkIt(position, keys, resolution):
  response = client.models.generate_content(
      model="gemini-2.0-flash",
      contents=f'''ÖNCELİKLE BENİ İYİ DİNLE VE SONUÇ OLARAK NE OLURSA OLSUN TEK CEVAP DÖNDÜR, HİÇBİR AÇIKLAMA VS. OLMASIN. NEYE GÖRE CEVAP DÖNDÜRECEĞİNİ
      BİRAZDAN AÇIKLAYACAĞIM AMA SAKIN AÇIKLAMA VS YAPMA DOĞRUDAN DİREKT TEK CEVAP OLARAK SÖYLEDİĞİM ŞEYİ DÖNDÜRECEN KARAR VERİP İŞTE TALİMATLAR BUYUR:
      SANA AZ SONRA VERECEĞİM BİLGİLERİ KULLANARAK (BU BİLGİLER KULANICININ EN SON TIKLADIĞI YER, EN SON YAZDIKLARI VS..) KULLANICININ BİR BELGE
      VEYA TÜREVİ BİR DOSYA,YAZI VS Mİ YAZDIĞI YOKSA BİR OYUNDA VEYA KOD YAZARKEN Mİ TUŞLARA TIKLADIĞINI ANLAMAN GEREKİYOR, EĞER GERÇEKTEN
      ASİSTANLIK EDEBİLECEĞİMİZ BİR BELGE VS. YAZDIĞINI TESPİT EDERSEN YANIT OLARAK YAZIM ASİSTANI POP-UPUNUN NEREDE AÇILMASI GEREKTİĞİNİ DÖNDÜR
      EĞER OYUN VS OLDUĞUNU VEYA ÖNERİ YAPMAMAMIZ GEREKTİĞİNİ DÜŞÜNDÜĞÜN BİR YERSE CEVAP OLARAK '#' DÖNDÜR. TEKRAR EDİYORUM EĞER BİR METİNE AİT OLDUĞUNU FALAN DÜŞÜNÜYORSAN
      POP-UP AÇILMASI GEREKTİĞİNİ DÜŞÜNDÜĞÜN YERİ '245,235' GİBİSİNDEN DÖNDÜR, EĞER AÇILMASINA GEREK OLMADIĞINI DÜŞÜNÜYORSAN '#' DÖNDÜR

      BİRDE POP-UP TAM ÜSTÜNDE FALAN AÇILMASIN BİRAZ MODERN DURSUN EKRANI ORTALASAIN VS VE DİREKT YAZDIĞIN YERİN ÜSTÜNDE OLMAMALI

      EN SON TIKLANAN YER: {position}
      TIKLADIKTAN SONRA EN SON YAZDIKLARI: {keys}
      EKRAN ÇÖZÜNÜRLÜĞÜ: {resolution}
      ''',
# Bir yere tıkladıktan sonra bellirli bir süre birşeyler yazdığı tespit edildiğinde checkIt(p,k) ile bu durum kontrol edilecek, gelen yanıt pozitif ise
# diğer fonksiyonlara yönlendirme yapılarak gelen yanıta bağlı pop-up etkinleştirilecek, '#' yanıt olarak döndürülrürse dinlemede kalmaya devam edecektir.
## ÖNEMLİ : güvenlik ilkesi gereğince kontroller ve bilgi parametreleri herhangi bir şekilde kaydedilmemeli ve ram üstünde tutulmaya devam edilmelidir.
  )
  return response.text
keys = ['a','b','i','backspace','b','i']
print(checkIt(position="X:2354, Y:23523", keys=keys, resolution="1920x1080"))


