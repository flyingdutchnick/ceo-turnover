import pandas as pd
import numpy as np
from integrate_stock import IntegrateStockData
from volatility_data import IntegrateVolatilityData
from sp500_data import IntegrateSPData
from sp500_data_merge import MergeSPWithMaster


""" 1. Constructing initial stock performance dataset (without market returns)"""


# location of raw wrds Compustat share price dataset
stock_data_no_returns_path = "csv_files/SharePriceData.csv"

# eventual location of share price dataset with returns added
stock_data_with_returns_path = "csv_files/StockDataWithReturns.csv"

# initialize IntegrateStockData instance to calculate share price returns and add them to the dataset
stock_data_add_returns = IntegrateStockData(stock_data_no_returns_path, stock_data_with_returns_path)

# calculates returns data from imported share price data and writes combined data to specified output path
stock_data_add_returns.process()

# eventual location of share price dataset with returns and volatility data
stock_data_returns_volatility_path = "csv_files/StockDataWithReturnsVolatility.csv"

# initialize IntegrateVolatilityData instance to calculate volatility of returns and add them to the dataset
stock_data_add_volatility = IntegrateVolatilityData(stock_data_with_returns_path, stock_data_returns_volatility_path)

# calculates volatility data from imported returns data and writes combined data to specified output path
stock_data_add_volatility.process()


""" 2. Constructing market performance dataset """


# path to csv file with SP500 monthly trade activity downloaded from Yahoo Finance
market_price_data_path = "csv_files/SP500-Monthly-2000.csv"

# eventual path to csv file with SP500 monthly returns
market_returns_data_path = "csv_files/SPMonthlyReturns.csv"

# initialize IntegrateSPData instance to calculate sp500 returns from adj. monthly trading close
market_price_to_returns = IntegrateSPData(market_price_data_path, market_returns_data_path)

# calculates returns data from imported sp500 price and writes combined data to specified output path
market_price_to_returns.process()


""" 3. Merging individual stock and market performance datasets """

# final data output
master_data_path = "csv_files/MasterPerformanceData.csv"

# initialize MergeSPWithMaster instance to marge stock performance and market performance datasets
merge_stock_market = MergeSPWithMaster(
    stock_data_returns_volatility_path, market_returns_data_path, master_data_path)

# merge the two datasets and write to master
merge_stock_market.process()
