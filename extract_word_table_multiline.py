import time
import pycld2 as cld2
from docx import Document
import os


start_time = time.time()


def extract(filepath, new_filepath):
    wordDoc = Document(filepath)

    for table in wordDoc.tables:
        for row in table.rows:
            sentences_pair = []
            sentences_en = []
            sentences_non_en = []

            if len(row.cells) >= 2:
                for cell in row.cells:
                    sentences_pair.append(
                        [text for text in cell.text.split('\n')])

                for sentence in sentences_pair[0]:
                    if sentence and not sentence.isspace():
                        if sentence.strip()[:16].lower() == 'stayprepared.sg/':
                            sentences_en[-1] = sentences_en[-1]+sentence
                        elif sentence.strip().lower()[:5] not in ["call-", "callo", "frame", "step ", "langk", "butto", "heade", "headl", "point", "title", "footn"]:
                            sentences_en.append(sentence)

                for sentence in sentences_pair[1]:
                    if sentence and not sentence.isspace():
                        if sentence.strip()[:16].lower() == 'stayprepared.sg/':
                            sentences_non_en[-1] = sentences_non_en[-1]+sentence
                        elif sentence.strip().lower()[:5] not in ["call-", "callo", "frame", "step ", "langk", "butto", "heade", "headl", "point", "title", "footn"]:
                            sentences_non_en.append(sentence)

            if len(sentences_en) != 0 and len(sentences_non_en) != 0:
                assert len(sentences_en) == len(sentences_non_en)
                with open(new_filepath, 'a', encoding='utf8') as fOut:
                    for i in range(len(sentences_en)):
                        if cld2.detect(sentences_en[i])[2][0][1] != cld2.detect(sentences_non_en[i])[2][0][1]:
                            fOut.write("{} | {}\n".format(sentences_en[i].replace(
                                "|", " "), sentences_non_en[i].replace("|", "")))


path = '../WORK/Batch7(CD7)/Temasek Foundation/Malay'
new_path = path.replace("Batch7(CD7)", "Batch7(CD7)_extracted")

if not os.path.exists(new_path):
    os.makedirs(new_path)

files = os.listdir(path)
for f in files:
    extract(os.path.join(path, f), os.path.join(new_path, f[:-5]+'.txt'))

print("--- %s seconds ---" % (time.time() - start_time))
