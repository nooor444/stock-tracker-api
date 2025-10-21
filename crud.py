from sqlalchemy.orm import Session
from models import Stock
from typing import List


def add_stock(db: Session, ticker: str, price: float):
    new_stock = Stock(ticker=ticker.upper(), price=price)
    db.add(new_stock)
    db.commit()
    db.refresh(new_stock)
    return new_stock


def get_stocks(db: Session, ticker: str):
    return db.query(Stock).filter(Stock.ticker == ticker.upper()).all()


def get_stocks_latest_n(db: Session, ticker: str, n: int) -> List[Stock]:
    return (
        db.query(Stock)
        .filter(Stock.ticker == ticker.upper())
        .order_by(Stock.timestamp.desc())
        .limit(n)
        .all()
    )
