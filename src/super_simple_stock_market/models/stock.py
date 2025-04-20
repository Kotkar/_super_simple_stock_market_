from datetime import datetime
from enum import Enum
from uuid import uuid4

from pydantic import BaseModel, Field, field_validator

from super_simple_stock_market.utils.constants import COMMON, PREFERRED


class StockType(str, Enum):
    common = COMMON
    preferred = PREFERRED


class Stock(BaseModel):
    id: str = Field(default=str(uuid4()))
    symbol: str = Field(..., max_length=10)
    type: StockType = StockType.common
    last_dividend: float
    fixed_dividend: float
    par_value: int


class StockPrice(BaseModel):
    """
    This model hold information about the stock and price requested.
    """

    stock: Stock
    price: float
    date_timestamp: datetime = datetime.now()

    @field_validator("price", mode="after")
    @classmethod
    def validate_price_type(cls, value: float) -> float:
        if value <= 0:
            raise ValueError("Price should be > 0")
        return value
