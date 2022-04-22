import time
import pycld2 as cld2
import fasttext
from docx import Document
import os

start_time = time.time()
model_fasttext = fasttext.load_model('../model/lid.176.bin')


def extract(filepath):
    wordDoc = Document(filepath)
    sentences_en = []
    sentences_ms = []
    sentences_ta = []
    sentences_zh = []

    for paragraph in wordDoc.paragraphs:
        texts=[text.strip() for text in paragraph.text.split('\n')]
        for text in texts:
            if text:
                language_type = cld2.detect(text)[2][0][1]
                if language_type == "en":
                    sentences_en.append(text)
                elif language_type == "ms":
                    sentences_ms.append(text)
                elif language_type == "ta":
                    sentences_ta.append(text)
                elif model_fasttext.predict(text)[0][0] == "__label__zh":
                    sentences_zh.append(text)

    for table in wordDoc.tables:
        for row in table.rows:

            for cell in row.cells:
                texts=[text.strip() for text in cell.text.split('\n')]

                for text in texts:
                    if text:
                        language_type = cld2.detect(text)[2][0][1]
                        if language_type == "en":
                            sentences_en.append(text)
                        elif language_type == "ms":
                            sentences_ms.append(text)
                        elif language_type == "ta":
                            sentences_ta.append(text)
                        elif model_fasttext.predict(text)[0][0] == "__label__zh":
                            sentences_zh.append(text)


    print("sentences_en number:{}".format(len(sentences_en)))
    print("sentences_ms number:{}".format(len(sentences_ms)))
    print("sentences_ta number:{}".format(len(sentences_ta)))
    print("sentences_zh number:{}".format(len(sentences_zh)))


extract("2021MGPLetterTopupETCM1.docx")

print("--- %s seconds ---" % (time.time() - start_time))
