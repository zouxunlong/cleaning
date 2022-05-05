import zipfile
import os


dir = '/home/xuanlong/dataclean/data'

for rootdir, dirs, files in os.walk(dir):

    for  file in files:
        if os.path.splitext(file)[1]=='.zip':
            zip_file= os.path.join(rootdir, file)
            with zipfile.ZipFile(zip_file, 'r') as zip_fin:
                zip_fin.extractall(rootdir)