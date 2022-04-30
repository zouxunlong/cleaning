import os
import re
import time
from sentence_transformers import SentenceTransformer
import pycld2 as cld2
import cld3
import fasttext
from googletrans import Translator


model_fasttext = fasttext.load_model('../model/lid.176.bin')
model_sentence_transformers = SentenceTransformer('../model/labse_bert_model')
translator = Translator()


start_time = time.time()


def lang_detect(text_for_lang_detect):

    if re.search('[\u4e00-\u9fff]', text_for_lang_detect):
        lang_detected = 'zh'
    elif re.search('[\u0B80-\u0BFF]', text_for_lang_detect):
        lang_detected = 'ta'
    else:

        lang_by_cld2 = cld2.detect(text_for_lang_detect)[2][0][1]
        lang_by_cld3 = cld3.get_language(text_for_lang_detect)[0]
        lang_by_fasttext = model_fasttext.predict(
            text_for_lang_detect)[0][0][-2:]

        if {"en", "ms", "id"} & {lang_by_cld2, lang_by_cld3, lang_by_fasttext}:
            if 'en' in [lang_by_cld2, lang_by_cld3, lang_by_fasttext]:
                lang_detected = 'en'
            elif {'ms', 'id'} & {lang_by_cld2, lang_by_cld3, lang_by_fasttext}:
                lang_detected = 'ms'
        else:
            try:
                lang_by_google = translator.detect(
                    text_for_lang_detect).lang[:2]
                lang_detected = lang_by_google
            except:
                lang_detected = 'un'
    return lang_detected


def embedding_saving(sentences_en, sentences_tgt, filepath_out):
    # source_embedding = model_sentence_transformers.encode(
    #     sentences_en, convert_to_numpy=True, normalize_embeddings=True)

    # target_embedding = model_sentence_transformers.encode(
    #     sentences_tgt, convert_to_numpy=True, normalize_embeddings=True)

    source_embedding = model_sentence_transformers.encode_multi_process(sentences_en, pool)

    target_embedding = model_sentence_transformers.encode_multi_process(sentences_tgt, pool)

    assert len(source_embedding) == len(
        target_embedding), "length of src and target don't match"

    with open(filepath_out, 'a', encoding='utf8') as fOUT:
        for k in range(len(source_embedding)):
            cosine = source_embedding[k].dot(target_embedding[k])
            if cosine >= 0.7:
                fOUT.write("{:.4f} | {} | {}\n".format(
                    cosine, sentences_en[k].replace("|", " "), sentences_tgt[k].replace("|", " ")))


def clean_with_score(filepath_en, filepath_ms, filepath_out):
    with open(filepath_en, encoding='utf-8') as file_en, \
            open(filepath_ms, encoding='utf-8') as file_ms:

        sentences_en = []
        sentences_tgt = []
        for (i, sentence_en), (j, sentence_ms) in zip(enumerate(file_en), enumerate(file_ms)):
            if len(sentence_en.strip()) > 10 and len(sentence_ms.strip()) > 10:
                language_detect = lang_detect(sentence_ms.strip())
                if language_detect == 'ms':
                    sentences_en.append(sentence_en.strip())
                    sentences_tgt.append(sentence_ms.strip())

            if (i+1) % 20000 == 0:
                embedding_saving(sentences_en, sentences_tgt, filepath_out)
                sentences_en.clear()
                sentences_tgt.clear()
                print("finished "+str(i))

        embedding_saving(sentences_en, sentences_tgt, filepath_out)
        print("finished "+str(len(sentences_en)))

if __name__ == '__main__':
    pool = model_sentence_transformers.start_multi_process_pool()
    clean_with_score("/home/xuanlong/dataclean/data/wikimedia/wikimedia.en-ms.en",
                    "/home/xuanlong/dataclean/data/wikimedia/wikimedia.en-ms.ms", "/home/xuanlong/dataclean/data/wikimedia/wikimedia.en-ms")

    model_sentence_transformers.stop_multi_process_pool(pool)
    print("--- %s seconds ---" % (time.time() - start_time))
