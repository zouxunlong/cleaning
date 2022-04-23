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


def allocate_text_by_lang(texts):
    texts_en = []
    texts_ms = []
    texts_zh = []
    texts_ta = []

    for text in texts:

        trimed_text = re.sub(
            "\w+@\S+\s?|http\S*\s?|www\.\S*\s?|[0-9]|\{[\s\S]*\}", "", text)

        text_for_lang_detect = trimed_text.translate(
            str.maketrans('', '', string.punctuation)).strip().lower()

        if text_for_lang_detect:

            text = re.sub("^[a-zA-Z0-9]+\.\s", "", text)

            lang_by_cld2 = cld2.detect(text_for_lang_detect)[2][0][1]
            lang_by_cld3 = cld3.get_language(text_for_lang_detect)
            lang_by_fasttext = model_fasttext.predict(
                text_for_lang_detect)[0][0]

            if lang_by_cld2 == "en" or lang_by_fasttext == "__label__en":
                texts_en.append(text)
            elif lang_by_cld2 in ["ms", "id"] or lang_by_fasttext in ["__label__ms", "__label__id"] or lang_by_cld3[0] in ["ms"]:
                texts_ms.append(text)
            elif lang_by_cld2 in ["zh", "ja"] or lang_by_fasttext in ["__label__zh", "__label__ja"]:
                text = text.replace(" ", "")
                texts_zh.append(text)
            elif lang_by_cld2 == "ta" or lang_by_fasttext == "__label__ta":
                texts_ta.append(text)

    return texts_en, texts_ms, texts_zh, texts_ta


def texts_from_tables(tables):
    def yield_texts(_tables):
        for table in _tables:
            for row in table.rows:
                for cell in row.cells:
                    texts = [text.strip() for text in cell.text.split('\n')]
                    for text in texts:
                        yield text
                    if cell.tables:
                        yield_texts(cell.tables)
    return list(yield_texts(tables))


def texts_from_paragraphs(paragraphs):
    texts = [text.strip() for text in p.text.split('\n') for p in paragraphs]
    return texts


def texts_from_textboxs(root_element):
    textbox_elements = root_element.xpath('.//w:drawing//w:txbxContent')
    texts = [" ".join(" ".join(textbox_element.xpath(".//text()")).split())
             for textbox_element in textbox_elements]
    return texts


def extract(filepath):
    wordDoc = Document(filepath)

    texts = []

    texts.append(texts_from_tables(wordDoc.tables))
    texts.append(texts_from_paragraphs(wordDoc.paragraphs))

    for section in wordDoc.sections:
        header = section.header
        footer = section.footer
        texts.append(texts_from_paragraphs(header.paragraphs))
        texts.append(texts_from_paragraphs(footer.paragraphs))

    texts.append(texts_from_textboxs(wordDoc.element))

    texts_en, texts_ms, texts_zh, texts_ta = allocate_text_by_lang(texts)

    print("sentences_en number:{}".format(len(sentences_en)))
    print("sentences_ms number:{}".format(len(sentences_ms)))
    print("sentences_ta number:{}".format(len(sentences_ta)))
    print("sentences_zh number:{}".format(len(sentences_zh)))

    with open('./sentences.en', 'w', encoding='utf8') as fOut:
        for sentence in texts_en:
            fOut.write("{}\n".format(sentence.replace("|", " ")))

    with open('./sentences.zh', 'w', encoding='utf8') as fOut:
        for sentence in texts_zh:
            fOut.write("{}\n".format(sentence.replace("|", " ")))

    with open('./sentences.ms', 'w', encoding='utf8') as fOut:
        for sentence in texts_ms:
            fOut.write("{}\n".format(sentence.replace("|", " ")))

    with open('./sentences.ta', 'w', encoding='utf8') as fOut:
        for sentence in texts_ta:
            fOut.write("{}\n".format(sentence.replace("|", " ")))


extract("LetterforSeniorsT.docx")

print("--- %s seconds ---" % (time.time() - start_time))
