import os
from bi_text_miner import Bi_text_miner
os.environ["TOKENIZERS_PARALLELISM"] = "false"

bi_text_miner = Bi_text_miner(knn_neighbors=6, min_matching_score=1.06, min_cos_sim=0.7,
                              model_path_or_name='../model/labse_bert_model', sort_by_cos=False)


def allocate_text_by_lang(file_en, file_id):

    texts_en = [line.strip() for line in open(file_en).readlines()]
    texts_id = [line.strip() for line in open(file_id).readlines()]

    return {'en': texts_en, 'id': texts_id}


text_list_dict = allocate_text_by_lang(
    '/home/xuanlong/dataclean/data/first50k_split.en', '/home/xuanlong/dataclean/data/first50k_split.id')
text_set_dict = bi_text_miner.list_to_set(text_list_dict)
en_zh_sentence_pair = bi_text_miner.sentence_matching(
    text_set_dict['en'], text_set_dict['id'])


with open('/home/xuanlong/dataclean/data/first50k_split.aligned.en', 'w', encoding='utf8') as f_out_en, \
        open('/home/xuanlong/dataclean/data/first50k_split.aligned.id', 'w', encoding='utf8') as f_out_id:
    for sentence_pair in en_zh_sentence_pair:
        f_out_en.write(sentence_pair[0])
        f_out_id.write(sentence_pair[1])

