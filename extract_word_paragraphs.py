import time
import pycld2 as cld2
import cld3
import fasttext
from docx import Document
import os
import re
import string
from docx.oxml.shared import qn
from docx.text.paragraph import Paragraph
from docx.text.run import Run

start_time = time.time()


def GetParagraphRuns(paragraph):
    def _get(node, parent):
        for child in node:
            if child.tag == qn('w:r'):
                yield Run(child, parent)
            if child.tag == qn('w:hyperlink'):
                yield from _get(child, parent)
    return list(_get(paragraph._element, paragraph))


Paragraph.runs = property(lambda self: GetParagraphRuns(self))

model_fasttext = fasttext.load_model('../model/lid.176.bin')


def allocate_text(text, sentences_en, sentences_ms, sentences_ta, sentences_zh):

    trimed_text = re.sub(
        "\w+@\S+\s?|http\S*\s?|www\.\S*\s?|[0-9]|\{[\s\S]*\}", "", text)

    text_for_lang_detect = trimed_text.translate(
        str.maketrans('', '', string.punctuation)).strip().lower()

    if text_for_lang_detect:
        
        text_for_sentence_mining = re.sub("^[a-zA-Z0-9]+\.\s", "", text)

        language_type_by_cld2 = cld2.detect(text_for_lang_detect)[2][0][1]
        language_type_by_cld3 = cld3.get_language(text_for_lang_detect)
        language_type_by_fasttext = model_fasttext.predict(text_for_lang_detect)[
            0][0]
        if language_type_by_cld2 == "en" or language_type_by_fasttext == "__label__en":
            sentences_en.append(text_for_sentence_mining)
        elif language_type_by_cld2 in ["ms", "id"] or language_type_by_fasttext in ["__label__ms", "__label__id"] or language_type_by_cld3[0] in ["ms"]:
            sentences_ms.append(text_for_sentence_mining)
        elif language_type_by_cld2 in ["zh", "ja"] or language_type_by_fasttext in ["__label__zh", "__label__ja"]:
            text = text.replace(" ", "")
            sentences_zh.append(text_for_sentence_mining)
        elif language_type_by_cld2 == "ta" or language_type_by_fasttext == "__label__ta":
            sentences_ta.append(text_for_sentence_mining)


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


    def parse_tables(tables):
        for table in tables:
            for row in table.rows:
                for cell in row.cells:
                    texts = [text.strip() for text in cell.text.split('\n')]
                    [allocate_text(text, sentences_en, sentences_ms,
                                sentences_ta, sentences_zh) for text in texts if text]
                    if cell.tables:
                        parse_tables(cell.tables)


    parse_tables(wordDoc.tables)


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

    root_element = wordDoc.element
    textbox_elements = root_element.xpath('.//w:drawing//w:txbxContent')
    for textbox_element in textbox_elements:
        text = " ".join(" ".join(textbox_element.xpath(".//text()")).split())
        if text:
            allocate_text(text, sentences_en, sentences_ms,
                          sentences_ta, sentences_zh)

    print("sentences_en number:{}".format(len(sentences_en)))
    print("sentences_ms number:{}".format(len(sentences_ms)))
    print("sentences_ta number:{}".format(len(sentences_ta)))
    print("sentences_zh number:{}".format(len(sentences_zh)))

    with open('./sentences.en', 'w', encoding='utf8') as fOut:
        for sentence in sentences_en:
            fOut.write("{}\n".format(sentence.replace("|", " ")))

    with open('./sentences.zh', 'w', encoding='utf8') as fOut:
        for sentence in sentences_zh:
            fOut.write("{}\n".format(sentence.replace("|", " ")))

    with open('./sentences.ms', 'w', encoding='utf8') as fOut:
        for sentence in sentences_ms:
            fOut.write("{}\n".format(sentence.replace("|", " ")))

    with open('./sentences.ta', 'w', encoding='utf8') as fOut:
        for sentence in sentences_ta:
            fOut.write("{}\n".format(sentence.replace("|", " ")))


extract("LetterforSeniorsT.docx")

print("--- %s seconds ---" % (time.time() - start_time))
