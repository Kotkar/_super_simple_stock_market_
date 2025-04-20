from unittest import mock
from unittest.mock import MagicMock

import pytest

from super_simple_stock_market.services.stock_service import (
    Stock,
    StockNotFoundException,
    StockPriceService,
    StockService,
    TradeService,
)


class TestStockService:
    def test_initialize_stock_service_when_symbol_exists(self):
        """
        Test initialization of stock service object with required parameters.
        """
        trade_records = MagicMock()
        price = 50
        symbol = "TEA"

        stock_service_obj = StockService(symbol, price, trade_records)

        assert isinstance(stock_service_obj.stock_object, Stock)
        assert isinstance(stock_service_obj.trade_service, TradeService)

    def test_initialize_stock_when_symbol_not_exists(self):
        """
        Test initialization of stock service object with required parameters when symbol doesn't exists.

        This time it should throw an error.
        """
        trade_records = MagicMock()
        price = 50
        symbol = "XYZ"

        with pytest.raises(StockNotFoundException) as ex:
            StockService(symbol, price, trade_records)
        assert str(ex.value) == "('XYZ', 50)"

    def test_initialize_stock_with_negative_value(self):
        """
        Validate if price is 0 or < 0.
        """
        trade_records = MagicMock()
        price = 0
        symbol = "TEA"

        with pytest.raises(ValueError) as ex:
            StockService(symbol, price, trade_records)
        assert str(ex.value.errors()[0]["msg"]) == "Value error, Price should be > 0"

    def test_dividend_yield_common_type(self):
        """
        Test dividend yield if common type
        """
        trade_records = MagicMock()
        price = 50
        symbol = "TEA"

        stock_service_obj = StockService(symbol, price, trade_records)
        #  0 / 50
        dividend_yield = stock_service_obj.get_dividend_yield()
        assert dividend_yield == 0.0

    def test_dividend_yield_preferred_type(self):
        """
        Test dividend yield if common type
        """
        trade_records = MagicMock()
        price = 50
        symbol = "GIN"

        stock_service_obj = StockService(symbol, price, trade_records)
        #  0 / 50
        dividend_yield = stock_service_obj.get_dividend_yield()
        assert dividend_yield == 4.0

    def test_get_pe_ratio(self):
        """
        Valid pe ratio
        """
        trade_records = MagicMock()
        price = 50
        symbol = "JOE"

        stock_service_obj = StockService(symbol, price, trade_records)

        pe_ratio = stock_service_obj.get_pe_ratio()

        assert pe_ratio == 192.31

    def test_get_pe_ratio_with_zero_dividend_yield(self):
        """
        InValid pe ratio to prevent zero division error
        """
        trade_records = MagicMock()
        price = 50
        symbol = "TEA"
        stock_service_obj = StockService(symbol, price, trade_records)
        pe_ratio = stock_service_obj.get_pe_ratio()
        assert not pe_ratio

    @mock.patch("super_simple_stock_market.services.stock_service.TradeService")
    def test_stock_trade_transaction(self, mock_trade_service):
        """
        Test case to valid the trade.
        """
        trade_records = MagicMock()
        price = 50
        symbol = "TEA"

        trade_service_obj = MagicMock()
        mock_trade_service.return_value = trade_service_obj

        stock_service_obj = StockService(symbol, price, trade_records)
        quantity, traded_price, trade_indicator = 10, 51, "BUY"

        trade_obj = MagicMock()
        trade_service_obj.trade = trade_obj

        stock_service_obj.stock_trade_transaction(
            quantity, traded_price, trade_indicator
        )
        trade_service_obj.create_trade.assert_called_once_with(
            symbol, traded_price, quantity, trade_indicator
        )
        trade_records.add_trade_record.assert_called_once_with(trade_obj)

    def test_get_volume_weighted_stock_price(self):
        """
        Validate the output for volume weighted stock price..
        """
        trade_records = MagicMock()
        price = 50
        symbol = "TEA"

        stock_service_obj = StockService(symbol, price, trade_records)
        trade_records.get_volume_weighted_trade_details.return_value = 10, 20
        # ((sum_of_traded_price * sum_of_traded_quantity) / sum_of_traded_quantity)

        result = stock_service_obj.get_volume_weighted_stock_price()
        assert result == 10


class TestStockPriceService:
    def test_initialize_stock_price_service(self):
        obj = StockPriceService()
        assert hasattr(obj, "stock_prices")

    @mock.patch("super_simple_stock_market.services.stock_service.StockPrice")
    def test_add_stock_price(self, mock_stock_price):
        stock_price_obj = MagicMock()
        obj = StockPriceService()
        obj.add_stock_price(stock_price_obj)
        assert len(obj.stock_prices) == 1
