import time
import fasttext
from sentence_transformers import SentenceTransformer, util

model_sentence_transformers = SentenceTransformer("LaBSE")

model_fasttext = fasttext.load_model('./model/lid.176.bin')

sentences_zh = []
sentences_en = []
sentences_written = 0
start_time = time.time()

print("Read zh and en file")
with open("./noisy/wikimedia/wikimedia.en-zh.zh", encoding='utf-8') as file_zh, open("./noisy/wikimedia/wikimedia.en-zh.en", encoding='utf-8') as file_en:
    for (i, sentence_zh), (j, sentence_en) in zip(enumerate(file_zh), enumerate(file_en)):

        sentence_zh = sentence_zh.strip()
        sentence_en = sentence_en.strip()
        if len(sentence_zh) > 3:
            for sentence in sentence_zh.split('。'):
                if model_fasttext.predict(sentence)[0][0] == "__label__zh" and model_fasttext.predict(sentence)[1][0] > 0.75:
                    sentences_zh.append(sentence)
            for sentence in sentence_en.split('.'):
                if model_fasttext.predict(sentence)[0][0] == "__label__en" and model_fasttext.predict(sentence)[1][0] > 0.75:
                    sentences_en.append(sentence)

        if i > 0 and i % 50 == 0:
            print("Chinese Sentences:", len(sentences_zh))
            print("English Sentences:", len(sentences_en))
            if len(sentences_zh) != 0 and len(sentences_en) != 0:
                print("Encode source sentences")
                source_embeddings = model_sentence_transformers.encode(
                    sentences_zh, convert_to_tensor=True)

                print("Encode target sentences")
                target_embeddings = model_sentence_transformers.encode(
                    sentences_en, convert_to_tensor=True)

                cosine_scores = util.cos_sim(
                    source_embeddings, target_embeddings)

                print("Write sentences to disc")

                with open('./noisy/wikimedia/clean1.txt', 'a', encoding='utf8') as fOut:
                    for i in range(len(cosine_scores)):
                        for j in range(len(cosine_scores[0])):
                            if cosine_scores[i][j] > 0.7:
                                ratio = len(
                                    sentences_en[j])/len(sentences_zh[i])
                                if ratio > 2 and ratio < 4:
                                    fOut.write("{} | {}\n".format(sentences_zh[i].replace(
                                        "|", " "), sentences_en[j].replace("|", "")))

                                    sentences_written += 1

            sentences_zh = []
            sentences_en = []

print("Done. {} sentences written".format(sentences_written))
print("--- %s seconds ---" % (time.time() - start_time))
