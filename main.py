import json
import pandas as pd

# JSON'u dosyadan veya API yanıtından alın
with open('response.json', 'r', encoding='utf-8') as f:
    data = json.load(f)  # str yerine dict

# date ve title alanlarını DataFrame'e çevir
try:
    df = pd.DataFrame({
        'date': data.get('date', {}),
        'title': data.get('title', {})
    })
except Exception as e:
    print("Hata oluştu:", e)
    exit(1)

# DataFrame'in indexleri bazen string olabiliyor, reset et
df = df.reset_index(drop=True)

# CSV olarak kaydet
df.to_csv('fonds.csv', index=False, encoding='utf-8-sig')
print("CSV başarıyla oluşturuldu: fonds.csv")
