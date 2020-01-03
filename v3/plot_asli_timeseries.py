import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# Read in ASL data
filename   = 'https://github.com/scott-hosking/amundsen_sea_low_index/raw/master/asli_era5_v3-latest.csv'
asli       = pd.read_csv(filename, comment='#')
asli['time'] = pd.to_datetime(asli['time'])
asli = asli.set_index('time')

def hamming(ts):
    # Hamming window (normalise first so integral equals 1)
    hamm = np.hamming(11) / np.sum(np.hamming(11))
    filt = np.convolve(hamm, ts, mode='same')
    return filt


# Plot lon
fig = plt.figure(figsize=(8, 4))

col = asli['lon']
ax = fig.add_subplot( 1, 1, 1)

ax.plot(asli.index, col, color='grey', linewidth=0.8, label='monthly')
ax.plot(asli.index[5:-5], hamming(col)[5:-5], color='black', linewidth=1.4, label='11-point Hamming')

ax.set_title('Time series of monthly mean ASL longitude index (v3)')
ax.set_xlabel('Time (years)')
ax.set_ylabel('ASL longitude ($^\circ$E)')

ax.legend(loc='lower right', prop={'size':8})

plt.tight_layout()
plt.savefig('asli_era5_v3_lon_monthly_timeseries.png', dpi=100)




# Plot all timeseries
fig = plt.figure(figsize=(8, 11))

for i, p in enumerate(asli.columns):

    col = asli[p]

    print(col.name)

    ax = fig.add_subplot( len(asli.columns), 1, i+1)

    ax.plot(asli.index, col, color='grey', linewidth=0.8, label='monthly')
    ax.plot(asli.index[5:-5], hamming(col)[5:-5], color='black', linewidth=1.4, label='11-point Hamming')

    # ax.set_title('Time series of monthly mean ASL longitude index (v3)')
    ax.set_xlabel('Time (years)')
    ax.set_ylabel(col.name)

    if i+1 == len(asli.columns):
        ax.legend(loc='lower right', prop={'size':8})

plt.suptitle('ASL indices (v3)', fontsize=24)

# plt.tight_layout()
plt.savefig('../asli_era5_v3_monthly_timeseries.png', dpi=100)
