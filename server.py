from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
import matplotlib.pyplot as plt
import io
import base64
import pandas as pd
import requests
from datetime import datetime
from fastapi_utils.tasks import repeat_every
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
origins = [
    "http://56.228.10.216:5173",  # your React frontend URL
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # allows only your React app
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)

DATA_FILE = "btc_prices.csv"

def fetch_bitcoin_price():
    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {"ids": "bitcoin", "vs_currencies": "usd"}
    response = requests.get(url, params=params)
    price = response.json()["bitcoin"]["usd"]
    timestamp = datetime.now().astimezone()
    return timestamp, float(price)

def save_price(timestamp, price):
    try:
        df = pd.read_csv(DATA_FILE)
    except FileNotFoundError:
        df = pd.DataFrame(columns=["timestamp", "price_usd"])

    df = pd.concat([df, pd.DataFrame([{"timestamp": timestamp, "price_usd": price}])])
    df.to_csv(DATA_FILE, index=False)

def create_btc_price_plot(filter_hours=None):
    try:
        df = pd.read_csv(DATA_FILE)
    except FileNotFoundError:
        df = pd.DataFrame(columns=["timestamp", "price_usd"])

    if df.empty:
        return ""

    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df = df.sort_values(by="timestamp")

    if filter_hours:
        time_threshold = pd.Timestamp.now(tz=df["timestamp"].dt.tz) - pd.Timedelta(hours=filter_hours)
        df = df[df["timestamp"] > time_threshold]

    df["moving_average"] = df["price_usd"].rolling(window=5).mean()

    plt.figure(figsize=(12, 6))
    plt.plot(df["timestamp"], df["price_usd"], label="Bitcoin Price", marker='o')
    plt.plot(df["timestamp"], df["moving_average"], label="5-Point Moving Average", linestyle='--')
    plt.title("Bitcoin Price Over Time")
    plt.xlabel("Timestamp")
    plt.ylabel("Price (USD)")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close()
    buf.seek(0)
    img_base64 = base64.b64encode(buf.read()).decode('utf-8')
    return img_base64

@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    hours = request.query_params.get("hours")

    filter_hours = None
    try:
        if hours is not None:
            filter_hours = int(hours)
    except ValueError:
        filter_hours = None

    img_base64 = create_btc_price_plot(filter_hours=filter_hours)
    if not img_base64:
        return "<h1>No data yet. Please wait for prices to be fetched.</h1>"

    html_content = f"""
    <html>
        <head><title>Bitcoin Live Price</title></head>
        <body>
            <h1>Bitcoin Live Price Graph</h1>
            <img src="data:image/png;base64,{img_base64}" alt="Bitcoin Price">
            <br><br>
            <a href="/">View All Time</a> |
            <a href="/?hours=1">Last 1 Hour</a> |
            <a href="/?hours=6">Last 6 Hours</a> |
            <a href="/?hours=12">Last 12 Hours</a> |
            <a href="/?hours=24">Last 24 Hours</a> |
            <a href="/?hours=168">Last 7 Days</a>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content)

@app.get("/fetch")
def fetch_price_now():
    ts, price = fetch_bitcoin_price()
    save_price(ts, price)
    return {"timestamp": str(ts), "price_usd": price}

@app.on_event("startup")
@repeat_every(seconds=300)  # every 5 minutes
def fetch_price_periodically():
    ts, price = fetch_bitcoin_price()
    save_price(ts, price)
    print(f"Auto-saved Bitcoin price: {price} at {ts}")
