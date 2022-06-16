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
from googletrans import Translator
from bi_text_miner import Bi_text_miner
from file_convert import doc_to_docx, rtf_to_docx
from combine_files import combine_files_in_dir
os.environ["TOKENIZERS_PARALLELISM"] = "false"

translator = Translator()
bi_text_miner = Bi_text_miner(knn_neighbors=6, min_matching_score=1.06, min_cos_sim=0.7,
                              model_path_or_name='../model/labse_bert_model', sort_by_cos=False)


def get_paragraph_runs(paragraph):
    def _get(node, parent):
        for child in node:
            if child.tag == qn('w:r'):
                yield Run(child, parent)
            if child.tag == qn('w:hyperlink'):
                yield from _get(child, parent)
    return list(_get(paragraph._element, paragraph))


Paragraph.runs = property(lambda self: get_paragraph_runs(self))
model_fasttext = fasttext.load_model('../model/lid.176.bin')


def lang_detect(text_for_lang_detect):

    if re.search('[\u4e00-\u9fff]', text_for_lang_detect):
        lang_detected = 'zh'
    elif re.search('[\u0B80-\u0BFF]', text_for_lang_detect):
        lang_detected = 'ta'
    else:
        try:
            lang_by_cld2 = cld2.detect(text_for_lang_detect)[2][0][1]
            lang_by_cld3 = cld3.get_language(text_for_lang_detect)[0]
            lang_by_fasttext = model_fasttext.predict(
                text_for_lang_detect)[0][0][-2:]

            if {"en", "ms", "id"} & {lang_by_cld2, lang_by_cld3, lang_by_fasttext}:
                if 'en' in [lang_by_cld2, lang_by_cld3, lang_by_fasttext]:
                    lang_detected = 'en'
                elif {'ms', 'id'} & {lang_by_cld2, lang_by_cld3, lang_by_fasttext}:
                    lang_detected = 'ms'
            else:
                lang_by_google = translator.detect(
                    text_for_lang_detect).lang[:2]
                lang_detected = lang_by_google
        except:
            lang_detected = 'un'
    return lang_detected


def allocate_text_by_lang(texts):

    texts_en = []
    texts_ms = []
    texts_zh = []
    texts_ta = []
    lang_detected = ""
    for text in texts:

        text = re.sub("^[a-zA-Z]?\.\s?|^[0-9]{0,2}\.\s?", "", text).strip()
        text_without_punctuation = text.translate(
            str.maketrans('', '', string.punctuation)).strip().lower()

        text_without_email_url_number = re.sub(
            "(?i)\w+@\S+\s?|http\S*\s?|www\.\S*\s?|[a-z\.]*\.sg\S*\s?|[0-9]+\s?", "", text)
        text_for_lang_detect = text_without_email_url_number.translate(
            str.maketrans('-', ' ', string.punctuation.replace('-', ''))).strip().lower()

        if text_for_lang_detect:
            lang_detected = lang_detect(text_for_lang_detect)

        if text_without_punctuation:
            if lang_detected == "en":
                texts_en.append(text)
            elif lang_detected == "ms":
                texts_ms.append(text)
            elif lang_detected == "zh":
                texts_zh.append(text.replace(" ", ""))
            elif lang_detected == "ta":
                texts_ta.append(text)

    return {'en': texts_en, 'ms': texts_ms, 'zh': texts_zh, 'ta': texts_ta}


def texts_from_tables(tables):
    def yield_texts(_tables):
        for table in _tables:
            for column in table.columns:
                for cell in column.cells:
                    texts = [text.strip() for text in cell.text.split('\n')]
                    for text in texts:
                        yield text
                    if cell.tables:
                        yield from yield_texts(cell.tables)
    return [text for text in list(yield_texts(tables)) if text]


def texts_from_paragraphs(paragraphs):
    texts = [text.strip() for p in paragraphs for text in p.text.split('\n')]
    return [text for text in texts if text]


def texts_from_textboxs(root_element):
    textbox_elements = root_element.xpath('.//w:drawing//w:txbxContent')
    texts = [" ".join(" ".join(textbox_element.xpath(".//text()")).split())
             for textbox_element in textbox_elements]
    return [text for text in texts if text]


def extend_texts_from_docx(docx_path, texts):

    wordDoc = Document(docx_path)
    for section in wordDoc.sections:
        header = section.header
        footer = section.footer
        texts.extend(texts_from_paragraphs(header.paragraphs))
        texts.extend(texts_from_paragraphs(footer.paragraphs))
    texts.extend(texts_from_tables(wordDoc.tables))
    texts.extend(texts_from_paragraphs(wordDoc.paragraphs))
    texts.extend(texts_from_textboxs(wordDoc.element))


def extend_texts_from_file(file_path, texts):

    if file.endswith('.doc'):
        returncode = doc_to_docx(file_path)
        if returncode == 0:
            extend_texts_from_docx(
                os.path.splitext(file_path)[0]+'.docx', texts)
        else:
            raise Exception("doc file convert to docx failed")
    elif file.endswith('.rtf'):
        returncode = rtf_to_docx(file_path)
        if returncode == 0:
            extend_texts_from_docx(
                os.path.splitext(file_path)[0]+'.docx', texts)
        else:
            raise Exception("rtf file convert to docx failed")
    elif file.endswith('.docx'):
        extend_texts_from_docx(file_path, texts)


rootdir = '/home/zxl/ssd/WORK/data_clean/data/redo'


for root, dirs, files in os.walk(rootdir):
    files.sort()
    texts = []
    for i, file in enumerate(files):

        file_path = os.path.join(root, file)

        extend_texts_from_file(file_path, texts)

        if i+1 < len(files) and os.path.splitext(file)[0][:-1].replace(' ', '') == os.path.splitext(files[i+1])[0][:-1].replace(' ', ''):
            continue

        if texts:
            text_list_dict = allocate_text_by_lang(texts)
            text_set_dict = bi_text_miner.list_to_set(text_list_dict)
            en_zh_sentence_pair = bi_text_miner.sentence_matching(
                text_set_dict['en'], text_set_dict['zh'])
            en_ms_sentence_pair = bi_text_miner.sentence_matching(
                text_set_dict['en'], text_set_dict['ms'])
            en_ta_sentence_pair = bi_text_miner.sentence_matching(
                text_set_dict['en'], text_set_dict['ta'])

            with open(os.path.splitext(file_path)[0]+'.en-zh', 'w', encoding='utf8') as fOut:
                for sentence_pair in en_zh_sentence_pair:
                    fOut.write("{} | {}\n".format(
                        sentence_pair[0], sentence_pair[1]))

            with open(os.path.splitext(file_path)[0]+'.en-ms', 'w', encoding='utf8') as fOut:
                for sentence_pair in en_ms_sentence_pair:
                    fOut.write("{} | {}\n".format(
                        sentence_pair[0], sentence_pair[1]))

            with open(os.path.splitext(file_path)[0]+'.en-ta', 'w', encoding='utf8') as fOut:
                for sentence_pair in en_ta_sentence_pair:
                    fOut.write("{} | {}\n".format(
                        sentence_pair[0], sentence_pair[1]))

            print(file_path)
            print('en_zh_sentence_pair number:{}'.format(
                len(en_zh_sentence_pair)))
            print('en_ms_sentence_pair number:{}'.format(
                len(en_ms_sentence_pair)))
            print('en_ta_sentence_pair number:{}'.format(
                len(en_ta_sentence_pair)))

            texts.clear()


print('finished translated sentences mining')


combine_files_in_dir(rootdir)
