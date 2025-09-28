from fastapi import FastAPI, Query
from tefas import Crawler

app = FastAPI()
tefas = Crawler()

@app.get("/fonlar")
def fonlar(
    start: str = Query(..., description="Başlangıç tarihi YYYY-MM-DD"),
    end: str = Query(None, description="Bitiş tarihi YYYY-MM-DD")
):
    try:
        end = end or start
        # Crawler fetch, sadece ihtiyacımız olan 4 alan ve yatırım fonları
        data = tefas.fetch(
            start=start,
            end=end,
            columns=["date", "code", "title", "price"],
            kind="YAT"
        )

        # Her alanı stringe çevir, nested object veya Decimal sorununu önle
        result = []
        for row in data:
            result.append({
                "date": str(row.get("date", "")),
                "code": str(row.get("code", "")),
                "title": str(row.get("title", "")),
                "price": str(row.get("price", ""))
            })

        return result

    except Exception as e:
        return {"error": str(e)}
