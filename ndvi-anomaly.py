__author__ = 'G Torres'

# pseudocode
# clip all ndvi rasters to philippine extent
# compute average ndvi values of time period
# compute anomalies for october 2015 to march 2016

import gdal
from gdalconst import *
import numpy as np
import numpy.ma as ma
import glob
import os
from subprocess import call

gdal.AllRegister()


def clip_raster(indir, shp):
    raster_list = glob.glob(indir + '\*.TIFF')
    shp_clip = shp

    for ds in raster_list:
        path, fn = os.path.split(ds)
        clipped = 'clip_' + fn
        clip_cmd = ['gdalwarp', '-srcnodata', '-99', '-cutline', shp_clip,
                    '-crop_to_cutline', ds, clipped]
        call(clip_cmd)

    return

        # return raster_list


def compute_average(indir):
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

    mask = np.greater(array_stack, 100)  # build mask for no-data values

    mask_ndvi = ma.array(array_stack, mask=mask)  # apply mask

    ndvi_average = np.mean(mask_ndvi, axis=2)  # compute climatological average

    # create new raster dataset to write average ndvi
    out_raster = driver.Create('phil_ndvi_average.TIFF', cols, rows, 1, GDT_Float32)
    out_band = out_raster.GetRasterBand(1)
    out_band.WriteArray(ndvi_average, 0, 0)
    out_band.SetNoDataValue(-99)
    out_raster.SetGeoTransform(geotrans)
    out_raster.SetProjection(projection)
    out_band.FlushCache()

    return ndvi_average


def compute_anomaly(avg, vari):
    # open climatological average data-set
    average = gdal.Open(avg, GA_ReadOnly)

    avg_driver = average.GetDriver()
    avg_cols = average.RasterXSize
    avg_rows = average.RasterYSize
    avg_proj = average.GetProjection()
    avg_gt = average.GetGeoTransform()
    avg_band = average.GetRasterBand(1)

    # open variable data-sets
    avg_ds = avg_band.ReadAsArray(0, 0, avg_cols, avg_rows)

    var_list = glob.glob(vari+'\*.TIFF')


    # compute anomaly for each data-set
    for ds in var_list:
        path, fn = os.path.split(ds)
        variable = gdal.Open(ds, GA_ReadOnly)
        var_cols = variable.RasterXSize
        var_rows = variable.RasterYSize
        #band_total = variable.RasterCount
        var_band = variable.GetRasterBand(1
                                          )
        var_ds = var_band.ReadAsArray(0, 0, var_cols, var_rows)

        mask = np.greater(var_ds, 10)

        anom_mask = ma.array(var_ds, mask=mask)

        anom_ds = anom_mask - avg_ds

        print anom_ds
        # create new data-set for each computation
        anom_fn = 'anom_' + fn
        out_raster = avg_driver.Create(anom_fn, var_cols, var_rows, 1, GDT_Float32)
        out_band = out_raster.GetRasterBand(1)
        out_band.WriteArray(anom_ds, 0, 0)
        #out_band.SetNoDataValue(99999)
        out_raster.SetGeoTransform(avg_gt)
        out_raster.SetProjection(avg_proj)
        out_band.FlushCache()

    return

def main():
    in_folder = "D:\LUIGI\EMERGENCY OBSERVATION\\2016_ELNINYO_DROUGHT\NDVI\clip_ndvi.TIF"

    avg_dataset = "D:\LUIGI\EMERGENCY OBSERVATION\\2016_ELNINYO_DROUGHT\NDVI\phil_ndvi_average.TIFF"

    anomalous_ds = "D:\LUIGI\EMERGENCY OBSERVATION\\2016_ELNINYO_DROUGHT\NDVI\\ndvi clipped"

    clip_shp = "D:\LUIGI\EMERGENCY OBSERVATION\\2016_ELNINYO_DROUGHT\NDVI\\phil_extent.shp"

    ndvi_anom = "D:\LUIGI\EMERGENCY OBSERVATION\\2016_ELNINYO_DROUGHT\NDVI\\ndvi-2015-2016"

    # print compute_average(in_folder)

    print compute_anomaly(avg_dataset, anomalous_ds)

    #print clip_raster(ndvi_anom, clip_shp)


if __name__ == "__main__":
    main()
