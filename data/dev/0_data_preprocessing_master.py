from sp500_data import IntegrateSPData
from volatility_data import IntegrateVolatilityData
from sp500_data_merge import MergeSPWithMaster
from make_data_yearly import MakeYearly
from clean_tenure import CleanTenure
from integrate_age import IntegrateAge
from make_panel import MakePanel
from create_roletenure import CreateRoleTenure
from integrate_conversion_data import IntegrateConversionData
from integrate_stock import IntegrateStockData
from dev_lib import timed_execution


def sagemaker_main():
    # NICO
    master_output = "master_data.csv"
    tenure_input = "DirectorTurnoverData.csv"
    step_1 = CleanTenure(tenure_input, master_output, input_type='s3', output_type='s3')
    step_1.process()

    age_data = "DirectorIDByDOB.csv"
    step_2 = IntegrateAge(master_output, age_data, master_output, input_type='s3', age_data_type='s3', output_type='s3')
    step_2.process()

    step_3 = MakePanel(master_output, master_output, input_type='s3', output_type='s3')
    step_3.process()

    step_4 = CreateRoleTenure(master_output, master_output, input_type='s3', output_type='s3')
    step_4.process()

    conversion_data = "conversion_dataset.csv"
    step_5 = IntegrateConversionData(master_output, conversion_data, master_output,
                                     input_type='s3', conversion_type='s3', output_type='s3')
    step_5.process()

    # OZZI
    pass

    


def main():
    
    #-------Nico Section-------#

    #Creating the master CSV
    master = "csv_files/master_data.csv"

    # 1) Cleaning tenure
    tenure_data = "csv_files/DirectorTurnoverData.csv"
    step_1 = CleanTenure(tenure_data, master)
    step_1.process()

    # 2) Integrating age
    age_data = "csv_files/DirectorIDByDOB.csv"
    step_2 = IntegrateAge(master, age_data, master)
    step_2.process()

    # 3) Making the dataset panel
    step_3 = MakePanel(master, master)
    step_3.process()

    # 4) Differentiating between role and company tenure
    step_4 = CreateRoleTenure(master, master)
    step_4.process()

    #-------Ozzi Section-------#

    initial_master = "csv_files/master_data_monthly.csv"
    intermediate_master = "csv_files/master_data_monthly_temp.csv"
    final_master_monthly = "csv_files/master_data_monthly_final.csv"
    final_master_yearly = "csv_files/master_data_yearly_final.csv"

    sp500_raw = "csv_files/SP500-Monthly-2000"
    sp500_processed = "csv_files/sp500-returns-volatility.csv"

    volatility_data = IntegrateVolatilityData(initial_master, intermediate_master)
    sp_data = IntegrateSPData(sp500_raw, sp500_processed)
    master_monthly = MergeSPWithMaster(intermediate_master, sp500_processed, final_master_monthly)
    master_yearly = MakeYearly(final_master_monthly, final_master_yearly)

    volatility_data.process()
    sp_data.process()
    master_monthly.process()
    master_yearly.process()
