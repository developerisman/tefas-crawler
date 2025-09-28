from fastapi import FastAPI, Query
from tefas import Crawler
import json
from datetime import datetime

app = FastAPI()
tefas = Crawler()

@app.get("/fonlar")
def fonlar(start: str = Query(None, description="Başlangıç tarihi YYYY-MM-DD"),
           end: str = Query(None, description="Bitiş tarihi YYYY-MM-DD")):
    try:
        # Tarih parametrelerini kontrol et
        start_date = datetime.strptime(start, "%Y-%m-%d") if start else None
        end_date = datetime.strptime(end, "%Y-%m-%d") if end else None

        data = tefas.fetch(start=start_date, end=end_date)
        return data
    except ValueError:
        return {"error": "Date format should be YYYY-MM-DD"}
    except Exception as e:
        return {"error": str(e)}
