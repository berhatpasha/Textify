# Dökümantasyon

> #### [📄 Giriş](#giriş)
> #### [🔧 Kurulum ve derleme](#kurulum)
> #### [🧠 Back-end & Mimari](#back-end)
> #### [🛠️ Debug](#debug)
> #### [📬 İletişim](#back-end)

<br>
<br>

# Giriş

>**Devlet Bahçeli Fen Lisesi, TÜBİTAK 4006 projesidir.**
>
>Projede yer alanlar;
>- **Akif Eren Akkuş**: -veri bilimi ve analizi-
>- **Ayberk Yalçın**: -kullanıcı arayüzü ve önplan-
>- **Berat Bayraktar**: -makine öğrenimi ve arkaplan-
>- **Arda Ülger**: -gözetmen öğretmen-
>
>## PROJE AMACI: 
>Twitter gibi sosyal medya platformları, WhatsApp gibi mesajlaşma uygulamaları veya e-posta yazarken bağlama uygun >gelişmiş tamamlama ve optimizasyon önerileri sunarak iletişimi güçlendirmeyi amaçlar.
>## PROJE YÖNTEMİ
>Proje kapsamında, gelişmiş yapay zeka dil modelleri ve metin analizi için kendi geliştirdiğimiz makine öğrenimi >modelleriyle desteklenen araçlar sunan bir uygulama ağı veya eklenti yazılması hedeflenmektedir.
>## BEKLENEN SONUÇ
>Bu projenin başarıya ulaşmasıyla birlikte, özellikle büyük şirketler ve bireysel kullanıcılar daha az çabayla daha >verimli ve düzenli e-postalar, metinler ve mesajlar yazarak işlerini kolaylaştıracaklardır

## Kurulum
**Şimdilik masaüstü demosunu kurmak için şu an bir kurulum dosyası veya yürütülebilir sürümü bulunmamaktadır. Hazır olduğunda bu bölümde yayınlanacaktır**

'app/' içerisinde masaüstü demosunun versionları bulunmaktadır. Modelin diğer dosyalarıda içerisinde barındırmaktadır. Bağımsız demoyu kendi bilgisayarınızda çalıştırmak isterseniz, masaüstü demosunun son kaynak versionundan şu satırı bulun :
```
# API Key'i gir
client = genai.Client(api_key="*")
```
https://aistudio.google.com/apikey sayfasından aldığınız anahtarı buraya girerek projeyi kendi bilgisayarınızda çalıştırabilirsiniz.

Çalıştırmadan önce her version için koyduğumuz (op.) 'requirements' dosyası aracılığıyla kütüphaneleri indirebilirsiniz => `pip install -r requirements.txt` veya `pip3 install -r requirements.txt` (eğer debian veya arch tabanlı bir sistem kullanıyorsanız şunu denemeniz gerekebilir : `--break-system-packages`) Ayrıca, api entegrasyonu için : `pip install -q -U google-genai
`

<br>

# Back-end
Proje birkaç modulden oluşmaktadır, bunları özetlemek gerekirse başlıca:
1) Analiz modülü
2) Öneri modülü 

olarak ikiye ayırabiliriz. *'Analiz modülü'* kendi oluşturduğumuz iki temel makine öğrenmesi modeli ile cümledeki 'radikal' kelimeleri saptamak üzerine iken,
*'Öneri modülü'* Googgle genai modeli ile bulunan bu radikal (uyumsuz) kelimeler yerine yenilerinin sunulması, cümlenin optimize edilmesi ve cümle bağlamından hareketle daha mantıklı tamamlamalar sunulması üzerinedir.

**Açıklamaya Öneri modülünden başlayalım**
Öneri modülünde genai modeline giden istekler (promtlar) şuna benzer =>
```
SANA AZ SONRA VERECEĞİM CÜMLEYİ, OPTİMİZE ET,
NOKTALAMA İŞARETLİNİ VE YAZIM KURALLARINI DÜZELT,
CÜMLENİN DÜZELTİLMİŞ HALİNİ SADECE CEVAP OLARAK DÖNDÜR
düzletilecek cümle : {text}
```
örnek olarak gösterdiğim bu prompt, metin optimizasyon fonksiyonuna aittir (optimizeThis)
bu fonksiyon kısaca şuna benzer : 
```
def optimizeThis(text):
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=f'''
        SANA AZ SONRA VERECEĞİM CÜMLEYİ, OPTİMİZE ET,
        NOKTALAMA İŞARETLİNİ VE YAZIM KURALLARINI DÜZELT,
        CÜMLENİN DÜZELTİLMİŞ HALİNİ SADECE CEVAP OLARAK DÖNDÜR
        düzletilecek cümle : {text}
        ''',
    )
    return response.text
```
gelen karşılık daha sonra aynı fonksiyon içerisinde (bu farklı versionlarda değişebilir) 1.modül kullanılarak tekrardan ayıklanır.

