import os
import time


start_time = time.time()


def combine_files(file):
    with open(file, encoding='utf8') as fIN, open('/home/xuanlong/dataclean/data_clean_and_extraction/zh_to_en/new_file.txt', 'a', encoding='utf8') as fOUT:
        for i, sentence in enumerate(fIN):
            fOUT.write(sentence)
            print(i)

rootdir = '/home/xuanlong/dataclean/data_clean_and_extraction/zh_to_en'

for subdir, dirs, files in os.walk(rootdir):
    for file in files:
        combine_files(os.path.join(subdir, file))


print("--- %s seconds ---" % (time.time() - start_time))