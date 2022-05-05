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


def get_dp(M):
    m = len(M)
    n = len(M[0])
    dp = [[0]*n for i in range(m)]
    dp[0] = [sum(M[0][:i+1]) for i in range(n)]
    for i in range(1, m):
        dp[i][0] = dp[i-1][0] + M[i][0]

    for i in range(1, m):
        for j in range(1, n):
            dp[i][j] = max(dp[i-1][j], dp[i][j-1]) + M[i][j]
    return dp


def retrieve_coordinate(dp, coordinate):
    if coordinate[0] == 0:
        return (coordinate[0], coordinate[1]-1)
    elif coordinate[1] == 0:
        return (coordinate[0]-1, coordinate[1])
    elif dp[coordinate[0]-1][coordinate[1]] >= dp[coordinate[0]][coordinate[1]-1]:
        return (coordinate[0]-1, coordinate[1])
    else:
        return (coordinate[0], coordinate[1]-1)


def get_path(M):

    coordinate = (len(M)-1, len(M[0])-1)
    path = [coordinate]
    dp = get_dp(M)

    while coordinate != (0, 0):
        coordinate = retrieve_coordinate(dp, coordinate)
        path.append(coordinate)
    path.reverse()
    return path


def lang_detect(text_for_lang_detect):

    text_for_lang_detect = re.sub(
        "(?i)\w+@\S+\s?|http\S*\s?|www\.\S*\s?|[a-z\.]*\.sg\S*\s?|[0-9]+\s?", "", text_for_lang_detect)
    text_for_lang_detect = text_for_lang_detect.translate(
        str.maketrans('-', ' ', string.punctuation.replace('-', ''))).strip().lower()

    if text_for_lang_detect:
        if re.search('[\u4e00-\u9fff]', text_for_lang_detect):
            lang_detected = 'zh'
        elif re.search('[\u0B80-\u0BFF]', text_for_lang_detect):
            lang_detected = 'ta'
        else:
            try:
                lang_by_cld2 = cld2.detect(text_for_lang_detect)[2][0][1]
                lang_by_cld3 = cld3.get_language(text_for_lang_detect)[0]
                lang_by_fasttext = model_fasttext.predict(
                    text_for_lang_detect)[0][0][-2:]

                if {"en", "ms", "id",'vi'} & {lang_by_cld2, lang_by_cld3, lang_by_fasttext}:
                    if 'en' in [lang_by_cld2, lang_by_cld3, lang_by_fasttext]:
                        lang_detected = 'en'
                    elif {'ms', 'id'} & {lang_by_cld2, lang_by_cld3, lang_by_fasttext}:
                        lang_detected = 'id'
                    elif {'vi'} & {lang_by_cld2, lang_by_cld3, lang_by_fasttext}:
                        lang_detected = 'vi'
                else:
                    lang_by_google = translator.detect(
                        text_for_lang_detect).lang[:2]
                    lang_detected = lang_by_google
            except:
                lang_detected = 'un'
    else:
        lang_detected = 'un'

    return lang_detected


def embedding_saving(sentences_en, sentences_tgt, filepath_out):
    # source_embedding = model_sentence_transformers.encode(
    #     sentences_en, convert_to_numpy=True, normalize_embeddings=True)

    # target_embedding = model_sentence_transformers.encode(
    #     sentences_tgt, convert_to_numpy=True, normalize_embeddings=True)

    source_embedding = model_sentence_transformers.encode_multi_process(
        sentences_en, pool)

    target_embedding = model_sentence_transformers.encode_multi_process(
        sentences_tgt, pool)

    cosine_scores = util.cos_sim(source_embedding, target_embedding)

    path = get_path(cosine_scores)

    with open(filepath_out, 'a', encoding='utf-8') as fOUT:
        for k in range(len(path)):
            cosine = source_embedding[path[k][0]].dot(
                target_embedding[path[k][1]])
            if cosine >= 0.7:
                fOUT.write("{:.4f} | {} | {}\n".format(
                    cosine, sentences_en[path[k][0]].replace("|", " "), sentences_tgt[path[k][1]].replace("|", " ")))


def clean_with_score(filepath_en, file_path_tgt, filepath_out):
    with open(filepath_en, encoding='utf-8') as file_en, \
            open(file_path_tgt, encoding='utf-8') as file_ms:

        sentences_en = []
        sentences_tgt = []
        for (i, sentence_en), (j, sentence_tgt) in zip(enumerate(file_en), enumerate(file_ms)):
            if len(sentence_en.strip()) > 10 and len(sentence_tgt.strip()) > 10:
                language_detect = lang_detect(sentence_tgt.strip())
                if language_detect == file_path_tgt[-2:]:
                    sentences_en.append(sentence_en.strip())
                    sentences_tgt.append(sentence_tgt.strip())

            if (i+1) % 500 == 0:
                embedding_saving(sentences_en, sentences_tgt, filepath_out)
                sentences_en.clear()
                sentences_tgt.clear()
                print("finished "+str(i))

        embedding_saving(sentences_en, sentences_tgt, filepath_out)
        print("finished "+str(len(sentences_en)))
    print("finished "+str(filepath_out))


if __name__ == '__main__':
    pool = model_sentence_transformers.start_multi_process_pool()

    rootdir = '/home/xuanlong/dataclean/data'

    for root, dirs, files in os.walk(rootdir):
        for file in files:
            if root.split(r'/')[-1] not in ['ccaligned', 'ccmatrix', 'wikimatrix', 'wikimedia']:
                a = os.path.splitext(file)
                if os.path.splitext(file)[1] == '.en':
                    file_path_en = os.path.join(root, file)
                    file_path_tgt = os.path.join(root, os.path.splitext(
                        file)[0]+'.'+os.path.splitext(file)[0][-2:])
                    filepath_out = os.path.join(root, os.path.splitext(
                        file)[0])
                    clean_with_score(file_path_en, file_path_tgt, filepath_out)

    model_sentence_transformers.stop_multi_process_pool(pool)
