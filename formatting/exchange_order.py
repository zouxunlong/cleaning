import time


start_time = time.time()


def exhange_order(filepath):
    with open(filepath, encoding='utf8') as fIN, open('/home/xuanlong/dataclean/data/MCI2.en-ta', 'w', encoding='utf8') as fOUT:
        for i, line in enumerate(fIN):
            sentences=line.split('|||')
            fOUT.write("{} | {}\n".format(sentences[1].strip(), sentences[0].strip()))
            print(i)


rootdir = '/home/xuanlong/dataclean/data/MCI2.ta-en'
exhange_order(rootdir)

print("--- %s seconds ---" % (time.time() - start_time))