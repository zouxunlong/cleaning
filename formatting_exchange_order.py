import os
import time


start_time = time.time()


def exhange_order(filepath):
    with open(filepath, encoding='utf8') as fIN, open('/home/xuanlong/dataclean/data_clean_and_extraction/en_to_zh/en_to_zh.txt', 'a', encoding='utf8') as fOUT:
        for i, sentence in enumerate(fIN):
            sentences=sentence.split('|')
            fOUT.write("{} | {}\n".format(sentences[1].strip(), sentences[0].strip()))
            print(i)


exhange_order('/home/xuanlong/dataclean/data_clean_and_extraction/zh_to_en/zh_to_en.txt')

print("--- %s seconds ---" % (time.time() - start_time))