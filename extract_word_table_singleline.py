import time
import pycld2 as cld2
from docx import Document
import os


start_time = time.time()


def extract(filepath, new_filepath):
    wordDoc = Document(filepath)

    for table in wordDoc.tables:
        for row in table.rows:
            sentence_pair = []
            for cell in row.cells:
                sentence_pair.append(cell.text.replace("\n", ""))
            language_type0 = cld2.detect(sentence_pair[0])[2][0][1]
            language_type1 = cld2.detect(sentence_pair[1])[2][0][1]

            if language_type0 != language_type1:
                with open(new_filepath, 'a', encoding='utf8') as fOut:
                    if language_type0 == "en":
                        fOut.write("{} | {}\n".format(sentence_pair[0].replace(
                            "|", " "), sentence_pair[1].replace("|", "")))
                    elif language_type1 == "en":
                        fOut.write("{} | {}\n".format(sentence_pair[1].replace(
                            "|", " "), sentence_pair[0].replace("|", "")))

path = '../WORK/batch11/Retainers/Tamil'
new_path = path.replace("batch11", "batch11_extracted")

if not os.path.exists(new_path):
    os.makedirs(new_path)

files = os.listdir(path)
for f in files:
    f='Tamil Document 58 (TE).docx'
    extract(os.path.join(path, f), os.path.join(new_path, f[:-5]+'.txt'))

print("--- %s seconds ---" % (time.time() - start_time))
