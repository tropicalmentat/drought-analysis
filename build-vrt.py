import glob
import os
from subprocess import call

def build_vrt(indir):
    tif_list = glob.glob(indir+'\*.TIFF')
    #print tif_list

    with open('tif_list.txt', 'wb') as f:
        for tif in tif_list:
            f.writelines(tif+'\n')
            #print tif

    txt_list = "C:\Users\G Torres\Desktop\\ndvi_test\\tif_list.txt"

    vrt_make = 'gdalbuildvrt -separate -input_file_list %s ndvi.vrt' % (txt_list)

    call(vrt_make)
    
def main():
    input_dir = "C:\Users\G Torres\Desktop\\ndvi_test"
    os.chdir(input_dir)
    build_vrt(input_dir)

    with open('tif_list.txt', 'rb') as f:
        lines = f.read()
        print lines
    
if __name__ == "__main__":
    main()
