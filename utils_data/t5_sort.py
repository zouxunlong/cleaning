import time


def sort(file_path):
    start_time = time.time()
    with open(file_path) as fIN:
        list = fIN.readlines()
        list.sort(reverse=True)
    with open(file_path, 'w', encoding='utf8') as fOUT:
        for sentence in list:
            fOUT.write(sentence)
    list.clear()
    print("finished " + file_path)
    print("--- %s seconds ---" % (time.time() - start_time))


if __name__ == '__main__':

    sort('/home/xuanlong/dataclean/data.t4.en-id')
