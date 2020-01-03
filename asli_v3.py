import xarray as xr
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
from skimage.feature import peak_local_max

ds   = xr.open_dataset('~/Desktop/era5_mean_sea_level_pressure_monthly.nc')
mask = xr.open_dataset('~/Desktop/era5_invariant_lsm.nc').lsm.squeeze()

da = ds.msl

da_mask = da.where(mask == 0)
da_mask.mean().values, da.mean().values # these are different, great!

da = da.sel(latitude=slice(-55,-90))

def get_lows(da, threshold=None, sigma=None):
    
    import scipy.ndimage as ndimage
    img = ndimage.gaussian_filter(da.values, sigma=sigma)
    da.values = img
    
    invert_data = (da*-1.).values     # search for peaks rather than minima
    
    if threshold is None:
        threshold_abs = invert_data.mean()
    else:
        threshold_abs  = threshold * -1  # define threshold cut-off for peaks (inverted lows)
                
    minima_yx = peak_local_max(invert_data,            # input data
                           min_distance=1,             # peaks are separated by at least min_distance
                           num_peaks=12,                # maximum number of peaks
                           exclude_border=True,        # excludes peaks from within min_distance - pixels of the border
                           threshold_abs=threshold_abs # minimum intensity of peaks
                           )
    return minima_yx



def sector_mean(da, dict):
    a = da.sel( latitude=slice(asl_region['north'],asl_region['south']), 
                longitude=slice(asl_region['west'],asl_region['east']) ).mean()
    return a



def get_asl(da, region, mask, sigma=11):
    '''
    da for one point in time (with lats x lons)
    '''
    
    lons, lats = da.longitude.values, da.latitude.values
    
    sector_mean_pres = sector_mean(da.where(mask == 0), region).values
    threshold = sector_mean_pres

    time_str = str(da.time.values)[:10]
    
    # fill land in with highest value to limit lows being found here
    da_max   = da.max().values
    da       = da.where(mask == 0).fillna(da_max)
    
    ### get lows for entire domain
    minima_yx = get_lows(da, threshold, sigma)
    
    minima_lat, minima_lon, pressure = [], [], []
    for minima in minima_yx:
        minima_lat.append(lats[minima[0]])
        minima_lon.append(lons[minima[1]])
        pressure.append(da.values[minima[0],minima[1]])
    
    df = pd.DataFrame()
    df['lat']      = minima_lat
    df['lon']      = minima_lon
    df['pressure'] = pressure
    df['ASL_Sector_Pres'] = sector_mean_pres
    df['time']     = time_str
    
    ### select only those points within ASL box
    asl_df = df[(df['lon'] > region['west'])  & 
                (df['lon'] < region['east'])  & 
                (df['lat'] > region['south']) & 
                (df['lat'] < region['north']) ]

    ### For each time, get the row with the lowest minima_number
    asl_df = asl_df.loc[asl_df.groupby('time')['pressure'].idxmin()]
    
    if len(asl_df) == 0:
        print('no asl present', time_str)
        asl_df = pd.DataFrame()
        asl_df['lat']      = [np.nan]
        asl_df['lon']      = [np.nan]
        asl_df['pressure'] = [np.nan]
        asl_df['ASL_Sector_Pres'] = [np.nan]
        asl_df['time']     = [time_str]
    
    asl_df = asl_df[['time','lon','lat','pressure','ASL_Sector_Pres']]
    
    return asl_df

asl_region = {'west':170., 'east':298., 'south':-80., 'north':-60.}

ntime      = da.time.shape[0]

all_lows_df = pd.DataFrame()
asl_df      = pd.DataFrame()

for t in range(0,ntime):
    da_t   = da.isel(time=t) / 100.
    asl_df = pd.concat([asl_df, get_asl(da_t, asl_region, mask, sigma=11)]).reset_index(drop=True)

# asl_df.to_csv('v3/era5/asli_v3_era5.csv', index=False)


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


for yr in range(1981,1982):

    plt.figure(figsize=(20,15))

    for i in range(0,12):

        da_2D = da_mask.isel(time=((yr-1979)*12)+i)
        
        da_2D = da_2D.sel(latitude=slice(-55,-90),longitude=slice(165,305))
        
        plt.suptitle(yr, fontsize=32)
        
        ax = plt.subplot( 3, 4, i+1, 
                            projection=ccrs.Stereographic(central_longitude=0., 
                                                          central_latitude=-90.) )

        ax.set_extent([165,305,-85,-55], ccrs.PlateCarree())

        result = da_2D.plot.contourf( 'longitude', 'latitude', cmap='Reds', 
                                        transform=ccrs.PlateCarree(), 
                                        add_colorbar=False, 
                                        levels=np.linspace(np.nanmin(da_2D.values), np.nanmax(da_2D.values), 20) )

        # ax.coastlines(resolution='110m')
        ax.set_title(str(da_2D.time.values)[0:7])

        ## mark ASL
        df2 = asl_df[ asl_df['time'] == str(da_2D.time.values)[0:10]]
        if len(df2) > 0:
            ax.plot(df2['lon'], df2['lat'], 'mx', transform=ccrs.PlateCarree() )
        draw_regional_box(asl_region)

    plt.savefig('v3/era5/testing/asli_v3_era5_'+str(yr)+'.png', dpi=150)    
    print('')



