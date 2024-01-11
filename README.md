# FLO Müşteri Segmentasyonu Projesi

## Proje Adı: FLO Müşteri Segmentasyonu

Proje amacı, FLO'nun müşteri segmentasyonunu yapmak ve bu segmentasyona göre kampanya planlaması yapmaktır. Projede kullanılan veri seti, FLO'dan alınan 20.000 müşteri verisini içermektedir. Müşteri veri setinde, müşteri kimlik numarası, sipariş sayısı, alışveriş tutarı, son alışveriş tarihi gibi önemli değişkenler bulunmaktadır.

## Proje Aşamaları

### Veri Ön Hazırlık

1. Veri seti okunmuş ve kopyası alınmıştır.
2. Tarih ifade eden değişkenler datetime tipine dönüştürülmüştür.
3. Boş değerler incelenmiş ve gerekli işlemler yapılmıştır.

### RFM Metriklerinin Hesaplanması

1. Recency: Müşterinin en son alışveriş yaptığı tarihten bugüne kadar geçen gün sayısıdır.
2. Frequency: Müşterinin toplam alışveriş sayısıdır.
3. Monetary: Müşterinin toplam harcama tutarıdır.

### RFM Skorunun Hesaplanması

1. Recency, Frequency ve Monetary metrikleri qcut yardımı ile 1-5 arasında skorlara dönüştürülmüştür.
2. Bu skorlar recency_score, frequency_score ve monetary_score olarak kaydedilmiştir.
3. Recency_score ve frequency_score'u tek bir değişken olarak ifade edilmiş ve RF_SCORE olarak kaydedilmiştir.

### RF Skorunun Segment Olarak Tanımlanması

1. Oluşturulan RF skorları için segment tanımlamaları yapılmıştır.
2. Aşağıdaki `seg_map` yardımı ile skorlar segmentlere çevrilmiştir.


## Aksiyon Zamanı

Segmentlerin recency, frequnecy ve monetary ortalamaları incelenmiştir. İki özel case için uygun müşteriler belirlenip CSV dosyalarına kaydedilmiştir.

### Case 1: Yeni Kadın Ayakkabı Markası

- Sadık müşterilerden (champions, loyal_customers)
- Kadın kategorisinden alışveriş yapan müşteriler

**CSV Dosyası:** [kadin_ayakkabi.csv](./kadin_ayakkabi.csv)

### Case 2: Erkek ve Çocuk İndirim Kampanyası

- Kaybedilmemesi gereken müşteriler (cant_loose)
- Uykuda olan müşteriler (about_to_sleep)
- Yeni gelen müşteriler (new_customer)

**CSV Dosyası:** [erkek_cocuk_indirim.csv](./erkek_cocuk_indirim.csv)

## Kütüphaneler ve Ortam Kurulumu

Projeyi çalıştırmak için aşağıdaki kütüphanelerin yüklü olması gerekmektedir. Aşağıdaki komutları kullanarak kütüphaneleri yükleyebilirsiniz:

pip install pandas datetime seaborn numpy matplotlib


