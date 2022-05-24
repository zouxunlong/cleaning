import os
import time


def sort(file_path):
    start_time = time.time()
    with open(file_path) as fIN:
        list = []
        for line in fIN:
            list.append(line)
        list.sort(reverse=True)
    with open(file_path, 'w', encoding='utf8') as fOUT:
        for sentence in list:
            fOUT.write(sentence)
    list.clear()
    print("finished " + file_path)
    print("--- %s seconds ---" % (time.time() - start_time))


if __name__ == '__main__':

    rootdir = '/home/xuanlong/dataclean/data/parallel_combined'

    for root, dirs, files in os.walk(rootdir):
        for file in files:
            if os.path.splitext(file)[1] in {'.en-ms','.en-ta'}:
                file_path = os.path.join(root, file)
                sort(file_path)
