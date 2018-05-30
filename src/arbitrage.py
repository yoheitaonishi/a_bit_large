# coding:utf-8

import sys
import configparser
import json
import ccxt
import urllib.request, urllib.error
import math
import requests
from decimal import (Decimal, ROUND_DOWN)
from order_logging import logger

from IPython import embed
from IPython.terminal.embed import InteractiveShellEmbed

ARBITRAGE_PAIR = "ETH/BTC"
BUY_COIN_SYMBOL_AT_BINANCE = 'BTC'
SELL_COIN_SYMBOL_AT_BINANCE = 'ETH'
BUY_COIN_SYMBOL_AT_HUOBIPRO = 'btc'
SELL_COIN_SYMBOL_AT_HUOBIPRO = 'eth'
ARBITRAGE_RATIO = 0.05


"""
Order by bids price
It doesn't mater bids or asks so just compare to bids price
"""


def get_balance(binance, huobi, order_type):
    binance_balances = binance.fetch_balance()['info']['balances']
    huobipro_balances = binance.fetch_balance()['info']['list']
    if order_type == "BUY":
        for binance_balance in binance_balances:
            if binance_balance['asset'] == BUY_COIN_SYMBOL_AT_BINANCE:
                buy_balance = binance_balance['free']
                break
        for huobipro_balance in huobipro_balances:
            if huobipro_balance['currency'] == SELL_COIN_SYMBOL_AT_HUOBIPRO:
                sell_balance = huobipro_balance['balance']
                break
    elif order_type == "SELL":
        for huobipro_balance in huobipro_balances:
            if huobipro_balance['currency'] == BUY_COIN_SYMBOL_AT_HUOBIPRO:
                buy_balance = huobipro_balance['balance']
                break
        for binance_balance in binance_balances:
            if binance_balance['asset'] == SELL_COIN_SYMBOL_AT_BINANCE:
                sell_balance = binance_balance['free']
                break
    return [buy_balance, sell_balance]

def apply_order(binance, huobipro, buy_balance, sell_balance, order_type):
    buy_balance = round_down2(buy_balance)
    sell_balance = round_down2(sell_balance)
    if order_type == "BUY":
        binance.create_market_buy_order(BUY_COIN_SYMBOL_AT_BINANCE, buy_balance)
        huobipro.create_market_sell_order(SELL_COIN_SYMBOL_AT_HUOBIPRO, sell_balance)
    elif order_type == "SELL":
        binance.create_market_sell_order(SELL_COIN_SYMBOL_AT_BINANCE, sell_balance)
        huobipro.create_market_buy_order(BUY_COIN_SYMBOL_AT_HUOBIPRO, buy_balance)

# 修正する
def set_api_key(client, api_key, api_secret):
    client.apiKey = api_key
    client.secret = api_secret
    return client

# 全pairを調べて、一番裁定が大きいものを設定する
def check_arbitrage_on_binance():
    binance = ccxt.binance()
    huobipro = ccxt.huobipro()
    binance_price = get_price(binance)
    huobipro_price = get_price(huobipro)
    arbitrage = (binance_price - huobipro_price) / binance_price
    abs_arbitrage = abs(arbitrage)
    if abs_arbitrage >= ARBITRAGE_RATIO:
        if arbitrage > 0:
            return [True, "BUY"]
        elif arbitrage < 0:
            return [True, "SELL"]
    else:
        return [False]

def get_price(client):
    bits = client.fetch_order_book(ARBITRAGE_PAIR)["bids"]
    prices = []
    for bit in bits:
        prices.append(bit)
    price = median(prices)
    return price

def round_down2(value):
    value = Decimal(value).quantize(Decimal('0.01'), rounding=ROUND_DOWN)
    return str(value)
