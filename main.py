from fastapi import FastAPI
from tefas import Crawler
import json

app = FastAPI()
tefas = Crawler()

@app.get("/fonlar")
def fonlar(start: str = None, end: str = None):
    try:
        data = tefas.fetch(start=start, end=end)
        return data
    except Exception as e:
        return {"error": str(e)}

