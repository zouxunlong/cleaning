import time
start_time = time.time()

with open("/home/xuanlong/dataclean/data/wikimedia/wikimedia.en-ms") as file, open("/home/xuanlong/dataclean/data/wikimedia/wikimedia_sorted.en-ms", 'w', encoding='utf8') as fOUT:
    list=[]
    for line in file:
        if float(line[:6]) < 0.997:
            list.append(line)
    list.sort(reverse=True)
    for sentence in list:
        fOUT.write(sentence)


print("--- %s seconds ---" % (time.time() - start_time))
