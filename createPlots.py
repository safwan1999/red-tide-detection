from utils import *
from os import walk
from findBoundBoxCoords import *

chlor_file_path = 'modis-data'

_, _, filenames = next(walk(chlor_file_path))

# Lat + long of bounding box of the study area (NW corner and SE corner)
latNW = 27.117033
longNW = -82.513229
latSE = 26.358022
longSE = -81.693427

chlor_a_output = 'chlora_plots'
chlor_ocx_output = 'chlocx_plots'

ensure_folder(chlor_a_output)
ensure_folder(chlor_ocx_output)

plotcounter = 1
print('Creating plots...')
for filename in filenames:
	file_path = chlor_file_path + '/' + filename
	collectionDate, orig_indexSE, orig_indexNW = findBoundBoxCoords(file_path, latNW, longNW, latSE, longSE)

	dataset = xr.open_dataset(file_path, 'geophysical_data')

	chlor_a = dataset['chlor_a']
	chl_ocx = dataset['chl_ocx']

	plt.figure(dpi=500)
	plt.imshow(chlor_a[orig_indexSE[0]:orig_indexNW[0], orig_indexSE[1]:orig_indexNW[1]], vmin=0.001, vmax=25)
	plt.gca().invert_xaxis()
	plt.gca().invert_yaxis()
	plt.title(collectionDate + ' Chlorophyll Concentration, OCI Algorithm')
	plt.colorbar()
	plt.savefig(chlor_a_output + '/' + collectionDate + '_chlora.png', bbox_inches='tight')

	plt.figure(dpi=500)
	plt.imshow(chl_ocx[orig_indexSE[0]:orig_indexNW[0], orig_indexSE[1]:orig_indexNW[1]], vmin=0.001, vmax=25)
	plt.gca().invert_xaxis()
	plt.gca().invert_yaxis()
	plt.title(collectionDate + ' Chlorophyll Concentration, OC3 Algorithm')
	plt.colorbar()
	plt.savefig(chlor_ocx_output + '/' + collectionDate + '_chlocx.png', bbox_inches='tight')

	plt.close('all')
	print('Plot ' + str(plotcounter) + ' completed')
	plotcounter = plotcounter + 1