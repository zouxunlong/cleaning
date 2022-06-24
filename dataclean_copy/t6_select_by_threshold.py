import os
import time


def select(file_in, file_out):
    start_time = time.time()

    with open(file_in, 'r', encoding='utf8') as f_in, \
            open(file_out, 'w', encoding='utf8') as f_out:
        for line in f_in:
            sentences = line.split('|')
            if len(sentences) != 3:
                continue
            if float(sentences[0]) > 0.8191:
                f_out.write(line)
            else:
                break

    print("finished " + file_in, flush=True)
    print("--- %s seconds ---" % (time.time() - start_time), flush=True)


def main():
    root_dir = '/home/xuanlong/dataclean/data/VMT'
    for folder, dirs, files in os.walk(root_dir):
        files.sort()
        for file in files:
            select(os.path.join(folder, file),
                   os.path.join(folder, file+'.select'))


if __name__ == '__main__':
    main()
