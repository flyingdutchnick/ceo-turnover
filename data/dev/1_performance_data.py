from integrate_stock import IntegrateStockData
from volatility_data import IntegrateVolatilityData
from sp500_data import IntegrateSPData
from sp500_data_merge import MergeSPWithMaster
from clean_master import CleanMasterData


""" 1. Constructing initial stock performance dataset (without market returns) """

def step_1():

    # location of raw wrds Compustat share price dataset
    stock_data_no_returns_path = "csv_files/na-monthly-share-price.csv"

    # eventual location of share price dataset with returns added
    stock_data_with_returns_path = "csv_files/stock-monthly-returns.csv"

    # initialize IntegrateStockData instance to calculate share price returns and add them to the dataset
    stock_data_add_returns = IntegrateStockData(stock_data_no_returns_path, stock_data_with_returns_path)

    # calculates returns data from imported share price data and writes combined data to specified output path
    stock_data_add_returns.process()

    # eventual location of share price dataset with returns and volatility data
    stock_data_returns_volatility_path = "csv_files/stock-monthly-returns-volatility.csv"

    # initialize IntegrateVolatilityData instance to calculate volatility of returns and add them to the dataset
    stock_data_add_volatility = IntegrateVolatilityData(stock_data_with_returns_path, stock_data_returns_volatility_path)

    # calculates volatility data from imported returns data and writes combined data to specified output path
    stock_data_add_volatility.process()


""" 2. Constructing SP performance dataset """

def step_3():

    # path to csv file with SP500 monthly trade activity downloaded from Yahoo Finance
    market_price_data_path = "csv_files/sp500-monthly-price.csv"

    # eventual path to csv file with SP500 monthly returns
    market_returns_data_path = "csv_files/SPMonthlyReturns.csv"

    # initialize IntegrateSPData instance to calculate sp500 returns from adj. monthly trading close
    market_price_to_returns = IntegrateSPData(market_price_data_path, market_returns_data_path)

    # calculates returns data from imported sp500 price and writes combined data to specified output path
    market_price_to_returns.process()


""" 3. Merging individual stock and market performance datasets """


def step_3():

    stock_data_returns_volatility_path = "csv_files/stock-monthly-returns-volatility.csv"

    market_returns_data_path = "csv_files/SPMonthlyReturns.csv"

    # final data output
    master_data_path = "csv_files/MasterPerformanceData.csv"

    # initialize MergeSPWithMaster instance to marge stock performance and market performance datasets
    merge_stock_market = MergeSPWithMaster(
        stock_data_returns_volatility_path, market_returns_data_path, master_data_path)

    # merge the two datasets and write to master
    merge_stock_market.process()


""" 4. Data cleaning """

def step_4():

    master_data_path = "csv_files/MasterPerformanceData.csv"

    clean_master = CleanMasterData(master_data_path)
    clean_master.process()

step_3()
step_4()