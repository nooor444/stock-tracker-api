from pydantic import BaseModel
from datetime import datetime
from typing import List


class StockPrice(BaseModel):
    ticker: str
    price: float


class HistoryItem(BaseModel):
    ticker: str
    price: float
    timestamp: datetime


class AnalysisResult(BaseModel):
    ticker: str
    count: int
    latest_price: float | None
    min_price: float | None
    max_price: float | None
    avg_price: float | None
    pct_change: float | None  # (% from oldest->latest in the window)
