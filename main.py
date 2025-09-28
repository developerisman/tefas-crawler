from fastapi import FastAPI, Query
from tefas import Crawler

app = FastAPI()
tefas = Crawler()

@app.get("/fonlar")
def fonlar(
    start: str = Query(..., description="Başlangıç tarihi YYYY-MM-DD"),
    end: str = Query(None, description="Bitiş tarihi YYYY-MM-DD")
):
    """
    TEFAS fonlarını alır.
    - start: Başlangıç tarihi (YYYY-MM-DD)
    - end: Bitiş tarihi (YYYY-MM-DD), opsiyonel
    Dönen JSON sadece:
      - date: Tarih
      - code: Fon Kodu
      - title: Fon Adı
      - price: Fiyat
    Gereksiz fon türleri (commercial_paper vb.) dahil edilmez.
    """
    try:
        # Eğer end parametresi yoksa start ile aynı gün alınır
        end = end or start

        # Sadece ihtiyacımız olan kolonlar ve yatırım fonları
        data = tefas.fetch(
            start=start,
            end=end,
            columns=["date", "code", "title", "price"],
            kind="YAT"  # yatırım fonlarını al, commercial_paper vb. gelmez
        )

        return data

    except Exception as e:
        return {"error": str(e)}
