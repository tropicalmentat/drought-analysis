__author__ = 'G Torres'

# pseudocode
# clip all ndvi rasters to philippine extent
# compute average ndvi values of time period
# compute anomalies for october 2015 to march 2016

import gdal
from gdalconst import *


def clip(indir, outdir, clpr):
    import glob
    import os
    from subprocess import call

    tif_list = glob.glob(indir+'\*.TIFF')

    for f in tif_list:
        (path_name, raster_name) = os.path.split(f)
        print 'clipping ' + raster_name
        out_raster = outdir + 'clip_' + raster_name
        warp = 'gdalwarp -dstnodata 0 -q -cutline %s -crop_to_cutline of GTiff %s %s' % (clpr, f, out_raster)

        call(warp)


def compute_anomaly():

    gdal.AllRegister()

    self.raster = gdal.Open(f, GA_ReadOnly)
    self.cols = self.raster.RasterXSize
    self.rows = self.raster.RasterYSize
    self.projection = self.raster.GetProjection()
    self.geotrans = self.raster.GetGeoTransform()
    self.band = self.raster.GetRasterBand(1)

def main():
    in_folder = "C:\Users\G Torres\Desktop\\ndvi_test"
    out_folder = "C:\Users\G Torres\Desktop\\ndvi_clip\\"
    clip_shp = "C:\Users\G Torres\Desktop\\ndvi\\phil_extent.shp"

    clip(in_folder, out_folder, clip_shp)

if __name__ == "__main__":
    main()