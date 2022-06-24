import os
import time


def sort(file_in, file_out):
    start_time = time.time()
    with open(file_in) as fIN:
        list = fIN.readlines()
        list.sort(reverse=True)
    with open(file_out, 'w', encoding='utf8') as fOUT:
        for line in list:
            fOUT.write(line)
    list.clear()
    print("finished " + file_in)
    print("--- {} seconds ---".format(time.time() - start_time))


def main():
    root_dir = '/home/xuanlong/dataclean/data/VMT'
    for folder, dirs, files in os.walk(root_dir):
        files.sort()
        for file in files:
            sort(os.path.join(folder, file),
                 os.path.join(folder, file))


if __name__ == '__main__':
    main()
