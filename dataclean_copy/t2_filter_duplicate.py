import os
import time
import plac
from pathlib import Path


@plac.opt('file_in', "Src Input File", type=Path)
@plac.opt('file_out', "Src Output File", type=Path)
def filter_duplicate(file_in, file_out):

    start_time = time.time()

    with open(file_in, 'r', encoding='utf8') as f_in:
        sentences_tuple_set = set()
        for line in f_in:
            sentences = line.split('|')
            if len(sentences) != 3:
                continue
            sentences_tuple_set.add(
                (sentences[0].strip(), sentences[1].strip(), sentences[2].strip()))
    with open(file_out, 'w', encoding='utf8') as f_out:
        for (score, sentence_en, sentence_non_en) in sentences_tuple_set:
            f_out.write("{} | {} | {}\n".format(
                    score, sentence_en, sentence_non_en))
        sentences_tuple_set.clear()

    print("finished " + file_in, flush=True)
    print("--- %s seconds ---" % (time.time() - start_time))


def main():
    root_dir='/home/xuanlong/dataclean/data/VMT'
    for folder, dirs, files in os.walk(root_dir):
        files.sort()
        for file in files:
            filter_duplicate(os.path.join(folder, file),
                        os.path.join(folder, file+'.select'))


if __name__ == '__main__':
    main()
