__author__ = 'G Torres'

import gdal
from gdalconst import *
import numpy
import csv
import sys
import glob
import os
import matplotlib

# pseudocode
# read csv file of place names and coordinates
# store in dict
# open and iterate thru LST anomalies
# iterate through each item in dict and convert coordinates to pixel coordinates
# collect pixel values and store in dict
# save pixel values with place names and coordinates in csv


def new_csv():
    pass

def map_to_pix():
    pass

def collect_pixels(fn, r_dir):

    loc_list = {}
    # open csv and collect place name and coordinates
    with open(fn, 'rb') as f:
        reader = csv.reader(f)
        try:
            count = 0
            for row in reader:
                if count == 0:  # ignore the first line
                    count += 1
                else:
                    print row
                    loc_list[row[0]] = [(float(row[1]),  # convert coordinates to float
                                         float(row[2]))]
                    count += 1
        except csv.Error as e:
            sys.exit('file %s, line %d: %s' %
                     (fn, reader.line_num, e))

    # open and iterate through LST anomalies
    raster_list = glob.glob(r_dir+'\*.TIFF')
    for r in raster_list:
        path, basename = os.path.split(r)
        if '2015' in basename or '2016' in basename:  # ignore files not included in time period
            print basename
            anom_raster = gdal.Open(r, GA_ReadOnly)
            anom_band = anom_raster.GetRasterBand(1)
            anom_gt, anom_proj = anom_raster.GetGeoTransform(), anom_raster.GetProjection()
            anom_cols, anom_rows = anom_raster.RasterXSize, anom_raster.RasterYSize
            anom_ds = anom_band.ReadAsArray(0, 0, anom_cols, anom_rows)

            topleft_x = anom_gt[0]
            topleft_y = anom_gt[3]
            pix_width = anom_gt[1]
            pix_height = anom_gt[5]*-1

            for location in loc_list:
                pix_x = (loc_list[location][0][0] - topleft_x)/pix_width
                pix_y = (loc_list[location][0][1] - topleft_y)/pix_height
                print location, pix_x, pix_y, anom_ds[pix_y, pix_x]
        else:
            pass

    return


def main():
    loc_csv = "D:\LUIGI\EMERGENCY OBSERVATION\\2016_ELNINYO_DROUGHT\LAND SURFACE TEMP\stations.csv"
    anom_dir = "D:\LUIGI\EMERGENCY OBSERVATION\\2016_ELNINYO_DROUGHT\LAND SURFACE TEMP\\float_tiff\day"

    print collect_pixels(loc_csv, anom_dir)

if __name__=="__main__":
    main()