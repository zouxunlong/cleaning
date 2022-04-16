import re
import time
# import fasttext
from docx import Document
import os

# model_fasttext = fasttext.load_model('../model/lid.176.bin')

start_time = time.time()


def detect_unaligned(filepath):
    wordDoc = Document(filepath)

    for table in wordDoc.tables:
        for row in table.rows:
            sentences_pair = []
            sentences_en = []
            sentences_non_en = []

            if len(row.cells) >= 2:
                for cell in row.cells:
                    sentences_pair.append([text for text in cell.text.split('\n')])

                for sentence in sentences_pair[0]:
                    if sentence and not sentence.isspace():
                        if sentence.strip()[:16].lower()=='stayprepared.sg/':
                            sentences_en[-1]=sentences_en[-1]+sentence
                        elif sentence.strip().lower()[:5] not in ["call-","callo","frame","step ","butto","heade","headl","point","title","footn"]:
                            sentences_en.append(sentence)
                        
                for sentence in sentences_pair[1]:
                    if sentence and not sentence.isspace():
                        if sentence.strip()[:16].lower()=='stayprepared.sg/':
                            sentences_non_en[-1]=sentences_non_en[-1]+sentence
                        elif sentence.strip().lower()[:5] not in ["call-","callo","frame","step ","butto","heade","headl","point","title","footn"]:
                            sentences_non_en.append(sentence)

            if len(sentences_en) != 0 and len(sentences_non_en) != 0:
                if len(sentences_en) == len(sentences_non_en):
                    pass
                else:
                    os.startfile(filepath)
                    print(len(sentences_en))
                    print("\n".join(sentences_en))
                    print(len(sentences_non_en))
                    print("\n".join(sentences_non_en))
                    print('detected')


dir = "../WORK/batch11/Temasek Foundation/Tamil"


files = os.listdir(dir)
files.reverse()
for f in files:
    detect_unaligned(os.path.join(dir, f))

print("--- %s seconds ---" % (time.time() - start_time))
