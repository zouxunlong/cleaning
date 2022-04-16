import os
import time


start_time = time.time()


def combine_files(file):
    with open(file, encoding='utf8') as fIN, open('/home/zxl/ssd/WORK/data_clean/WORK/Batch7(CD7)_extracted_en_to_ms.txt', 'a', encoding='utf8') as fOUT:
        for i, sentence in enumerate(fIN):
            fOUT.write(sentence)
        print('finished one file')

rootdir = '/home/zxl/ssd/WORK/data_clean/WORK/Batch7(CD7)_extracted'

for subdir, dirs, files in os.walk(rootdir):
    for file in files:
        combine_files(os.path.join(subdir, file))


print("--- %s seconds ---" % (time.time() - start_time))