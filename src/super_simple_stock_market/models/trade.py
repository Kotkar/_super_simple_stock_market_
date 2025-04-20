from datetime import datetime

from pydantic import BaseModel, Field, field_validator


class Trade(BaseModel):
    symbol: str
    date_timestamp: datetime = datetime.now()
    quantity: int
    trade_type: str = Field(default="BUY")  # buy/sell
    traded_price: float

    @field_validator("trade_type", mode="after")
    @classmethod
    def validate_trade_type(cls, value: str) -> str:
        if value not in ["BUY", "SELL"]:
            raise ValueError(f"Trade Inidicator is either BUY or SELL. Not {value}")
        return value
