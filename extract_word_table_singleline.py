import time
import fasttext
from docx import Document
import os

model_fasttext = fasttext.load_model('../model/lid.176.bin')

start_time=time.time()

def extract(filepath,new_filepath):
    wordDoc = Document(filepath)

    for table in wordDoc.tables:
        for row in table.rows:
            sentence_pair= []
            for cell in row.cells:
                sentence_pair.append(cell.text.replace("\n", ""))
            language_types=model_fasttext.predict(sentence_pair)

            if language_types[0][0] != language_types[0][1]:
                with open(new_filepath, 'a', encoding='utf8') as fOut:
                    fOut.write("{} | {}\n".format(sentence_pair[0].replace(
                        "|", " "), sentence_pair[1].replace("|", "")))

path = '/home/zxl/ssd/WORK/data_clean/Batch_14/Retainers/Chinese'

new_path=path.replace("Batch_14", "Batch_14_extracted")

os.makedirs(new_path, exist_ok=False)
print("The new directory is created!")

files = os.listdir(path)
for f in files:
	extract(os.path.join(path, f),os.path.join(new_path, f[:-5]+'_table.txt'))

print("--- %s seconds ---" % (time.time() - start_time))