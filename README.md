# Red Tide Detection

Implements the red tide detection algorithm outlined in the IOCCG report #20 (2021).

The code uses MODIS data (.nc files), available from: https://oceancolor.gsfc.nasa.gov/cgi/browse.pl?sen=amod

The code assumes a folder named 'modis-data' is in the parent directory which contains all of the MODIS files to be used.

### Functions:

redTideDetector.py: Runs the red tide detection algorithm on all MODIS data available and saves output plots in a new folder named 'red_tide_plots'. In these plots, -1 indicates masked pixels (ground or cloud), 0 indicates water without detected red tide, and 1 indicates water with detected red tide.

createPlots.py: Creates plots of estimated chlorphyll-a levels in all available MODIS data. Saves resulting plots in folders named 'chlora_plots' and 'chlocx_plots'. Can be easily modifed to plot other extracted features.

findBoundBoxCoords.py: Utility function for extracting a bounding box from MODIS lat/long data.

utils.py: Other utility functions.