import logging
from datetime import datetime, timedelta

from super_simple_stock_market.models.trade import Trade
from super_simple_stock_market.utils.exceptions import TradeException

logger = logging.getLogger(__name__)
# logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.INFO)


class TradeService:
    def __init__(self):
        self.trade: Trade = None

    def create_trade(
        self, symbol: str, traded_price: float, quantity: int, trade_type: str
    ) -> Trade:
        logger.info("Creating Trade object.")
        try:
            self.trade = Trade(
                symbol=symbol,
                quantity=quantity,
                traded_price=traded_price,
                trade_type=trade_type,
            )
        except TradeException as ex:
            logger.error("Trade Creation Error: {ex}")
            raise ex


class TradeRecords:
    def __init__(self):
        self.__trades = list()

    def add_trade_record(self, trade: Trade):
        """
        Append the new trade to the Records.
        """
        logger.info("Adding Trade in records")
        self.__trades.append(trade)

    @property
    def trades(self):
        return self.__trades

    def __recent_trades(self, symbol: str):
        """
        Get a list of trades happened in last 15 minutes.
        """
        logger.info(f"Preparing traded for the given symbol: {symbol}")
        past_datetime = datetime.now() - timedelta(minutes=15)
        return [
            trade
            for trade in self.trades
            if not trade.date_timestamp < past_datetime and trade.symbol == symbol
        ]

    def get_volume_weighted_trade_details(self, symbol: str):
        """
        Extract the details required to calculate volume weighted stock price.

        :params symbol str: Abbreivation used for Stock Name.
        """
        recent_trades = self.__recent_trades(symbol)
        logger.info(
            f"Traded from last 15 min. for given symbol: {symbol} are {recent_trades}"
        )

        sum_of_traded_price = sum([trade.traded_price for trade in recent_trades])

        sum_of_traded_quantity = sum([trade.quantity for trade in recent_trades])

        logger.info(
            f"Sum of traded price: {sum_of_traded_price} and quantiy of stocks: {sum_of_traded_quantity}"
        )
        return sum_of_traded_price, sum_of_traded_quantity
