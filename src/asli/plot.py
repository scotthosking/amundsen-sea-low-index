"""Helper functions for plotting ASLI data"""

import cartopy.crs as ccrs
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import xarray as xr

from .params import ASL_REGION

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
    
    for i in range( int(region['west']),int(region['east']) ): 
        plt.plot([i,i+1], [region['south'],region['south']], 'k-', transform=transform, linewidth=1)
        plt.plot([i,i+1], [region['north'],region['north']], 'k-', transform=transform, linewidth=1)

def plot_lows(da:xr.DataArray, df:pd.DataFrame,
            cmap:str="Reds",
            regionbox:dict=ASL_REGION, coastlines:bool=False):

    plt.figure(figsize=(20,15))

    for i in range(da.shape[0]):
        
        da_2D = da.isel(time=i)

        da_2D = da_2D.sel(latitude=slice(regionbox['north']+10, regionbox['south']-10),
                          longitude=slice(regionbox['west']-10, regionbox['east']-10))

        ax = plt.subplot( 3, 4, i+1, 
                            projection=ccrs.Stereographic(central_longitude=0., 
                                                        central_latitude=-90.) )

        if regionbox:
            ax.set_extent([regionbox['west']-10,
                                     regionbox['east']-10,
                                     regionbox['south']-10,
                                     regionbox['north']+10],
                                    ccrs.PlateCarree())

        da_2D.plot.contourf('longitude', 'latitude', cmap=cmap, 
                        transform=ccrs.PlateCarree(), 
                        add_colorbar=False, 
                        levels=np.linspace(np.nanmin(da_2D.values), np.nanmax(da_2D.values), 20) )

        if coastlines: ax.coastlines(resolution='110m')

        ax.set_title(str(da_2D.time.values)[0:7])

        ## mark ASL
        df2 = df[df['time'] == str(da_2D.time.values)[0:10]]
        if len(df2) > 0:
            ax.plot(df2['lon'], df2['lat'], 'mx', transform=ccrs.PlateCarree() )

        if regionbox: draw_regional_box(regionbox)

    return ax