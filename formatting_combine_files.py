import os
import time


start_time = time.time()


def combine_files(file, output_filepath):
    with open(file, encoding='utf8') as fIN, open(output_filepath, 'a', encoding='utf8') as fOUT:
        for i, sentence in enumerate(fIN):
            fOUT.write(sentence)


rootdir = '/home/zxl/ssd/WORK/data_clean/data_clean_and_extraction/Batch_14'
file_combined=0

for root, dirs, files in os.walk(rootdir):
    for file in files:
        if file.endswith('.en-ta'):
            combine_files(os.path.join(root, file), rootdir+'.en-ta')
            file_combined+=1
        if file.endswith('.en-ms'):
            combine_files(os.path.join(root, file), rootdir+'.en-ms')
            file_combined+=1
        if file.endswith('.en-zh'):
            combine_files(os.path.join(root, file), rootdir+'.en-zh')
            file_combined+=1


print("--- %s seconds ---" % (time.time() - start_time))
print("Done. {} file combined".format(file_combined))
