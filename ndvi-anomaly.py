__author__ = 'G Torres'

# pseudocode
# clip all ndvi rasters to philippine extent
# compute average ndvi values of time period
# compute anomalies for october 2015 to march 2016

import gdal
from gdalconst import *
import numpy as np
import numpy.ma as ma

def compute_average(indir):

    gdal.AllRegister()

    raster = gdal.Open(indir, GA_ReadOnly)
    driver = raster.GetDriver()
    cols = raster.RasterXSize
    rows = raster.RasterYSize
    projection = raster.GetProjection()
    geotrans = raster.GetGeoTransform()
    band_total = raster.RasterCount

    # iterate each band and build a list of arrays
    array_list = []
    for i in range(1, band_total):
        band = raster.GetRasterBand(1)
        array_list.append(band.ReadAsArray(0, 0, cols, rows))

    array_stack = np.dstack(array_list)  # build stack of arrays

    mask = np.greater(array_stack, 100)

    mask_ndvi = ma.array(array_stack, mask=mask)

    ndvi_average = np.mean(mask_ndvi, axis=2)  # compute climatological average

    # create new raster dataset to write average

    out_raster = driver.Create('phil_ndvi_average.TIFF', cols, rows, 1, GDT_Float32)
    out_band = out_raster.GetRasterBand(1)
    out_band.WriteArray(ndvi_average,0 ,0)
    out_band.SetNoDataValue(-99)
    out_raster.SetGeoTransform(geotrans)
    out_raster.SetProjection(projection)
    out_band.FlushCache()

    return ndvi_average



def main():

    in_folder = "D:\LUIGI\EMERGENCY OBSERVATION\\2016_ELNINYO_DROUGHT\NDVI\clip_ndvi.TIFF"

    print compute_average(in_folder)

if __name__ == "__main__":
    main()