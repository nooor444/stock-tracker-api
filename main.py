from fastapi.responses import StreamingResponse
import matplotlib.pyplot as plt
from fastapi import FastAPI, Depends, Query, HTTPException
from sqlalchemy.orm import Session
import yfinance as yf

from database import SessionLocal, engine
from models import Base
import crud
from schemas import StockPrice, HistoryItem, AnalysisResult
import io
import matplotlib
matplotlib.use("Agg")  # Use non-GUI backend for servers


# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="📊 Live Stock Tracker API",
    description="""
A modern FastAPI project that fetches **live stock prices** using Yahoo Finance,
stores them in a local **SQLite database**, and provides **historical data & analytics**.

### Endpoints:
- `/stock/{ticker}` → Fetch the latest live stock price
- `/history/{ticker}` → Retrieve stored historical prices
- `/analysis/{ticker}` → Analyze recent price trends (min, max, avg, % change)
""",
    version="1.0.0",
    contact={
        "name": "Noor Kanwal",
    },
)


# Database dependency

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Root endpoint

@app.get("/", tags=["Health Check"])
def home():
    return {"message": " Stock Tracker API is running successfully!"}


# Fetch live stock price and store

@app.get("/stock/{ticker}", response_model=StockPrice, tags=["Stocks"])
def fetch_stock(ticker: str, db: Session = Depends(get_db)):
    data = yf.Ticker(ticker).history(period="1d")

    # Handle invalid ticker or missing data
    if data.empty:
        raise HTTPException(
            status_code=404,
            detail=f"No data found for ticker '{ticker.upper()}'"
        )

    latest = data.tail(1)
    price = float(latest["Close"].iloc[0])
    crud.add_stock(db, ticker, price)

    return {"ticker": ticker.upper(), "price": round(price, 2)}


# Retrieve stock price history

@app.get("/history/{ticker}", response_model=list[HistoryItem], tags=["Stocks"])
def stock_history(ticker: str, db: Session = Depends(get_db)):
    records = crud.get_stocks(db, ticker)
    if not records:
        raise HTTPException(
            status_code=404,
            detail=f"No records found for ticker '{ticker.upper()}'"
        )

    return [
        {"ticker": r.ticker, "price": r.price, "timestamp": r.timestamp}
        for r in records
    ]


# Analyze recent stock performance

@app.get("/analysis/{ticker}", response_model=AnalysisResult, tags=["Analytics"])
def analyze_ticker(
    ticker: str,
    n: int = Query(
        20, ge=2, le=1000,
        description="Number of most recent records to include in analysis"
    ),
    db: Session = Depends(get_db),
):
    rows = crud.get_stocks_latest_n(db, ticker, n)
    rows = list(reversed(rows))  # oldest → newest

    if not rows:
        raise HTTPException(
            status_code=404,
            detail=f"No records found for ticker '{ticker.upper()}'"
        )

    prices = [r.price for r in rows]
    latest = prices[-1]
    mn = min(prices)
    mx = max(prices)
    avg = sum(prices) / len(prices)
    pct_change = ((prices[-1] - prices[0]) / prices[0]
                  * 100) if prices[0] != 0 else None

    return {
        "ticker": ticker.upper(),
        "count": len(prices),
        "latest_price": round(latest, 2),
        "min_price": round(mn, 2),
        "max_price": round(mx, 2),
        "avg_price": round(avg, 2),
        "pct_change": round(pct_change, 2) if pct_change is not None else None,
    }


@app.get("/chart/{ticker}", tags=["Visualization"])
def chart_ticker(
    ticker: str,
    n: int = Query(
        20, ge=2, le=1000,
        description="Number of most recent records to visualize"
    ),
    db: Session = Depends(get_db),
):
    rows = crud.get_stocks_latest_n(db, ticker, n)
    rows = list(reversed(rows))  # oldest → newest

    if not rows:
        raise HTTPException(
            status_code=404,
            detail=f"No records found for ticker '{ticker.upper()}'"
        )

    # Extract timestamps and prices
    times = [r.timestamp for r in rows]
    prices = [r.price for r in rows]

    # Create chart
    plt.figure(figsize=(7, 4))
    plt.plot(times, prices, marker="o", linestyle="-",
             color="royalblue", linewidth=2)
    plt.title(f"{ticker.upper()} - Recent Price Trend", fontsize=14)
    plt.xlabel("Time", fontsize=12)
    plt.ylabel("Price ($)", fontsize=12)
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.tight_layout()

    # Save chart to a bytes buffer
    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    plt.close()
    buf.seek(0)

    # Return image as a streamed response
    return StreamingResponse(buf, media_type="image/png")
