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
    ndvi_vrt = "D:\LUIGI\EMERGENCY OBSERVATION\\2016_ELNINYO_DROUGHT\NDVI\\ndvi.vrt"

    vrt_make = 'gdalbuildvrt -separate -input_file_list %s %s' % (txt_list, ndvi_vrt)

    os.system(vrt_make)
    
def main():
    input_dir = "D:\LUIGI\EMERGENCY OBSERVATION\\2016_ELNINYO_DROUGHT\NDVI\\ndvi"
    workspace = "D:\LUIGI\EMERGENCY OBSERVATION\\2016_ELNINYO_DROUGHT\NDVI"
    os.chdir(workspace)
    build_vrt(input_dir)

    """
    with open('tif_list.txt', 'rb') as f:
        lines = f.read()
        print lines
    """

if __name__ == "__main__":
    main()
