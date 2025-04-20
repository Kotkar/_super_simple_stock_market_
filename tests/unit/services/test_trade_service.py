from unittest import mock

import pytest

from super_simple_stock_market.services.trade_service import (
    TradeException,
    TradeService,
)


class TestTradeService:
    @mock.patch("super_simple_stock_market.services.trade_service.Trade")
    def test_create_trade(self, mock_trade):
        symbol = "POP"
        quantity = 100
        traded_price = 50
        trade_type = "BUY"

        trade_service_obj = TradeService()
        trade_service_obj.create_trade(
            symbol="POP", quantity=100, traded_price=50, trade_type="BUY"
        )
        mock_trade.assert_called_once_with(
            symbol=symbol,
            quantity=quantity,
            traded_price=traded_price,
            trade_type=trade_type,
        )

    @mock.patch("super_simple_stock_market.services.trade_service.Trade")
    def test_create_trade_with_exception(self, mock_trade):
        trade_service_obj = TradeService()
        mock_trade.side_effect = TradeException("Error")

        with pytest.raises(TradeException) as ex:
            trade_service_obj.create_trade(
                symbol="POP", quantity=100, traded_price=50, trade_type="BUY"
            )
        assert str(ex.value) == "Error"
