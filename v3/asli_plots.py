import xarray as xr
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import cartopy.crs as ccrs


### Update this as the ASL / low detection algorithm is updated
### version_id = 3.<DATE>
version_id = '3.20210820' 


def draw_regional_box( region, transform=None ):
    '''
    Draw box around a region on a map
    region is a dictionary with west,east,south,north
    '''

    if transform == None:
        transform = ccrs.PlateCarree()

    plt.plot([region['west'], region['west']], [region['south'],region['north']], 
                 'k-', transform=transform, linewidth=1)
    plt.plot([region['east'], region['east']], [region['south'],region['north']], 
                 'k-', transform=transform, linewidth=1)
    
    for i in range( np.int(region['west']),np.int(region['east']) ): 
        plt.plot([i,i+1], [region['south'],region['south']], 'k-', transform=transform, linewidth=1)
        plt.plot([i,i+1], [region['north'],region['north']], 'k-', transform=transform, linewidth=1)

def slice_region(da, region, boarder=5):
    da = da.sel( latitude=slice(region['north']+boarder,region['south']-boarder), 
                longitude=slice(region['west']-boarder,region['east']+boarder))
    return da

#---------------------------
# Plotting
#---------------------------

da   = xr.open_mfdataset('../INDATA/ERA5/monthly/era5_mean_sea_level_pressure_monthly*.nc').msl
da   = da.isel(expver=0)
mask = xr.open_dataset('../INDATA/ERA5/era5_invariant_lsm.nc').lsm.squeeze()

da_mask = da.where(mask == 0)

# region of interest (asl sector)
asl_region = {'west':170., 'east':298., 'south':-80., 'north':-60.}

### slice area around ASL region
da      = slice_region(da, asl_region)
da_mask = slice_region(da_mask, asl_region)

# change units
da = da  / 100. 
da = da.assign_attrs(units='hPa')

all_lows_dfs = pd.read_csv('era5/all_lows_v'+version_id+'-era5.csv', comment='#')
asl_df       = pd.read_csv('era5/asli_v'+version_id+'-era5.csv', comment='#')

for yr in range(1979,2022):

    print('plotting ', yr, version_id)
    plt.figure(figsize=(20,15))

    da_yr = da_mask.sel(time=str(yr))

    for m in da_yr.time.dt.month.values:

        da_2D = da_yr.sel(time=str(yr)+'-'+str('{:02d}'.format(m))).squeeze()
        
        plt.suptitle(yr, fontsize=32)
        
        ax = plt.subplot( 3, 4, m, 
                            projection=ccrs.Stereographic(central_longitude=0., 
                                                          central_latitude=-90.) )

        ax.set_extent([165,305,-85,-55], ccrs.PlateCarree())

        result = da_2D.plot.contourf( 'longitude', 'latitude', cmap='Reds', 
                                        transform=ccrs.PlateCarree(), 
                                        add_colorbar=False, 
                                        levels=np.linspace(np.nanmin(da_2D.values), np.nanmean(da_2D.values), 20) )

        ax.set_title(str(da_2D.time.values)[0:7])

        ## mark lows
        df2 = all_lows_dfs[ all_lows_dfs['time'] == str(da_2D.time.values)[0:10]]
        if len(df2) > 0:
            for index, row in df2.iterrows():
                ax.plot(row['lon'], row['lat'], 'mx', transform=ccrs.PlateCarree() )

        ## mark asl
        df3 = asl_df[ asl_df['time'] == str(da_2D.time.values)[0:10]]
        if len(df3) > 0:
            for index, row in df3.iterrows():
                ax.plot(row['lon'], row['lat'], 'g+', transform=ccrs.PlateCarree() )

        draw_regional_box(asl_region)

    plt.savefig('era5/testing/asli_v3_era5_'+str(yr)+'_'+version_id+'.png', dpi=150)
    plt.close()