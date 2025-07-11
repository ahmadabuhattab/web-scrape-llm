from fastapi import FastAPI, HTTPException
import json, pathlib

DATA = pathlib.Path("products_enriched.json")
app = FastAPI(title="Product API")

def read_data():
    if not DATA.exists():
        raise RuntimeError("Run scraper and summarizer first")
    return json.loads(DATA.read_text())

@app.get("/products")
def list_products():
    return read_data()

@app.get("/products/{idx}")
def product_detail(idx: int):
    data = read_data()
    if idx < 0 or idx >= len(data):
        raise HTTPException(404, "Product not found")
    return data[idx]
