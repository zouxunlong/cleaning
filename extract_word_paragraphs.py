import time
import pycld2 as cld2
import cld3
import fasttext
from docx import Document
import os
import re
import string

start_time = time.time()
model_fasttext = fasttext.load_model('../model/lid.176.bin')


def allocate_text(text, sentences_en, sentences_ms, sentences_ta, sentences_zh):

    trimed_text=re.sub("\w+@\S+\s?|http\S*\s?|www\.\S*\s?|[0-9]", "", text)
    new_text = trimed_text.translate(str.maketrans('', '', string.punctuation)).strip().lower()
    
    language_type_by_cld2 = cld2.detect(new_text)[2][0][1]
    language_type_by_cld3 = cld3.get_language(new_text)
    language_type_by_fasttext = model_fasttext.predict(new_text)[0][0]
    if language_type_by_cld2 == "en" or language_type_by_fasttext == "__label__en":
        sentences_en.append(text)
    elif language_type_by_cld2 in ["ms", "id"] or language_type_by_fasttext in ["__label__ms", "__label__id"] or language_type_by_cld3[0] in ["ms"]:
        sentences_ms.append(text)
    elif language_type_by_cld2 in ["zh", "ja"] or language_type_by_fasttext in ["__label__zh", "__label__ja"]:
        text = text.replace(" ", "")
        sentences_zh.append(text)
    elif language_type_by_cld2 == "ta" or language_type_by_fasttext == "__label__ta":
        sentences_ta.append(text)



def extract(filepath):
    wordDoc = Document(filepath)
    sentences_en = []
    sentences_ms = []
    sentences_ta = []
    sentences_zh = []

    for paragraph in wordDoc.paragraphs:

        texts = [text.strip() for text in paragraph.text.split('\n')]

        [allocate_text(text, sentences_en, sentences_ms,
                       sentences_ta, sentences_zh) for text in texts if text]

    for table in wordDoc.tables:
        for row in table.rows:
            for cell in row.cells:
                texts = [text.strip() for text in cell.text.split('\n')]
                [allocate_text(text, sentences_en, sentences_ms,
                               sentences_ta, sentences_zh) for text in texts if text]


    for section in wordDoc.sections:
        header = section.header
        footer = section.footer

        for paragraph in header.paragraphs:
            texts = [text.strip() for text in paragraph.text.split('\n')]
            [allocate_text(text, sentences_en, sentences_ms,
                           sentences_ta, sentences_zh) for text in texts if text]

        for paragraph in footer.paragraphs:
            texts = [text.strip() for text in paragraph.text.split('\n')]
            [allocate_text(text, sentences_en, sentences_ms,
                           sentences_ta, sentences_zh) for text in texts if text]


    e = wordDoc.element
    textbox_elements = e.xpath('.//w:drawing//w:txbxContent')
    for textbox_element in textbox_elements:
        text = " ".join(" ".join(textbox_element.xpath(".//text()")).split())
        if text:
            allocate_text(text, sentences_en, sentences_ms,
                          sentences_ta, sentences_zh)


    print("sentences_en number:{}".format(len(sentences_en)))
    print("sentences_ms number:{}".format(len(sentences_ms)))
    print("sentences_ta number:{}".format(len(sentences_ta)))
    print("sentences_zh number:{}".format(len(sentences_zh)))


extract("2021MGPLetterTopupETCM1.docx")

print("--- %s seconds ---" % (time.time() - start_time))
