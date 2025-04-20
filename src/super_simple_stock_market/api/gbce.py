import logging
import math

from super_simple_stock_market.services.stock_service import (
    StockPriceService,
    StockService,
    TradeRecords,
)

logger = logging.getLogger(__name__)
# Create a formatter to define the log format
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.INFO)


class StockAPI:
    def __init__(self):
        self.symbol: str = None
        self.stock_price: float = None
        self.quantity: int = None
        self.transaction_type: str = None
        self.traded_price: float = None

        # Adding new transaction is a mutable operation which will keep on adding new items to the list.
        # This will keep the trade records in memory to perform operations.
        self.trade_records = TradeRecords()
        self.stock_prices = StockPriceService()

    def initialize_by_inputs(self):
        """
        Initialize as user manual inputs rather than passing as in command line args to the script.
        """
        print("Enter Stock Details: \n ")
        self.symbol = input("SYMBOL: ")
        self.stock_price = float(input("STOCK PRICE: "))
        self.transaction_type = input("BUY/SELL: ")
        self.quantity = int(input(f"QUANTITY {self.transaction_type.capitalize()}: "))
        self.traded_price = float(input("TRADE PRICE: "))

    def get_all_share_index_geometric_mean(self):
        """
        Calculate the GBCE All Share Index using the geometric mean of prices for all stocks
        """
        all_share_price_geometric_mean = float(
            math.pow(
                self.stock_prices.get_accumulative_price(),
                (1 / len(self.stock_prices.stock_prices)),
            )
        )
        return all_share_price_geometric_mean

    def run(self):
        """
        Initialize Stock Services and execute required operations.
        E.g.
            - Calculate and get dividend yield
            - Calculate and get p/e ratio
            - Record the transaction
            - Calculate volume weighted stock price based on the trades in past 15 min.
            - Calculate the GBCE All Share Index using the geometric mean of prices for all stocks
        """
        try:
            stock_service = StockService(
                self.symbol, self.stock_price, self.trade_records
            )
            # Following will manage stock object and given price.
            self.stock_prices.add_stock_price(stock_service.stock_price)

            # Log the operations on given stock and price.
            logger.info(f"{self.symbol} STOCK DETAILS, \n")
            logger.info(f"DIVIDEND YIELD: {stock_service.get_dividend_yield()}")
            logger.info(f"PE RATIO: {stock_service.get_pe_ratio()}")
            trade_transaction_details = stock_service.stock_trade_transaction(
                self.quantity, self.traded_price, self.transaction_type
            )
            logger.info(f"RECORDED TRADE DETAILS: {trade_transaction_details}")
            logger.info(
                f"VOLUME WEIGHTED STOCK PRICE: {stock_service.get_volume_weighted_stock_price()}"
            )
            logger.info("\n========================================\n")
        except Exception as ex:
            logger.error(f"Error while performing stock details. {ex}")


if __name__ == "__main__":
    stock_api = StockAPI()
    continue_ = "yes"
    while continue_.lower() in ("yes", "y"):
        stock_api.initialize_by_inputs()
        stock_api.run()

        continue_ = input("Do you want continue more transactions (yes/no):")

    logger.info(
        f"\nGBSE Index / GEOMETRIC MEAN: {stock_api.get_all_share_index_geometric_mean()} \n\n"
    )
