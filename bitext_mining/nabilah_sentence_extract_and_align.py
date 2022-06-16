import os
import json
import plac
from pathlib import Path
from sentsplit.segment import SentSplit
import html
import pandas as pd
from bi_text_miner import Bi_text_miner

os.environ["TOKENIZERS_PARALLELISM"] = "false"

bi_text_miner = Bi_text_miner(knn_neighbors=4, min_matching_score=0.99, min_cos_sim=0.7,
                              model_path_or_name='../model/labse_bert_model', sort_by_cos=False)


def extract_sentences(paragraph, lang):
    sent_splitter = SentSplit(lang, strip_spaces=True)
    sentences = sent_splitter.segment(paragraph)
    return sentences


def main():

    os.chdir(os.path.dirname(__file__))

    with open('/home/zxl/ssd/WORK/data_clean/data/train.clean.sorted.rev.en', 'r', encoding='utf8') as f_in_en, \
            open('/home/zxl/ssd/WORK/data_clean/data/train.clean.sorted.rev.id', 'r', encoding='utf8') as f_in_id, \
            open('/home/zxl/ssd/WORK/data_clean/data/first50k_split.aligned.en', 'a', encoding='utf8') as f_out_en, \
            open('/home/zxl/ssd/WORK/data_clean/data/first50k_split.aligned.id', 'a', encoding='utf8') as f_out_id:

        for (i, sentence_src), (j, sentence_tgt) in zip(enumerate(f_in_en), enumerate(f_in_id)):
            sentence_src = sentence_src.strip()
            sentence_tgt = sentence_tgt.strip()
            sentences_src = extract_sentences(sentence_src, 'en')
            sentences_tgt = extract_sentences(sentence_tgt, 'en')

            text_list_dict = {'en': sentences_src, 'id': sentences_tgt}

            text_set_dict = bi_text_miner.list_to_set(text_list_dict)
            en_zh_sentence_pair = bi_text_miner.sentence_matching(
                text_set_dict['en'], text_set_dict['id'])

            for sentence_pair in en_zh_sentence_pair:
                f_out_en.write(sentence_pair[0]+'\n')
                f_out_id.write(sentence_pair[1]+'\n')
            
            if i==50000:
                break


if __name__ == "__main__":
    plac.call(main)
