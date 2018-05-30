import logging

logger = logging.getLogger('ArbitrageLogging')
logger.setLevel(10)
fh = logging.FileHandler('log/arbitrage.log')
logger.addHandler(fh)
sh = logging.StreamHandler()
logger.addHandler(sh)
formatter = logging.Formatter('%(asctime)s:%(lineno)d:%(levelname)s:%(message)s')
fh.setFormatter(formatter)
sh.setFormatter(formatter)
