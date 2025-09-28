from fastapi import FastAPI, Query
from tefas import Crawler
from datetime import datetime

app = FastAPI()
tefas = Crawler()

@app.get("/fonlar")
def fonlar(start: str = Query(None), end: str = Query(None)):
    try:
        # Tarih parametrelerini datetime'a çevir
        start_date = datetime.strptime(start, "%Y-%m-%d") if start else None
        end_date = datetime.strptime(end, "%Y-%m-%d") if end else None

        data = tefas.fetch(start=start_date, end=end_date)

        # Eğer string döndüyse JSON olarak parse et
        if isinstance(data, str):
            import json
            data = json.loads(data)

        # Sadece dict olanları al
        filtered_data = [
            {
                "symbol": item.get("symbol"),
                "name": item.get("name"),
                "price": item.get("price")
            }
            for item in data
            if isinstance(item, dict)
        ]

        return filtered_data

    except ValueError:
        return {"error": "Date format should be YYYY-MM-DD"}
    exce
