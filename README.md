# Super Simple Stock Market

Example Assignment – Super Simple Stock Market

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install dependencies.

```bash
pip install uv
make venv
source .venv/bin/activate
make install
export SOURCE_DIR=~/super_simple_stock_market/src
```

## Usage

```
cd ~/super_simple_stock_market/src
python -m super_simple_stock_market.api.gbce

>>> Enter Stock Details:
SYMBOL: POP
STOCK PRICE: 50
BUY/SELL: BUY
QUANTITY Buy: 50
TRADE PRICE: 50
POP STOCK DETAILS,

DIVIDEND YIELD: 0.16
PE RATIO: 312.5
RECORDED TRADE DETAILS: {"symbol":"POP","date_timestamp":"2025-04-20T15:51:29.649200","quantity":50,"trade_type":"BUY","traded_price":50.0}
VOLUME WEIGHTED STOCK PRICE: 50.0
========================================
Do you want continue more transactions (yes/no):no
GBSE Index / GEOMETRIC MEAN: 50.0

```


## Test

```
export PYTHONPATH=~/super_simple_stock_market/src
make test
make cov
```