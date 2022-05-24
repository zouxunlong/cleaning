import os
import re
import time


def chaotic_detected(text_for_chaotic_detect):
    alphabetic_text = ''.join(
        re.sub('[^a-zA-Z]', '', text_for_chaotic_detect).split())
    if len(alphabetic_text)/len(text_for_chaotic_detect) < 0.7:
        return True
    return False


def filter(file_path):
    with open(file_path, encoding='utf8') as f_in, open(file_path + '.filtered3', 'w', encoding='utf8') as f_out:
        for line in f_in:
            en_sent = line.split('|')[1].strip()
            if not chaotic_detected(en_sent):
                f_out.write(line)
    print("finished " + file_path, flush=True)


def main(rootdir):
    for root, dirs, files in os.walk(rootdir):
        for file in files:
            if os.path.splitext(file)[1] in {'.filtered2'}:
                file_path = os.path.join(root, file)
                filter(file_path)


if __name__ == '__main__':
    start_time = time.time()
    rootdir = '/home/xuanlong/dataclean/data/parallel/en-ms'
    main(rootdir)
    print("--- %s seconds ---" % (time.time() - start_time), flush=True)
