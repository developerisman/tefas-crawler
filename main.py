from fastapi import FastAPI
from fastapi.responses import FileResponse
import csv
import os
import json

app = FastAPI()

# CSV dosya adı
CSV_FILE = "fonds.csv"
# JSON response dosyası (opsiyonel, isteğe bağlı)
JSON_FILE = "response.json"

# Örnek veri, kendi verinle değiştirebilirsin
fonds_data = [
    {"name": "Fon A", "value": 1000},
    {"name": "Fon B", "value": 2000},
    {"name": "Fon C", "value": 3000},
]

def create_csv():
    """CSV dosyasını oluşturur veya günceller."""
    with open(CSV_FILE, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["name", "value"])
        writer.writeheader()
        for row in fonds_data:
            writer.writerow(row)
    print(f"CSV başarıyla oluşturuldu: {CSV_FILE}")

# Deploy veya uygulama başlatılırken CSV oluştur
create_csv()

@app.get("/")
def root():
    return {"status": "ok", "csv_file": os.path.abspath(CSV_FILE)}

@app.get("/download-csv")
def download_csv():
    """CSV dosyasını indirilebilir şekilde döndürür."""
    if os.path.exists(CSV_FILE):
        return FileResponse(CSV_FILE, media_type="text/csv", filename="fonds.csv")
    return {"status": "error", "message": "CSV dosyası bulunamadı."}

@app.get("/response-json")
def get_response_json():
    """response.json içeriğini döndürür."""
    if os.path.exists(JSON_FILE):
        with open(JSON_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data
    return {"status": "empty", "message": "response.json bulunamadı."}
