import time
from sentence_transformers import SentenceTransformer


model_sentence_transformers = SentenceTransformer('../model/labse_bert_model')

start_time = time.time()
for path in ["../data/noisy_4.en-zh","../data/noisy_5.en-zh","../data/noisy_2.en-zh","../data/noisy_1.en-zh"]:
    with open(path, encoding='utf-8') as fIN,\
            open("../data/clean_0_9.en-zh", 'a', encoding='utf8') as fOUT_9, \
            open("../data/clean_0_85.en-zh", 'a', encoding='utf8') as fOUT_85, \
            open("../data/clean_0_8.en-zh", 'a', encoding='utf8') as fOUT_8, \
            open("../data/clean_0_75.en-zh", 'a', encoding='utf8') as fOUT_75, \
            open("../data/clean_0_7.en-zh", 'a', encoding='utf8') as fOUT_7:
        sentences_en = []
        sentences_zh = []
        for i, sentence in enumerate(fIN):
            sentences = sentence.split('|')
            sentences_en.append(sentences[0].strip())
            sentences_zh.append(sentences[1].strip())

            if (i+1) % 100000 == 0:
                source_embedding = model_sentence_transformers.encode(
                    sentences_en, convert_to_numpy=True, normalize_embeddings=True)
                target_embedding = model_sentence_transformers.encode(
                    sentences_zh, convert_to_numpy=True, normalize_embeddings=True)

                for j in range(len(source_embedding)):
                    cosine = source_embedding[j].dot(target_embedding[j])
                    if cosine >= 0.9:
                        fOUT_9.write("{:.4f} | {} | {}\n".format(
                            cosine, sentences_en[j].replace("|", " "), sentences_zh[j].replace("|", " ")))
                    elif cosine >= 0.85:
                        fOUT_85.write("{:.4f} | {} | {}\n".format(
                            cosine, sentences_en[j].replace("|", " "), sentences_zh[j].replace("|", " ")))
                    elif cosine >= 0.8:
                        fOUT_8.write("{:.4f} | {} | {}\n".format(
                            cosine, sentences_en[j].replace("|", " "), sentences_zh[j].replace("|", " ")))
                    elif cosine >= 0.75:
                        fOUT_75.write("{:.4f} | {} | {}\n".format(
                            cosine, sentences_en[j].replace("|", " "), sentences_zh[j].replace("|", " ")))
                    elif cosine >= 0.7:
                        fOUT_7.write("{:.4f} | {} | {}\n".format(
                            cosine, sentences_en[j].replace("|", " "), sentences_zh[j].replace("|", " ")))
                sentences_en.clear()
                sentences_zh.clear()
                print("finished "+str(i))
print("--- %s seconds ---" % (time.time() - start_time))
