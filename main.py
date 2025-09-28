from fastapi import FastAPI, Query
from tefas import Crawler
from datetime import datetime

app = FastAPI()
tefas = Crawler()

@app.get("/fonlar")
def fonlar(start: str = Query(..., description="Başlangıç tarihi YYYY-MM-DD"),
           end: str = Query(None, description="Bitiş tarihi YYYY-MM-DD")):
    try:
        start_date = start
        end_date = end if end else start

        # Crawler.fetch() → veri tipi ne olursa olsun olduğu gibi döndür
        data = tefas.fetch(start=start_date, end=end_date)

        # Debug: veri tipi log
        print("Crawler returned type:", type(data))

        return data

    except Exception as e:
        return {"error": str(e)}
