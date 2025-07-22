# Eşleştirme Servisi (Flask + Sentence Transformers)

Bu proje, kayıp ve bulunan eşyalar arasında **akıllı eşleşme** yapılmasını sağlayan bir Python tabanlı eşleştirme servisidir. Flask framework’ü ve `sentence-transformers` kütüphanesi kullanılarak geliştirilmiştir.

## Özellikler

- TF-IDF ve BERT destekli metin benzerliği hesaplama
- Konum (şehir, ilçe, mahalle) ve kategori bazlı skor algoritması
- RESTful API ile kolay entegrasyon (örneğin .NET uygulamalarıyla)

## Kullanılan Teknolojiler

- Python 3.10
- Flask
- sentence-transformers (MiniLM-L12-v2)
- scikit-learn
- NumPy, SciPy
- Postman / HTTP test araçları

## API Kullanımı

### `POST /match`

Yeni bir eşya verisi ile mevcut adaylar arasında en uygun eşleşmeleri döner.

#### Gönderilen JSON

```json
{
  "input": {
    "sehir": "Ankara",
    "ilce": "Çankaya",
    "mahalle": "Bahçelievler",
    "esya": "telefon",
    "marka": "Samsung",
    "model": "S21",
    "renk": "siyah"
  },
  "aday": [
    {
      "sehir": "Ankara",
      "ilce": "Çankaya",
      "mahalle": "Bahçelievler",
      "esya": "telefon",
      "marka": "Samsung",
      "model": "S20",
      "renk": "siyah"
    }
  ]
}