İkinci modül içerisinde iki temel işlev daha vardır; bunlar tahmin (predictNext) ve alternatif (suggestNew) fonksiyonlarıdır. Biri cümlenin bağlamına uygun doldurma seçenekleri için sonraki kelimeyi tahmin eder. Diğeri ise, iki parametreden oluşur : ilk parametre bağlamı analiz edilecek cümleyi diğeri ise alternatif sunulmak istenen 'radikal' kelimeyi içerir (bu kelime önceden modül 1 ile saptanır) ve sonuç olarak alternatif kelimeyi döndürür. 

Diğer kritik modül olan modül **birincil modül** ile devam edelim;

Bu modül üzerinde daha fazla ayarlama ve teknik detaya girdiğimiz için nispeten daha karışıktır.
daha verimli olmak adına ikiye ayrılır. Bunlar 'resmiyet' ve 'duygu' durumudur. Resmiyet saptamak için basit bir veri seti üzerine Linear Regression altyapısı kurulmuştur. Over-fitting (aşşırı öğrenmenin) önüne geçmek için eğitim verileri işlenirken TF-IDF vektorizer kullanılmıştır. Bu sayede cümlenin resmiyet oranı saptanabilmektedir. Resmiyet oranı* 1-10 arasında değer alan bir puanlandırmadır; bu puan 0'a ne kadar yakın ise o kadar samimi, 10'a ne kadar yakın ise o kadar resmidir. Örneğin günlük hayattaki konuşmalarda ve whatsapp yazışmalarında 1-3 arası değerler alırken; kurumsal e-postalar, tutanaklar ve diğer belgeler 7-10 arası değerler alırlar. Bu değerlerdeki küçük değişimler dahi cümle içerisinde kısmi uyumsuzluklar yaratabilir. 

Benzer bir modelde az önce arz ettiğim gibi, duygusallık için yapılmıştır. Bu model sonuca nispeten daha az etki etmektedir ancak yinede iletişim kısmında ortaya çıkabilecek bazı olumsuzluklar ve manipilasyonların önüne geçmek açısından gerekli görmekteyiz. Bu modelde ise Naive Bayers ve Logistic Regression gibi farklı çözümleri test ettik.

Bu modelleri küçük veri setleriyle eğitmemize rağmen, hatrı sayılır bir başarı elde ettiğini söyleyebiliriz. Ancak yinede daha büyük veri setleri ile kusursuza daha yakın modeller üretilebilir. Veri kaynağı olarak faklı anlayışlar için birkaç farklı veri kaynağı kullandık ve topladık ancak bazılarının daha yararlı olduğunu söyleyebiliriz. Bu veri kaynakları başlıca : 

1) tweetler (x.com daki rastgele konular hakkındaki postlar )
2) mailler (çeşitli markaların gönderdiği bilgilendirme e-postaları ve diğer belgeler)
3) sentetik kaynaklı bağımsız cümleler (ChatGpt,Cloude gibi modellerin oluşturduğu cümleler)

Makine öğrenmesi modeli için skitlearn tercih edilmiştir.

Ayrıca projenin en başından, sonuna yapılan test ve denemeler, deneme süreci, çalışmaları görmek için 'model/' altındaki '**.ipynb**' uzantılı dosyaları kendi notebookunuza yükleyerek üzerine çalışabilirsiniz.

Proje sürecinde oldukça portlanabilir, temel bir anlayış ile çalıştık. Makine öğrenmesi anlayışlarını varsayılan düzeyde değiştirdik. Bunların amacı genelde projeyi daha anlaşılabilir ve altyapı düzeyinde kılmak. Veri seti büyütülerek ve teorik bazı çözümlerle model performansları arttırılabilir. Projenin genel *performansını arttıracağını düşündüğümüz temelde kritik noktalar* :

1) api'ye giden isteklerdeki promptlar (kritik bir önem taşırlar ve iyileştirilirse daha kısa sürede daha iyi yanıtlar alınabilir)
2) veri seti ve veri seti büyüklüğü (veri setinde optimizasyon ve dengeleme yapılabilir. Küçük bir veri seti ile çalıştığımızı düşünürsek, daha büyük bir veri seti çok daha yüksek performans sağlayabilir.)
3) modeller (kullanılan makine öğrenmesi model altyapıları daha öncede belirttiğim gibi varsayılan ölçekte düzenlenmiştir, daha kritik düzenlemeler ve teorik oynamalar ile daha yüksek performans elde edilebilir)

---

