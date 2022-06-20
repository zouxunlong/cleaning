import os
import time


def main():
    start_time = time.time()
    with open('/home/xuanlong/dataclean/data/Total/train.filtered.en', 'r', encoding='utf8') as f_in_en, \
            open('/home/xuanlong/dataclean/data/Total/train.filtered.id', 'r', encoding='utf8') as f_in_id:
        sentences_tuple_set = set()
        for (i, sentence_en), (j, sentence_id) in zip(enumerate(f_in_en), enumerate(f_in_id)):
            sentences_tuple_set.add((sentence_en.strip(), sentence_id.strip()))
    with open('/home/xuanlong/dataclean/data/Total/train.filtered2.en', 'w', encoding='utf8') as f_out_en, \
            open('/home/xuanlong/dataclean/data/Total/train.filtered2.id', 'w', encoding='utf8') as f_out_id:
        for (sentence_en, sentence_id) in sentences_tuple_set:
            f_out_en.write(sentence_en+'\n')
            f_out_id.write(sentence_id+'\n')
    sentences_tuple_set.clear()
    print("finished ")
    print("--- %s seconds ---" % (time.time() - start_time))


if __name__ == '__main__':
    main()
