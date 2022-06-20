import time


start_time = time.time()


def exhange_order(filepath):
    with open(filepath, encoding='utf8') as fIN, open('/home/xuanlong/dataclean/data/MCI.en-ta', 'a', encoding='utf8') as fOUT:
        for i, line in enumerate(fIN):
            sentences=line.split('|||')
            if len(sentences) != 2:
                continue
            fOUT.write("{} | {}\n".format(sentences[1].strip(), sentences[0].strip()))
            print(i)


rootdir = '/home/xuanlong/dataclean/data/MCI.ta-en'
exhange_order(rootdir)

print("--- %s seconds ---" % (time.time() - start_time))