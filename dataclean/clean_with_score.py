import os
import re
import string
from sentence_transformers import SentenceTransformer, util
import pycld2 as cld2
import cld3
import fasttext
from googletrans import Translator


model_fasttext = fasttext.load_model('../model/lid.176.bin')
model_sentence_transformers = SentenceTransformer('../model/labse_bert_model')
translator = Translator()


def lang_detect(text_for_lang_detect):

    lang_detected = set()

    text_for_lang_detect = re.sub(
        "(?i)\w+@\S+\s?|http\S*\s?|www\.\S*\s?|[a-z\.]*\.sg\S*\s?|[0-9]+\s?", "", text_for_lang_detect)
    text_for_lang_detect = text_for_lang_detect.translate(
        str.maketrans('-', ' ', string.punctuation.replace('-', ''))).strip().lower()

    if text_for_lang_detect:
        if re.search('[\u4e00-\u9fff]', text_for_lang_detect):
            lang_detected.add('zh')
        if re.search('[\u0B80-\u0BFF]', text_for_lang_detect):
            lang_detected.add('ta')
        if re.search('[àáãạảăắằẳẵặâấầẩẫậèéẹẻẽêềếểễệđìíĩỉịòóõọỏôốồổỗộơớờởỡợùúũụủưứừửữựỳỵỷỹýÀÁÃẠẢĂẮẰẲẴẶÂẤẦẨẪẬÈÉẸẺẼÊỀẾỂỄỆĐÌÍĨỈỊÒÓÕỌỎÔỐỒỔỖỘƠỚỜỞỠỢÙÚŨỤỦƯỨỪỬỮỰỲỴỶỸÝ]', text_for_lang_detect):
            lang_detected.add('vi')

        if len(lang_detected) == 0:

            lang_by_cld2 = cld2.detect(text_for_lang_detect)[2][0][1]
            lang_by_cld3 = cld3.get_language(text_for_lang_detect)[0]
            lang_by_fasttext = model_fasttext.predict(
                text_for_lang_detect)[0][0][-2:]

            if {"en"} & {lang_by_cld2, lang_by_cld3, lang_by_fasttext}:
                lang_detected.add('en')
            if {'ms', 'id'} & {lang_by_cld2, lang_by_cld3, lang_by_fasttext}:
                lang_detected.add('ms')
                lang_detected.add('id')

            if len(lang_detected) == 0:
                try:
                    lang_by_google = translator.detect(
                        text_for_lang_detect).lang[:2]
                    lang_detected.add(lang_by_google)
                except BaseException as err:
                    print(err)

    return lang_detected


def embedding_saving(sentences_src, sentences_tgt, file_path_out):

    source_embedding = model_sentence_transformers.encode_multi_process(
        sentences_src, pool)

    target_embedding = model_sentence_transformers.encode_multi_process(
        sentences_tgt, pool)

    assert len(source_embedding) == len(
        target_embedding), "length of src and target don't match"

    cosine_scores = util.cos_sim(source_embedding, target_embedding)

    with open(file_path_out, 'a', encoding='utf-8') as fOUT:
        for k in range(len(cosine_scores)):
            cosine_score = cosine_scores[k][k]
            if cosine_score >= 0.7:
                fOUT.write("{:.4f} | {} | {}\n".format(
                    cosine_score, sentences_src[k].replace("|", " "), sentences_tgt[k].replace("|", " ")))


def clean_with_score(file_path_src, file_path_tgt, file_path_out, src_lang, tgt_lang):
    with open(file_path_src, encoding='utf-8') as file_src, \
            open(file_path_tgt, encoding='utf-8') as file_tgt:

        sentences_src = []
        sentences_tgt = []
        for (i, sentence_src), (j, sentence_tgt) in zip(enumerate(file_src), enumerate(file_tgt)):
            if len(sentence_src.strip()) > 20 and len(sentence_tgt.strip()) > 2:

                if tgt_lang in lang_detect(sentence_tgt.strip()):
                    sentences_src.append(sentence_src.strip())
                    sentences_tgt.append(sentence_tgt.strip())

            if (i+1) % 50000 == 0:
                embedding_saving(sentences_src, sentences_tgt, file_path_out)
                sentences_src.clear()
                sentences_tgt.clear()
                print("finished "+str(i))

        embedding_saving(sentences_src, sentences_tgt, file_path_out)
    print("finished "+ file_path_out)


if __name__ == '__main__':
    pool = model_sentence_transformers.start_multi_process_pool()

    rootdir = '/home/xuanlong/dataclean/data'

    for root, dirs, files in os.walk(rootdir):
        for file in files:
            if root.split(r'/')[-1] in ['ccaligned', 'ccmatrix', 'wikimatrix', 'wikimedia', 'wikimedia_v1', 'wikimedia_v20210402']:
                if os.path.splitext(file)[1] in {'.ta', '.zh', '.vi', '.ms', '.id'}:
                    file_path_src = os.path.join(
                        root, os.path.splitext(file)[0]+'.en')
                    file_path_tgt = os.path.join(root, file)
                    file_path_out = os.path.join(
                        root, os.path.splitext(file)[0])
                    src_lang = 'en'
                    tgt_lang = file.split('.')[-1]
                    clean_with_score(
                        file_path_src, file_path_tgt, file_path_out, src_lang, tgt_lang)
    model_sentence_transformers.stop_multi_process_pool(pool)
