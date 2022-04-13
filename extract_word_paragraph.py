import time
import fasttext
from sentence_transformers import SentenceTransformer, util
from docx import Document
import os

model_fasttext = fasttext.load_model('../model/lid.176.bin')
model_sentence_transformers = SentenceTransformer("LaBSE")

start_time=time.time()

def extract(filepath,new_filepath):
    wordDoc = Document(filepath)
    sentences_en=[]
    sentences_zh=[]
    for paragraph in wordDoc.paragraphs:
        text=paragraph.text.replace("\n", "")
        if text:
            if model_fasttext.predict(text)[0][0] == "__label__en":
                sentences_en.append(text)
            elif model_fasttext.predict(text)[0][0] == "__label__zh":
                sentences_zh.append(text)

    if len(sentences_zh) != 0 and len(sentences_en) != 0:
        source_embeddings = model_sentence_transformers.encode(
            sentences_zh, convert_to_tensor=True)

        target_embeddings = model_sentence_transformers.encode(
            sentences_en, convert_to_tensor=True)

        cosine_scores = util.cos_sim(
            source_embeddings, target_embeddings)


        with open(new_filepath, 'w', encoding='utf8') as fOut:
            for i in range(len(cosine_scores)):
                for j in range(len(cosine_scores[0])):
                    if cosine_scores[i][j] > 0.75:
                        fOut.write("{} | {}\n".format(sentences_zh[i].replace(
                            "|", " "), sentences_en[j].replace("|", "")))



path = '/home/zxl/ssd/WORK/data_clean/Batch_14/Retainers/Chinese'
new_path=path.replace("Batch_14", "Batch_14_extracted")

# os.makedirs(new_path, exist_ok=False)
# print("The new directory is created!")

files = os.listdir(path)
for f in files:
	extract(os.path.join(path, f),os.path.join(new_path, f[:-5]+'_paragraph.txt'))

print("--- %s seconds ---" % (time.time() - start_time))