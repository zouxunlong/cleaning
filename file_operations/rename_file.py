import os
import time


start_time = time.time()


def rename_file(filepath):
    os.rename(filepath, filepath+'.en-ta')


rootdir = '/home/xuanlong/dataclean/data/MCI/en-ta/batch9/WOG_completed'
for root, dirs, files in os.walk(rootdir):
    for file in files:
        if file.endswith('.en-ta'):
            continue
        rename_file(os.path.join(root, file))

print("--- %s seconds ---" % (time.time() - start_time))