### detay =>
** *Bu kısım arkaplanın daha detaylı ve genel kod kısmıdır 'model/' altında bulunan test ortamlarının izahı olarakda düşünülebilir. Eğer üst kısmı okuduysanız buraya ihtiyacınız olmayabilir. Ancak proje üzerinde düzenleme & geliştirme yapacaksanız burayı lütfen okuyun*

*** *Bu kısımdaki bilgiler, projenin genel versiyonu için geçerlidir, farklı sürümlerde bu yaklaşımlar ve kod parçaları değiştirilebilir ancak altyapı temelde aynıdır.*

**O halde başlayalım :**

```
futures = vector.get_feature_names_out()

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
```

Bu modül (indirgeme modülü) yakalayıcı algoritmaya girecek kelimeleri ön elemeden geçirerek onların muadillerini bulmak için kullanılır. Bu kelimenin eğer varsa eğitimde oluşturulan 'futures' (öz nitelikler) den birine dönüştürür. Örneğin girecek olan kelime (parametre), 'vektörel' kelimesi olsun: `reWrite("vektörel işlemlerde teorik bakış açıları..", futures=futures, esik=0.85)`
burada vektörel kelimesi örneğinde, bu kelime eğitim veri setinde yoksa ve eğer var ise eğitim veri setindeki en yakın karşılığına çevirilir. ÖR: `vektörel => vektör` buradaki esik değeri aslında bu çevirmenin ne hassasiyette yapılacağı ve 'difflib' kütüphanesinin neyi kabul edeceğini ifade eder. Test için %85 (0.85) değerinde bırakılmıştır ancak ufak denemelerle en iyi sonuç bulunabilir.

```
while True:
    search_phrase = input(">> ").strip()
    search_words = search_phrase.split()

    temp = 0
    for word in search_words:
      temp += model.predict(vector.transform([reWrite(word, futures)]))
      print(temp)

    ort = temp / len(search_words) # cümledeki kelimelerin ortalama ağırlık değeri
    print(f"ortalama ağırlık değeri = {ort}")

    print("...")
    for word in search_words:
      if abs(model.predict(vector.transform([reWrite(word, futures)])) - ort) >= 1:
        print(f"yakalanan kelime >> '{word}'")
        print(f"alternatif >> '{suggestNew(search_words,word)}'")
```

Buradaki kod parçası ise aslında radikal kelimeleri yakalayan algoritmanın temel çalışma mantığını gösterir. Her metin parçalara (cümlelere) ayrılır ve her cümle bu fonksiyona girer. Cümle içerisindeki kelimelerin ortalama ağırlık değeri yada resmiyet oranı (1-10) bulunduktan sonra her kelimenin bu orana olan uzaklığına bakılır. Fark, belirli bir eşik değerinden *(burada `>=1`)* yüksek ise bu kelime işaretlenir. Bu eşik değeri algoritmanın hassasiyetidir denilebilir. Eğer çok yüksek olursa algoritma işaretleme yapmaz, çok düşük olursada her kelimeyi işaretler. Test için eşik değeri sabit '1' olarak bırakılmıştır ancak ufak testler ile daha iyi bir eşik değeri bulunabilir. (`tahmini değer = ~(0.964-1.325)`)

```
data = pd.read_excel('resmiyetV2.xlsx')

vector = TfidfVectorizer()
x = vector.fit_transform(data['Cümle'])
y = data["Resmiyet"]

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

model = LinearRegression()
model.fit(x_train,y_train)
```
bu kısımda verilerin vektörize olup temel makine öğrenimi modelinin tanımlandığı kısımdır. Burada test verilerini ve eğitim verilerini ayırarak denemeler yaptık. Model eğitimi tamamlandıktan sonra kaydedilip demo içerisinde doğrudan tahmin kullanılır.

Duygu modelide buna benzerdir, bu model için *birkaç farklı makine öğrenimi anlayışını denedik*:

Naive bayersi eğittik `=> nb_model.fit(X_train, y_train)`
Logistic Regression `=> lr_model.fit(X_train, y_train)`
Random Forest `=> rf_model.fit(X_train, y_train)`

*doğruluk oranları* sırasıyla : `~0.89(%89)`,`~0.91(%91)`,`~0.89(%89)` oldu. Regression eğitim hızında ve model doğruluk oranında iyi performans sergiledi. 

<br>

# Debug

Burası demoların release versionları ile güncellenecektir.
Eğer başka bir sorun olursa [📬 İletişim](#i̇letişim) bölümünden bizle iletişime geç.


<br>
<br>

# İletişim

>Okulumuzun internet sitesi  => https://774025.meb.k12.tr <br>
>Proje sayfası => ***şimdilik hizmet vermiyor!*** <br>
>Proje sayfası, iletişim bölümü => ***şimdilik hizmet vermiyor!*** <br>


