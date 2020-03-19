from sp500_data import IntegrateSPData
from volatility_data import IntegrateVolatilityData
from sp500_data_merge import MergeSPWithMaster
from make_data_yearly import MakeYearly


initial_master = "csv_files/master_data_monthly.csv"
intermediate_master = "csv_files/master_data_monthly_temp.csv"
final_master_monthly = "csv_files/master_data_monthly_final.csv"
final_master_yearly = "csv_files/master_data_yearly_final.csv"

sp500_raw = "csv_files/SP500-Monthly-2000"
sp500_processed = "csv_files/SP500-Returns-Volatility.csv"

volatility_data = IntegrateVolatilityData(initial_master, intermediate_master)
sp_data = IntegrateSPData(sp500_raw, sp500_processed)
master_monthly = MergeSPWithMaster(intermediate_master, sp500_processed, final_master)
master_yearly = MakeYearly(final_master_monthly, final_master_yearly)

volatility_data.process()
sp_data.process()
master_monthly.process()
master_yearly.process()
