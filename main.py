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
        # Tarihleri datetime veya string olarak ayarla
        start_date = start
        end_date = end if end else start

        # Sadece istediğimiz kolonları al: date, code, title, price
        data = tefas.fetch(start=start_date, end=end_date, columns=["date","code","title","price"])

        # Eğer string gelirse parse et
        if isinstance(data, str):
            data = json.loads(data)

        # Dict olanları filtrele ve sadece gerekli alanları döndür
        filtered_data = [
            {
                "date": item.get("date"),
                "code": item.get("code"),
                "title": item.get("title"),
                "price": item.get("price")
            }
            for item in data
            if isinstance(item, dict)
        ]

        return filtered_data

    except Exception as e:
        return {"error": str(e)}
