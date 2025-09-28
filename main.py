from fastapi import FastAPI
from fastapi.responses import JSONResponse
import csv
import json
from pathlib import Path

# --------------------------
# FastAPI uygulamasını oluştur
# --------------------------
app = FastAPI()  # <- Buradaki 'app' önemli, uvicorn main:app bunu arıyor

# --------------------------
# Dosya yolları
# --------------------------
BASE_DIR = Path(__file__).parent
RESPONSE_FILE = BASE_DIR / "response.json"
CSV_FILE = BASE_DIR / "fonds.csv"

# --------------------------
# response.json yoksa oluştur
# --------------------------
if not RESPONSE_FILE.exists():
    with open(RESPONSE_FILE, "w", encoding="utf-8") as f:
        json.dump([], f)

# --------------------------
# CSV oluşturma fonksiyonu
# --------------------------
def create_csv_from_json():
    with open(RESPONSE_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    if not data:
        # Boş CSV oluştur, başlıkları örnek
        with open(CSV_FILE, "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["id", "name", "value"])
        print("response.json boş, CSV oluşturuldu ama veri yok.")
    else:
        with open(CSV_FILE, "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=data[0].keys())
            writer.writeheader()
            writer.writerows(data)
        print(f"CSV başarıyla oluşturuldu: {CSV_FILE}")

# Başlangıçta CSV oluştur
create_csv_from_json()

# --------------------------
# FastAPI endpoint'leri
# --------------------------
@app.get("/")
def read_root():
    return JSONResponse(content={"status": "ok", "csv_file": str(CSV_FILE)})

@app.get("/refresh-csv")
def refresh_csv():
    create_csv_from_json()
    return JSONResponse(content={"status": "csv refreshed", "csv_file": str(CSV_FILE)})
