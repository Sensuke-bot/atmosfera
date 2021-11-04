import numpy as np
import pandas as pd
import os
import netCDF4
import matplotlib.pyplot as plt

#%%
""" 
titolo: Flusso del fiume (giornaliero)
descrizione: Il flusso del fiume è la portata in volume del flusso d'acqua che viene trasportato attraverso una data area della sezione trasversale. Esso
è sinonimo di deflusso fluviale o deflusso.
Per ogni periodo di analisi di 30 anni, gli indicatori di portata fluviale sono:
- Media: media dell'intero periodo di tutti i valori giornalieri
- Stagionalità: valori medi di tutti i gennaio, febbraio ecc. che fanno parte del periodo di 30 anni
- Giornaliero: serie temporali giornaliere
Per il periodo di riferimento (1971-2000) sono riportati i valori assoluti, mentre per i periodi futuri i
sono previste le relative modifiche. Gli indicatori sopra descritti sono forniti in un gran numero di file NetCDF. Questo file fa parte della consegna
"""

cwd = os.getcwd()

path = (cwd+"\\cout_ecv_EUR-44_rcp45_IMPACT2C_QM-EOBS_1971-2000_remap0.5.nc")

data = netCDF4.Dataset(path)
print(data)
#%%

print(data.variables.keys())
"""
dict_keys(['lat', 'lon', 'time', 'value1', 'value10', 'value11', 'value12',
'value13', 'value14', 'value15', 'value2', 'value3', 'value4', 'value5',
'value6', 'value7', 'value8', 'value9'])
"""

for d in data.dimensions.items():
    print(d)
"""
#('lat', <class 'netCDF4._netCDF4.Dimension'>: name = 'lat', size = 78)
#('lon', <class 'netCDF4._netCDF4.Dimension'>: name = 'lon', size = 130)
#('time', <class 'netCDF4._netCDF4.Dimension'> (unlimited): name = 'time', size = 10958)
"""
#%%
""" 
ANALISI VARIABILI ASSOCIATE ALLE DIMENISONI
"""

for dname in data.dimensions:
    print(data.variables[dname])

    """ 
    <class 'netCDF4._netCDF4.Variable'>
float32 lat(lat)
    standard_name: latitude
    long_name: Latitude
    units: degrees_north
    axis: Y
unlimited dimensions: 
current shape = (78,)
filling on, default _FillValue of 9.969209968386869e+36 used
<class 'netCDF4._netCDF4.Variable'>
float32 lon(lon)
    standard_name: longitude
    long_name: Longitude
    units: degrees_east
    axis: X
unlimited dimensions: 
current shape = (130,)
filling on, default _FillValue of 9.969209968386869e+36 used
<class 'netCDF4._netCDF4.Variable'>
float64 time(time)
    standard_name: time
    units: days since 1951-01-01 00:00:00
    calendar: proleptic_gregorian
unlimited dimensions: time
current shape = (10958,)
filling on, default _FillValue of 9.969209968386869e+36 used
"""

#%%
from netCDF4 import num2date, date2num, date2index
"""  
NOMI VAR:

dict_keys(['lat', 'lon', 'time', 'value1', 'value10', 'value11', 'value12',
'value13', 'value14', 'value15', 'value2', 'value3', 'value4', 'value5',
'value6', 'value7', 'value8', 'value9'])
"""

value1 = data.variables['value1']

time_dim, lat_dim, lon_dim = value1.get_dims()
time_var = data.variables[time_dim.name]
times = num2date(time_var[:], time_var.units)
latitudes = data.variables[lat_dim.name][:]
longitudes = data.variables[lon_dim.name][:]

output_dir = cwd

#%%

os.makedirs(output_dir, exist_ok=True)
for i, t in enumerate(times):
    filename = os.path.join(output_dir, f'{t.isoformat()}.csv')
    print(f'Writing time {t} to {filename}')
    df = pd.DataFrame(value1[i, :, :], index=latitudes, columns=longitudes)
    df.to_csv('atmo.csv')
print('Done')

#%%

"""  
CONVERSIONE IN CSV
"""


filename = os.path.join(output_dir, 'table.csv')
print(f'Writing data in tabular form to {filename} (this may take some time)...')
times_grid, latitudes_grid, longitudes_grid = [
    x.flatten() for x in np.meshgrid(times, latitudes, longitudes, indexing='ij')]
df = pd.DataFrame({
    'time': [t.isoformat() for t in times_grid],
    'latitude': latitudes_grid,
    'longitude': longitudes_grid,
    't2m': value1[:].flatten()})
df.to_csv(filename, index=False)
print('Done')

