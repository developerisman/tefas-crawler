from fastapi import FastAPI, Query
from tefas import Crawler
from datetime import datetime
import json

app = FastAPI()
tefas = Crawler()

@app.get("/fonlar")
def fonlar(start: str = Query(..., description="Başlangıç tarihi YYYY-MM-DD"),
           end: str = Query(None, description="Bitiş tarihi YYYY-MM-DD")):
    try:
        # Tarih parametrelerini doğrula
        try:
            start_date = datetime.strptime(start, "%Y-%m-%d").date()
            end_date = datetime.strptime(end, "%Y-%m-%d").date() if end else start_date
        except ValueError:
            return {"error": "Date format should be YYYY-MM-DD"}

        # Crawler.fetch() ile veriyi çek
        # columns parametresi bazı sürümlerde opsiyonel, CSV kolon isimleri ile uyumlu
        data = tefas.fetch(start=start_date.isoformat(), end=end_date.isoformat())

        # Eğer string gelirse JSON olarak parse et
        if isinstance(data, str):
            data = json.loads(data)

        # Dict olanları filtrele ve sadece CSV kolonlarını al
        filtered_data = []
        for item in data:
            if isinstance(item, dict):
                filtered_data.append({
                    "date": item.get("Tarih") or item.get("date"),
                    "code": item.get("Fon Kodu") or item.get("code"),
                    "title": item.get("Fon Adı") or item.get("title"),
                    "price": item.get("Fiyat") or item.get("price")
                })

        # Eğer hiçbir veri yoksa bilgi ver
        if not filtered_data:
            return {"message": "No data found for the given date(s)."}

        return filtered_data

    except Exception as e:
        return {"error": str(e)}
