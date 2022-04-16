import time
# import cld3
import pycld2 as cld2
from sentence_transformers import SentenceTransformer, util
from docx import Document
import os

model_sentence_transformers = SentenceTransformer("LaBSE")

start_time=time.time()


def extract(filepath,new_filepath):
    wordDoc = Document(filepath)
    sentences_en=[]
    sentences_non_en=[]
    
    for paragraph in wordDoc.paragraphs:
        text=paragraph.text.replace("\n", "")
        if text:
            # language_type=cld3.get_language(text).language
            language_type = cld2.detect(text)[2][0][1]
            if language_type=="en":
                sentences_en.append(text)
            elif language_type=="ms":
                sentences_non_en.append(text)

    if len(sentences_en) != 0 and len(sentences_non_en) != 0:
        source_embeddings = model_sentence_transformers.encode(
            sentences_en, convert_to_tensor=True)

        target_embeddings = model_sentence_transformers.encode(
            sentences_non_en, convert_to_tensor=True)

        cosine_scores = util.cos_sim(
            source_embeddings, target_embeddings)


        with open(new_filepath, 'w', encoding='utf8') as fOut:
            for i in range(len(cosine_scores)):
                for j in range(len(cosine_scores[0])):
                    if cosine_scores[i][j] > 0.8:
                        fOut.write("{} | {}\n".format(sentences_en[i].replace(
                            "|", " "), sentences_non_en[j].replace("|", "")))



path = '../WORK/Batch7(CD7)/Retainers/Malay'
new_path=path.replace("Batch7(CD7)", "Batch7(CD7)_extracted")

# os.makedirs(new_path, exist_ok=False)
# print("The new directory is created!")

files = os.listdir(path)
for f in files:
	extract(os.path.join(path, f),os.path.join(new_path, f[:-5]+'.txt'))

print("--- %s seconds ---" % (time.time() - start_time))