import xarray as xr
import netCDF4
import math
import numpy as np
import matplotlib.pyplot as plt
from scipy import spatial

file_path = 'modis-chlor/A2018057185000.L2_LAC_OC.nc'
# Lat + long of bounding box of the study area (NW corner and SE corner)
latNW = 27.117033
longNW = -82.513229
latSE = 26.358022
longSE = -81.693427

fh = netCDF4.Dataset(file_path, mode='r')
#print(fh)
collectionDate = fh.time_coverage_start[0:10]

nav_dataset = xr.open_dataset(file_path, 'navigation_data')

#print(nav_dataset)

latitude = nav_dataset['latitude']
longitude = nav_dataset['longitude']

# plot a sub-grid
#slat = np.array([arr[::100] for arr in latitude[::100]]).flatten()
#slon = np.array([arr[::100] for arr in longitude[::100]]).flatten()
#plt.scatter(slat, slon)
#plt.show()
latarr = np.array(latitude).flatten()
longarr = np.array(longitude).flatten()
latarr = np.expand_dims(latarr, axis=1)
longarr = np.expand_dims(longarr, axis=1)

points = np.concatenate([latarr, longarr], axis=1)
pointNW = [latNW, longNW]
latlongKDTree = spatial.KDTree(points)
distance,index = latlongKDTree.query(pointNW)
orig_indexNW = np.unravel_index(index, latitude.shape)
pointSE = [latSE, longSE]
distance,index = latlongKDTree.query(pointSE)
orig_indexSE = np.unravel_index(index, latitude.shape)

dataset = xr.open_dataset(file_path, 'geophysical_data')

#print(dataset)
#print('')
#print(dataset.variables)

chlor_a = dataset['chlor_a']
chl_ocx = dataset['chl_ocx']

plt.figure()
plt.imshow(chlor_a[orig_indexSE[0]:orig_indexNW[0], orig_indexSE[1]:orig_indexNW[1]], vmin=0.001, vmax=15)
plt.gca().invert_xaxis()
plt.gca().invert_yaxis()
plt.title(collectionDate + ' Chlorophyll Concentration, OCI Algorithm')
plt.colorbar()

plt.figure()
plt.imshow(chl_ocx[orig_indexSE[0]:orig_indexNW[0], orig_indexSE[1]:orig_indexNW[1]], vmin=0.001, vmax=15)
plt.gca().invert_xaxis()
plt.gca().invert_yaxis()
plt.title(collectionDate + ' Chlorophyll Concentration, OC3 Algorithm')
plt.colorbar()

plt.show()