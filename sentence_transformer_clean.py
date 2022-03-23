import fasttext
from sentence_transformers import SentenceTransformer, util

model_sentence_transformers = SentenceTransformer("LaBSE")

model_fasttext = fasttext.load_model('./lid.176.bin')

min_sent_len = 10

sentences_zh = []
sentences_en = []

print("Read zh and en file")
with open("wikimedia.en-zh.zh", encoding='utf-8') as file_zh, open("wikimedia.en-zh.en", encoding='utf-8') as file_en:
    for (i, sentence_zh), (j, sentence_en) in zip(enumerate(file_zh), enumerate(file_en)):
        if i in range(0, 500, 1):
            sentence_zh = sentence_zh.strip()
            sentence_en = sentence_en.strip()

            if model_fasttext.predict(sentence_zh)[0][0] == "__label__zh" and model_fasttext.predict(sentence_en)[0][0] == "__label__en":
                sentences_zh.append(sentence_zh)
                sentences_en.append(sentence_en)


print("Chinese Sentences:", len(sentences_zh))
print("English Sentences:", len(sentences_en))


print("Encode source sentences")
source_embeddings = model_sentence_transformers.encode(
    sentences_zh, show_progress_bar=True, convert_to_tensor=True)


print("Encode target sentences")
target_embeddings = model_sentence_transformers.encode(
    sentences_en, show_progress_bar=True, convert_to_tensor=True)

cosine_scores = util.cos_sim(source_embeddings, target_embeddings)


print("Write sentences to disc")
sentences_written = 0

with open('parallel-sentences-cleaned_out.txt', 'at', encoding='utf8') as fOut:
    for i in range(len(cosine_scores)):
        if cosine_scores[i][i] > 0.6:
            fOut.write("{} | {} | Score: {:.4f}\n".format(sentences_zh[i].replace(
                "|", " "), sentences_en[i].replace("|", ""), cosine_scores[i][i]))
            sentences_written += 1

print("Done. {} sentences written".format(sentences_written))