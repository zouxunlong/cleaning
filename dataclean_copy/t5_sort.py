import time


def sort(file_in,file_out):
    start_time = time.time()
    with open(file_in) as fIN:
        list = fIN.readlines()
        list.sort(reverse=True)
    with open(file_out, 'w', encoding='utf8') as fOUT:
        for sentence in list:
            fOUT.write(sentence)
    list.clear()
    print("finished " + file_in)
    print("--- %s seconds ---" % (time.time() - start_time))


if __name__ == '__main__':

    sort('/home/xuanlong/dataclean/data.t4.en-id','/home/xuanlong/dataclean/data.t5.en-id')
