__author__ = 'G Torres'

# pseudocode
# clip all ndvi rasters to philippine extent
# compute average ndvi values of time period
# compute anomalies for october 2015 to march 2016

import gdal
from gdalconst import *

def compute_anomaly(indir):

    gdal.AllRegister()

    tif_list = glob.glob(indir+'\*.TIFF')

    array_stack = None

    for i in tif_list:

        raster = gdal.Open(f, GA_ReadOnly)
        cols = self.raster.RasterXSize
        rows = self.raster.RasterYSize
        projection = self.raster.GetProjection()
        geotrans = self.raster.GetGeoTransform()
        band = self.raster.GetRasterBand(1)
        data = band.ReadAsArray(0, 0, cols, rows)

        array_stack = (data)

    return


def main():
    #call(["ls", "-l"])
    in_folder = "C:\Users\G Torres\Desktop"
    out_folder = "C:\Users\G Torres\Desktop\\ndvi_clip\\"
    clip_shp = "C:\Users\G Torres\Desktop\\ndvi_test\\phil_extent.shp"

    os.chdir(in_folder)
    clip(in_folder, out_folder)

if __name__ == "__main__":
    main()