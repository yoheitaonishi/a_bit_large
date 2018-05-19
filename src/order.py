# coding:utf-8

import sys
import configparser
import json
import ccxt
import binance.client
import kucoin.client
import urllib.request, urllib.error
import math
import requests
from decimal import (Decimal, ROUND_DOWN)
sys.path.append('../')
from order_logging import logger

from IPython import embed
from IPython.terminal.embed import InteractiveShellEmbed

COIN_TYPE = "BTC"

def get_price(api_key, api_secret, exchange_type):
    client = ccxt.huobipro()
    client.apiKey = api_key
    client.secret = api_secret
