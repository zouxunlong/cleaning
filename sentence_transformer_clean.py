import fasttext
from sentence_transformers import SentenceTransformer, util

model_sentence_transformers = SentenceTransformer("LaBSE")

model_fasttext = fasttext.load_model('./lid.176.bin')

sentences_zh = []
sentences_en = []

print("Read zh and en file")
with open("wikimedia.en-zh.zh", encoding='utf-8') as file_zh, open("wikimedia.en-zh.en", encoding='utf-8') as file_en:
    for (i, sentence_zh), (j, sentence_en) in zip(enumerate(file_zh), enumerate(file_en)):
        if i in range(0, 100):
            sentence_zh = sentence_zh.strip()
            sentence_en = sentence_en.strip()
            ratio = len(sentence_en)/len(sentence_zh)
            if ratio > 1.8 and ratio < 4.5 and len(sentence_zh) > 5:
                for sentence in sentence_zh.split('。'):
                    if model_fasttext.predict(sentence)[0][0] == "__label__zh" and model_fasttext.predict(sentence)[1][0] >0.6:
                        sentences_zh.append(sentence)
                for sentence in sentence_en.split('.'):
                    if model_fasttext.predict(sentence)[0][0] == "__label__en" and model_fasttext.predict(sentence)[1][0] >0.6:
                        sentences_en.append(sentence)


print("Chinese Sentences:", len(sentences_zh))
print("English Sentences:", len(sentences_en))

difference = abs(len(sentences_zh)-len(sentences_en))

print("Encode source sentences")
source_embeddings = model_sentence_transformers.encode(
    sentences_zh, show_progress_bar=True, device='cpu')


print("Encode target sentences")
target_embeddings = model_sentence_transformers.encode(
    sentences_en, show_progress_bar=True, device='cpu')

cosine_scores = util.cos_sim(source_embeddings, target_embeddings)

print("Write sentences to disc")
sentences_written = 0

with open('parallel-sentences-cleaned_out.txt', 'at', encoding='utf8') as fOut:
    for i in range(len(cosine_scores)):
        for j in range(i-difference-1, i+difference+1):
            if cosine_scores[i][j] > 0.65:
                fOut.write("{} | {}\n".format(sentences_zh[i].replace(
                    "|", " "), sentences_en[j].replace("|", "")))
                sentences_written += 1

print("Done. {} sentences written".format(sentences_written))
