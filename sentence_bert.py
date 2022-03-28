import time
import fasttext
from sentence_transformers import SentenceTransformer, util

model_sentence_transformers = SentenceTransformer("LaBSE")

model_fasttext = fasttext.load_model('./lid.176.bin')


start_time=time.time()


with open("wikimedia.en-zh.zh", encoding='utf-8') as file_zh, open("wikimedia.en-zh.en", encoding='utf-8') as file_en:
    for (i, sentence_zh), (j, sentence_en) in zip(enumerate(file_zh), enumerate(file_en)):
        if i in range(100):
            sentence_zh = sentence_zh.strip()
            sentence_en = sentence_en.strip()
            ratio = len(sentence_en)/len(sentence_zh)
            if ratio > 1.8 and ratio < 4.5 and len(sentence_zh) > 3:
                sentences_zh = []
                sentences_en = []
                for sentence in sentence_zh.split('。'):
                    if model_fasttext.predict(sentence)[0][0] == "__label__zh" and model_fasttext.predict(sentence)[1][0] > 0.6:
                        sentences_zh.append(sentence)
                for sentence in sentence_en.split('.'):
                    if model_fasttext.predict(sentence)[0][0] == "__label__en" and model_fasttext.predict(sentence)[1][0] > 0.6:
                        sentences_en.append(sentence)

                if len(sentences_zh) != 0 and len(sentences_en) != 0:
                    source_embeddings = model_sentence_transformers.encode(
                        sentences_zh, device='cpu')
                    target_embeddings = model_sentence_transformers.encode(
                        sentences_en, device='cpu')

                    cosine_scores = util.cos_sim(
                        source_embeddings, target_embeddings)

                    with open('parallel-sentences-cleaned_out3.txt', 'at', encoding='utf8') as fOut:
                        for i in range(len(cosine_scores)):
                            for j in range(len(cosine_scores[0])):
                                if cosine_scores[i][j] > 0.65:
                                    fOut.write("{} | {}\n".format(sentences_zh[i].replace(
                                        "|", " "), sentences_en[j].replace("|", "")))

print("--- %s seconds ---" % (time.time() - start_time))
