import os
import time


def sort(file_path):
    start_time = time.time()
    with open(file_path) as fIN:
        list = []
        for line in fIN:
            if float(line[:6]) < 1:
                list.append(line)
        list.sort(reverse=True)
    with open(file_path, 'w', encoding='utf8') as fOUT:
        for sentence in list:
            fOUT.write(sentence)
    list.clear()
    print("finished " + file_path)
    print("--- %s seconds ---" % (time.time() - start_time))


if __name__ == '__main__':

    rootdir = '/home/xuanlong/dataclean/data/indo/parallel/wikimedia'

    for root, dirs, files in os.walk(rootdir):
        for file in files:
            if os.path.splitext(file)[1] in {'.en-ta', '.en-zh', '.en-vi', '.en-ms', '.en-id'}:
                file_path = os.path.join(root, file)
                sort(file_path)
