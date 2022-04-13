import re
import time
import fasttext
from sentence_transformers import SentenceTransformer, util
from docx import Document
import os

model_fasttext = fasttext.load_model('../model/lid.176.bin')
model_sentence_transformers = SentenceTransformer("LaBSE")

start_time = time.time()


def extract(filepath, new_filepath):
    wordDoc = Document(filepath)

    for table in wordDoc.tables:
        for row in table.rows:
            sentences_pair = []
            sentences_en = []
            sentences_zh = []

            if len(row.cells) >= 2:
                for cell in row.cells:
                    sentences_pair.append([text for text in cell.text.split('\n')])

                for sentence in sentences_pair[0]:
                    if sentence:
                        sentences_en.append(sentence)
                for sentence in sentences_pair[1]:
                    if sentence:
                        sentences_zh.append(sentence)

            if len(sentences_zh) != 0 and len(sentences_en) != 0:
                if len(sentences_zh) == len(sentences_en):
                    with open(new_filepath, 'a', encoding='utf8') as fOut:
                        for i in range(len(sentences_zh)):
                            if model_fasttext.predict(sentences_en[i])[0][0] != model_fasttext.predict(sentences_zh[i])[0][0]:
                                fOut.write("{} | {}\n".format(sentences_en[i].replace(
                                    "|", " "), sentences_zh[i].replace("|", "")))
                else:
                    clean_sentences_zh = [sentence_zh for sentence_zh in sentences_zh if model_fasttext.predict(
                        sentence_zh)[0][0] in ["__label__zh", "__label__ja"]]

                    if len(clean_sentences_zh) != 0:
                        source_embeddings = model_sentence_transformers.encode(
                            sentences_en, convert_to_tensor=True)
                        target_embeddings = model_sentence_transformers.encode(
                            clean_sentences_zh, convert_to_tensor=True)
                        cosine_scores = util.cos_sim(
                            source_embeddings, target_embeddings)

                        with open(new_filepath, 'a', encoding='utf8') as fOut:
                            for i in range(len(cosine_scores)):
                                for j in range(len(cosine_scores[0])):
                                    if cosine_scores[i][j] > 0.7:
                                        fOut.write("{} | {}\n".format(sentences_en[i].replace(
                                            "|", " "), clean_sentences_zh[j].replace("|", "")))


path = '/home/zxl/ssd/WORK/data_clean/Batch_14/Temasek Foundation/Chinese'

new_path = path.replace("Batch_14", "Batch_14_extracted")

# os.makedirs(new_path, exist_ok=False)
# print("The new directory is created!")

files = os.listdir(path)
for f in files:
    extract(os.path.join(path, f), os.path.join(new_path, f[:-5]+'_table.txt'))

print("--- %s seconds ---" % (time.time() - start_time))
