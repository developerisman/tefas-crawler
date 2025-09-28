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
        # Tarihleri kontrol et
        start_date = datetime.strptime(start, "%Y-%m-%d")
        end_date = datetime.strptime(end, "%Y-%m-%d") if end else start_date

        # Veri çek
        data = tefas.fetch(start=start_date, end=end_date)

        # Eğer DataFrame veya CSV string geliyorsa JSON’a çevir
        if not isinstance(data, list):
            # Örn: pandas DataFrame veya CSV string
            try:
                import pandas as pd
                if isinstance(data, str):
                    from io import StringIO
                    df = pd.read_csv(StringIO(data))
                else:
                    df = data
                # Sadece ihtiyacımız olan kolonları al
                data = df[["Tarih","Fon Kodu","Fon Adı","Fiyat"]].to_dict(orient="records")
            except Exception:
                return {"error": "Could not parse data from crawler"}

        return data

    except ValueError:
        return {"error": "Date format should be YYYY-MM-DD"}
    except Exception as e:
        return {"error": str(e)}
