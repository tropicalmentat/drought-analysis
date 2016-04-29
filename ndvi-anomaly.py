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


def build_vrt(indir, outdir):
    tif_list = glob.glob(indir+'\*.TIFF')
    with open(outdir+'\\tif_list.txt', 'wb') as f:
        for fn in tif_list:
            path, name = os.path.split(fn)
            if '2000' in name:
                pass
            elif '2011' in name:
                pass
            elif '2012' in name:
                pass
            elif '2013' in name:
                pass
            elif '2014' in name:
                pass
            elif '2015' in name:
                pass
            elif '2016' in name:
                pass
            else:
                print fn
                f.writelines(fn+'\n')


    list_dir = glob.glob(outdir+'\*.txt')
    print '\nfound %s in %s' % (list_dir[0], outdir)
    print '\nbuilding vrt...'
    ndvi_anom = outdir+"\\ndvi_2001-2010.vrt"

    vrt_make = ["gdalbuildvrt", "-separate", "-input_file_list", list_dir[0], ndvi_anom]

    call(vrt_make)
    return


def clip_raster(fn, shp, outdir):

    path, name = os.path.split(fn)
    print '\nclipping ' + name + ' to ' + outdir
    clipped = outdir+'\clip_' + name.split('.')[0] + '.TIFF'
    clip_cmd = ['gdalwarp', '-srcnodata', '-99', '-cutline', shp,
                '-crop_to_cutline', fn, clipped]
    call(clip_cmd)

    return


def compute_mean(fn, wrkspc):
    """Computes the mean of a data-set time-stack.
    Returns .TIFF of mean array"""
    raster = gdal.Open(fn, GA_ReadOnly)
    driver = raster.GetDriver()
    cols = raster.RasterXSize
    rows = raster.RasterYSize
    projection = raster.GetProjection()
    geotrans = raster.GetGeoTransform()
    band_total = raster.RasterCount

    # iterate each band and build a list of arrays
    array_list = []
    print '\nbuilding array stack...'
    for i in range(1, band_total):
        band = raster.GetRasterBand(1)
        array_list.append(band.ReadAsArray(0, 0, cols, rows))

    array_stack = np.dstack(array_list)  # build stack of arrays

    print '\ncomputing mean...'
    mask = np.greater(array_stack, 100)  # build mask for no-data values

    mask_ndvi = ma.array(array_stack, mask=mask)  # apply mask

    ndvi_average = np.mean(mask_ndvi, axis=2)  # compute climatological average

    # create new raster dataset to write average ndvi
    print '\nwriting output to .TIFF...'
    out_raster = driver.Create(wrkspc+'\\phil_ndvi_mean.TIFF', cols, rows, 1, GDT_Float32)
    out_band = out_raster.GetRasterBand(1)
    out_band.WriteArray(ndvi_average, 0, 0)
    #out_band.SetNoDataValue(-99)
    out_raster.SetGeoTransform(geotrans)
    out_raster.SetProjection(projection)
    out_band.FlushCache()

    return


def compute_anomaly(avg, vari, outdir):
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

        # create new data-set for each computation
        anom_fn = outdir + '\\2anom_' + fn
        print '\nsaving to %s' % anom_fn
        out_raster = avg_driver.Create(anom_fn, var_cols, var_rows, 1, GDT_Float32)
        out_band = out_raster.GetRasterBand(1)
        out_band.WriteArray(anom_ds, 0, 0)
        #out_band.SetNoDataValue(99999)
        out_raster.SetGeoTransform(avg_gt)
        out_raster.SetProjection(avg_proj)
        out_band.FlushCache()

    return

def main():

    work_space = "D:\LUIGI\EMERGENCY OBSERVATION\\2016_ELNINYO_DROUGHT\NDVI"
    in_folder = "D:\LUIGI\EMERGENCY OBSERVATION\\2016_ELNINYO_DROUGHT\NDVI\\ndvi"
    clip_shp = "D:\LUIGI\EMERGENCY OBSERVATION\\2016_ELNINYO_DROUGHT\NDVI\\phil_extent.shp"
    ndvi_clip = "D:\LUIGI\EMERGENCY OBSERVATION\\2016_ELNINYO_DROUGHT\NDVI\\ndvi clipped"
    ndvi_anom = "D:\LUIGI\EMERGENCY OBSERVATION\\2016_ELNINYO_DROUGHT\NDVI\\ndvi anomalies"

    """
    print build_vrt(in_folder, work_space)

    vrt = glob.glob(work_space+'\*.vrt')[0]
    print clip_raster(vrt, clip_shp, work_space)

    clipped = glob.glob(work_space+'\*.TIFF')

    for f in clipped:
        if 'clip' in f:
            print compute_mean(f, work_space)

    clip_anom = glob.glob(in_folder+'\*TIFF')
    for anom_ds in clip_anom:
        path, name = os.path.split(anom_ds)
        if '2015' in name or '2016' in name:
            print clip_raster(anom_ds, clip_shp, ndvi_clip)

    """
    mean_ds = glob.glob(work_space+'\*.TIFF')
    for f in mean_ds:
        if 'mean' in f:
            compute_anomaly(f, ndvi_clip, ndvi_anom)


if __name__ == "__main__":
    # pseudo code
    # build vrt of data-sets from 2000-2010
    # clip vrt to philippine extent
    # clip data-sets from 2015-2016
    # compute anomaly
    main()
