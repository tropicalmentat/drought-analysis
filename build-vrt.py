import glob
import os
from subprocess import call


def build_vrt(indir):
    tif_list = glob.glob(indir+'\*.TIFF')
    print tif_list

    with open('tif_list.txt', 'wb') as f:
        for tif in tif_list:
            f.writelines(tif+'\n')
            print tif

    txt_list = "D:\LUIGI\EMERGENCY OBSERVATION\\2016_ELNINYO_DROUGHT\NDVI\\tif_list.txt"
    ndvi_anom = "ndvi_anom.vrt"

    vrt_make = ["gdalbuildvrt", "-separate", "-input_file_list", txt_list, ndvi_anom]

    call(vrt_make)


def main():
    #input_dir = "D:\LUIGI\EMERGENCY OBSERVATION\\2016_ELNINYO_DROUGHT\NDVI\\ndvi"
    workspace = "D:\LUIGI\EMERGENCY OBSERVATION\\2016_ELNINYO_DROUGHT\NDVI"
    anom_ds = "D:\LUIGI\EMERGENCY OBSERVATION\\2016_ELNINYO_DROUGHT\NDVI\\ndvi-2015-2016"
    os.chdir(workspace)
    build_vrt(anom_ds)

    """
    with open('tif_list.txt', 'rb') as f:
        lines = f.read()
        print lines
    """

if __name__ == "__main__":
    main()
