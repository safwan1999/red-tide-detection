from os import walk
from getChl import *

chlor_file_path = 'modis-chlor'

_, _, filenames = next(walk(chlor_file_path))

# Lat + long of bounding box of the study area (NW corner and SE corner)
latNW = 27.117033
longNW = -82.513229
latSE = 26.358022
longSE = -81.693427

plotcounter = 1
print('Creating plots...')
for filename in filenames:
	file_path = chlor_file_path + '/' + filename
	collectionDate, chlor_a, chl_ocx = getChl(file_path, latNW, longNW, latSE, longSE)

	plt.figure(dpi=500)
	plt.imshow(chlor_a, vmin=0.001, vmax=25)
	plt.gca().invert_xaxis()
	plt.gca().invert_yaxis()
	plt.title(collectionDate + ' Chlorophyll Concentration, OCI Algorithm')
	plt.colorbar()
	plt.savefig('chlora_plots/' + collectionDate + '_chlora.png')

	plt.figure(dpi=500)
	plt.imshow(chl_ocx, vmin=0.001, vmax=25)
	plt.gca().invert_xaxis()
	plt.gca().invert_yaxis()
	plt.title(collectionDate + ' Chlorophyll Concentration, OC3 Algorithm')
	plt.colorbar()
	plt.savefig('chlocx_plots/' + collectionDate + '_chlocx.png')

	plt.close('all')
	print('Plot ' + str(plotcounter) + ' completed')
	plotcounter = plotcounter + 1