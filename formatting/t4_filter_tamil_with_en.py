import os
import re
import time


def filter(file_path):
    with open(file_path, encoding='utf8') as f_in, open(file_path + '.filtered', 'w', encoding='utf8') as f_out:
        for line in f_in:
            sents=line.split('|')
            en_sent = sents[1].strip()
            ms_sent = sents[2].strip()
            if re.match('[0-9]', ms_sent) or re.match('[0-9]', en_sent):
                continue
            f_out.write(line)
    print("finished " + file_path, flush=True)


def main(rootdir):
    for root, dirs, files in os.walk(rootdir):
        for file in files:
            if os.path.splitext(file)[1] in {'.en-ms'}:
                file_path = os.path.join(root, file)
                filter(file_path)


if __name__ == '__main__':
    start_time = time.time()
    rootdir = '/home/xuanlong/dataclean/data/parallel_combined'
    main(rootdir)
    print("--- %s seconds ---" % (time.time() - start_time), flush=True)
