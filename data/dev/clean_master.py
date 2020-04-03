from dev_lib import IntegrateData


class CleanMasterData(IntegrateData):

    def __init__(self, data_path, in_type='csv', out_type='csv'):
        super().__init__(data_path, data_path, input_type=in_type, output_type=out_type)

    def integrate_data(self):

        id_cols = ['datadate', 'sic', 'gvkey', 'iid', 'tic', 'cusip', 'conm']
        returns_cols = ["trailing_{}_mo_return".format(n) for n in [1, 3, 6, 12, 24, 36]]
        vol_cols = ["trailing_{}_mo_volatility".format(n) for n in [3, 6, 12]]
        market_cols = ['{}mo_sp_return'.format(n) for n in [12, 24, 36]] + \
            ['{}mo_sp_volatility'.format(n) for n in [12, 24, 36]]

        data_cols = id_cols + returns_cols + vol_cols + market_cols

        self.data = self.data[data_cols]
        self.data.sort_values(by=['sic', 'gvkey'])

        super().integrate_data()
