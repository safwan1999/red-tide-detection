import xarray as xr
import netCDF4
import math
import numpy as np
import matplotlib.pyplot as plt
from scipy import spatial

file_path = 'modis-chlor/A2020040184500.L2_LAC_OC.nc'
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
nflh = dataset['nflh']
RRS_443 = dataset['Rrs_443']
RRS_555 = dataset['Rrs_555']

#QAA to derive b_bp from Lee et al. 2002
rrs_443 = RRS_443/(0.52 + 1.7*RRS_443)
rrs_555 = RRS_555/(0.52 + 1.7*RRS_555)

g_0 = 0.0895
g_1 = 0.1247
#from Lin and Lee, 2018
bbw_555 = 0.001
u_555 = (-g_0 + np.sqrt(g_0**2 + 4*g_1*rrs_555))/(2*g_1)
rho = np.log(rrs_443/rrs_555)
a_440_i = np.exp(-2.0 - 1.4*rho + 0.2*(rho**2))
a_555 = 0.0596 + 0.2*(a_440_i - 0.01)
bb_555 = ((u_555*a_555)/(1-u_555))
bbp_555_QAA = ((u_555*a_555)/(1-u_555)) - bbw_555
bbp_555_MOREL = 0.3*(chl_ocx**0.62)*(0.002 + 0.02*(0.5-0.25*np.log10(chl_ocx)))

bbp_555_ratio = bbp_555_QAA/bbp_555_MOREL

red_tide = np.zeros_like(u_555)
#red_tide_inds = np.where(chl_ocx>1.5 and nflh>0.01 and bbp_555_ratio<1)[0]
red_tide_inds = np.where((chl_ocx>1.5) & (nflh>0.01) & (bbp_555_ratio<1))
mask_inds = np.isnan(chl_ocx)
red_tide[mask_inds] = -1
red_tide[red_tide_inds[0], red_tide_inds[1]] = 1

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

plt.figure()
plt.imshow(nflh[orig_indexSE[0]:orig_indexNW[0], orig_indexSE[1]:orig_indexNW[1]])
plt.gca().invert_xaxis()
plt.gca().invert_yaxis()
plt.title(collectionDate + ' Normalized Fluorescence Line Height')
plt.colorbar()

plt.figure()
plt.imshow(bbp_555_ratio[orig_indexSE[0]:orig_indexNW[0], orig_indexSE[1]:orig_indexNW[1]])
plt.gca().invert_xaxis()
plt.gca().invert_yaxis()
plt.title(collectionDate + ' Particle Backscatter Ratio')
plt.clim(-1, 1)
plt.colorbar()

plt.figure()
plt.imshow(bbp_555_QAA[orig_indexSE[0]:orig_indexNW[0], orig_indexSE[1]:orig_indexNW[1]])
plt.gca().invert_xaxis()
plt.gca().invert_yaxis()
plt.title(collectionDate + ' Particle Backscatter at 555 nm from QAA')
plt.clim(-0.05, 0.05)
plt.colorbar()

plt.figure()
plt.imshow(bbp_555_MOREL[orig_indexSE[0]:orig_indexNW[0], orig_indexSE[1]:orig_indexNW[1]])
plt.gca().invert_xaxis()
plt.gca().invert_yaxis()
plt.title(collectionDate + ' Particle Backscatter at 555 nm from MOREL')
plt.colorbar()

plt.figure()
plt.imshow(bb_555[orig_indexSE[0]:orig_indexNW[0], orig_indexSE[1]:orig_indexNW[1]])
plt.gca().invert_xaxis()
plt.gca().invert_yaxis()
plt.title(collectionDate + ' Total Backscatter at 555 nm')
plt.clim(0, 0.2)
plt.colorbar()

plt.figure()
plt.imshow(red_tide[orig_indexSE[0]:orig_indexNW[0], orig_indexSE[1]:orig_indexNW[1]])
plt.gca().invert_xaxis()
plt.gca().invert_yaxis()
plt.title(collectionDate + ' Red Tide')
plt.colorbar()

plt.show()