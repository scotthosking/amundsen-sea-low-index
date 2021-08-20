from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

import cdsapi

variables = [
    # '10m_u_component_of_wind',
    # '10m_v_component_of_wind',
    '2m_temperature',
    'mean_sea_level_pressure']

for yr in range(1979,2022):

    for variable in variables:

        print(variable)

        c = cdsapi.Client()
        c.retrieve(
            'reanalysis-era5-single-levels-monthly-means',
            {
                'product_type':'monthly_averaged_reanalysis',
                'variable':variable,
                'year':str(yr),
                'month':[
                    '01','02','03',
                    '04','05','06',
                    '07','08','09',
                    '10','11','12'
                ],
                'time':'00:00',
                'format':'netcdf'
            },
            '../INDATA/ERA5/monthly/era5_'+variable+'_monthly_'+str(yr)+'.nc')
