import logging
from functools import reduce

from super_simple_stock_market.models.stock import Stock, StockPrice
from super_simple_stock_market.services.trade_service import TradeRecords, TradeService
from super_simple_stock_market.utils.constants import (
    COMMON,
    GBCE_SAMPLE_DATA,
    PREFERRED,
)
from super_simple_stock_market.utils.exceptions import StockNotFoundException

log = logging.getLogger(__name__)
# log.addHandler(logging.StreamHandler())
log.setLevel(logging.INFO)


class StockService:
    def __init__(self, symbol: str, price: float, trade_records: TradeRecords):
        """
        Initialize the requested stock to calculate it based on the given price.
        """
        self.symbol = symbol
        self.price = price
        stock_details = GBCE_SAMPLE_DATA.get(self.symbol)
        if not stock_details:
            log.error(f"No stock details found for the given symbol: {self.symbol}")
            raise StockNotFoundException(self.symbol, self.price)
        self.stock_object = Stock(**stock_details)
        self.stock_price = StockPrice(stock=self.stock_object, price=self.price)
        self.trade_service = TradeService()
        self.trade_records = trade_records

    def get_dividend_yield(self):
        """
        For given stock and price, calculate the dividend yield.
        """
        if self.stock_object.type.lower() == COMMON:
            return self.stock_object.last_dividend / self.price

        elif self.stock_object.type.lower() == PREFERRED:
            return (
                self.stock_object.fixed_dividend * self.stock_object.par_value
            ) / self.price

    def get_pe_ratio(self):
        """
        For given stock and price, calculate the P/E ratio.
        """
        dividend_yield = self.get_dividend_yield()
        try:
            return round(self.price / dividend_yield, 2)
        except ZeroDivisionError:
            log.error(f"Zero dividend yeild i.e.{dividend_yield} for the given stock.")
            return None
        except Exception:
            log.error(f"Error while calculating PE ratio for {self.symbol}")
            return None

    def stock_trade_transaction(
        self, quantity: int, traded_price: float, trade_indicator: str
    ):
        """
        Record a trade, with timestamp, quantity of shares, buy or sell indicator and traded price
        """
        # Creating Trade Transaction
        self.trade_service.create_trade(
            self.symbol, traded_price, quantity, trade_indicator
        )

        # Appending new trade transaction as in list of records.
        self.trade_records.add_trade_record(self.trade_service.trade)
        return self.trade_service.trade.json()

    def get_volume_weighted_stock_price(self):
        """
        Calculate Volume Weighted Stock Price based on trades in past 15 minutes.
        """
        sum_of_traded_price, sum_of_traded_quantity = (
            self.trade_records.get_volume_weighted_trade_details(self.symbol)
        )
        return (sum_of_traded_price * sum_of_traded_quantity) / sum_of_traded_quantity


class StockPriceService:
    def __init__(self):
        self.stock_prices = list()

    def add_stock_price(self, stock_price: StockPrice):
        self.stock_prices.append(stock_price)

    def get_accumulative_price(self):
        return reduce(
            lambda accumulative_price, price: accumulative_price * price,
            self.__list_of_stock_prices(),
        )

    def __list_of_stock_prices(self):
        return [stock_price.price for stock_price in self.stock_prices]
