import sys
import pycld2 as cld2
import cld3
import fasttext
from docx import Document
import os
import re
import string
from docx import Document
from docx.oxml.shared import qn
from docx.text.paragraph import Paragraph
from docx.text.run import Run, _Text
from googletrans import Translator
from bi_text_miner import Bi_text_miner
from file_convert import doc2docx, rtf2docx
from combine_files import combine_files_in_dir
os.environ["TOKENIZERS_PARALLELISM"] = "false"

translator = Translator()
bi_text_miner = Bi_text_miner(knn_neighbors=6, min_matching_score=0.99, min_cos_sim=0.65,
                              model_path_or_name='../model/labse_bert_model', sort_by_cos=False)

model_fasttext = fasttext.load_model('../model/lid.176.bin')


punctuation = r"""!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~，。、‘’“”：；【】·！￥★…《》？！（）—"""
pattern_punctuation = r"""[!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~，。、‘’“”：；【】·！￥★…《》？！（）—]"""
pattern_url = r"[(http(s)?):\/\/(www\.)?a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,6}\b([-a-zA-Z0-9@:%_\+.~#?&//=]*)"
pattern_email = r"[\w\-\.]+@([\w\-]+\.)+[\w\-]{2,4}"
pattern_arabic = r"[\u0600-\u06FF]"
pattern_chinese = r"[\u4e00-\u9fff]"
pattern_tamil = r"[\u0B80-\u0BFF]"
pattern_russian = r"[\u0400-\u04FF]"
pattern_korean = r"[\uac00-\ud7a3]"
pattern_japanese = r"[\u3040-\u30ff\u31f0-\u31ff]"
pattern_vietnamese = r"[àáãạảăắằẳẵặâấầẩẫậèéẹẻẽêềếểễệđìíĩỉịòóõọỏôốồổỗộơớờởỡợùúũụủưứừửữựỳỵỷỹýÀÁÃẠẢĂẮẰẲẴẶÂẤẦẨẪẬÈÉẸẺẼÊỀẾỂỄỆĐÌÍĨỈỊÒÓÕỌỎÔỐỒỔỖỘƠỚỜỞỠỢÙÚŨỤỦƯỨỪỬỮỰỲỴỶỸÝ]"


def lang_detect(text_for_lang_detect):

    lang_detected = set()

    text_for_lang_detect = ' '.join(re.sub("{}|{}|{}".format(
        pattern_url, pattern_email, pattern_punctuation), " ", text_for_lang_detect, 0, re.I).split()).strip().lower()

    if text_for_lang_detect:
        if re.search(pattern_arabic, text_for_lang_detect):
            lang_detected.add('ar')
        if re.search(pattern_chinese, text_for_lang_detect):
            lang_detected.add('zh')
        if re.search(pattern_tamil, text_for_lang_detect):
            lang_detected.add('ta')
        if re.search(pattern_russian, text_for_lang_detect):
            lang_detected.add('ru')
        if re.search(pattern_korean, text_for_lang_detect):
            lang_detected.add('ko')
        if re.search(pattern_japanese, text_for_lang_detect):
            lang_detected.add('ja')
        if re.search(pattern_vietnamese, text_for_lang_detect):
            lang_detected.add('vi')

        try:
            lang_by_cld2 = cld2.detect(text_for_lang_detect)[2][0][1]
            lang_by_cld3 = cld3.get_language(text_for_lang_detect)[0]
            lang_by_fasttext = model_fasttext.predict(
                text_for_lang_detect)[0][0][-2:]

            if {"en"} & {lang_by_cld2, lang_by_cld3, lang_by_fasttext}:
                lang_detected.add('en')
            if {'ms'} & {lang_by_cld2, lang_by_cld3, lang_by_fasttext}:
                lang_detected.add('ms')
            if {'id'} & {lang_by_cld2, lang_by_cld3, lang_by_fasttext}:
                lang_detected.add('id')
            if {'th'} & {lang_by_cld2, lang_by_cld3, lang_by_fasttext}:
                lang_detected.add('th')
            if {'vi'} & {lang_by_cld2, lang_by_cld3, lang_by_fasttext}:
                lang_detected.add('vi')

            # if len(lang_detected)==0:
            #     lang_by_google = translator.detect(
            #         text_for_lang_detect).lang[:2]
            #     if lang_by_google in ['zh','ms','ta','en','th','vi']:
            #         lang_detected.add(lang_by_google)

        except Exception as err:
            exception_type, exception_object, exception_traceback = sys.exc_info()
            filename = exception_traceback.tb_frame.f_code.co_filename
            line_number = exception_traceback.tb_lineno

            print("text_for_lang_detect: ", text_for_lang_detect, flush=True)
            print("Exception type: ", exception_type, flush=True)
            print("File name: ", filename, flush=True)
            print("Line number: ", line_number, flush=True)
            print(err)

    return lang_detected


def allocate_text_by_lang(texts):

    texts_en = []
    texts_ms = []
    texts_zh = []
    texts_ta = []
    lang_detected = set()
    for text in texts:
        lang_detecting=lang_detect(text)
        if len(lang_detecting)!=0:
            lang_detected = lang_detecting

        if {"en"} & lang_detected:
            texts_en.append(text)
        elif {"id", "ms"} & lang_detected:
            texts_ms.append(text)
        elif {"zh"} & lang_detected:
            texts_zh.append(text.replace(" ", ""))
        elif {"ta"} & lang_detected:
            texts_ta.append(text)

    return {'en': texts_en, 'ms': texts_ms, 'zh': texts_zh, 'ta': texts_ta}


def get_all_texts(node):
    def _get(node):
        for child in node:
            if child.tag == qn('w:t'):
                yield _Text(child)._t
            yield from _get(child)
    return list(_get(node._element))


def get_all_runs(node):
    def _get(node):
        for child in node:
            if child.tag == qn('w:r'):
                yield Run(child, node)
            yield from _get(child)
    return list(_get(node._element))


def get_all_paragraphs(node):
    def _get(node):
        for child in node:
            if child.tag == qn('w:p'):
                yield Paragraph(child, node)
            yield from _get(child)
    return list(_get(node._element))


def get_paragraph_runs(paragraph):
    def _get(node):
        for child in node:
            if not (child.tag == qn('w:drawing') or child.tag == qn('w:pict')):
                if child.tag == qn('w:r'):
                    yield Run(child, node)
                yield from _get(child)
    return list(_get(paragraph._element))


def get_paragraph_text(paragraph):
    text = ''
    for run in paragraph.runs:
        text += run.text
    return text


def set_paragraph_text(paragraph, text):
    runs = paragraph.runs
    for run in runs:
        if run.text.strip():
            run._r.getparent().remove(run._r)
    for child in paragraph._element:
        if child.tag == qn('w:hyperlink'):
            if len(child) == 0:
                child.getparent().remove(child)
    paragraph.add_run(text)


Paragraph.runs = property(fget=lambda self: get_paragraph_runs(self))
Paragraph.text = property(fget=lambda self: get_paragraph_text(self),
                          fset=lambda self, text: set_paragraph_text(self, text))


def extend_texts_from_docx(docx_path, texts):

    wordDoc = Document(docx_path)
    items = get_all_paragraphs(wordDoc)
    for section in wordDoc.sections:
        header = section.header
        footer = section.footer
        items += get_all_paragraphs(header)
        items += get_all_paragraphs(footer)

    texts.extend([' '.join(item.text.split('\n')) for item in items if item.text.strip()])


def extend_texts_from_file(file_path, texts):

    if file.endswith('.doc'):
        returncode = doc2docx(file_path)
        if returncode == 0:
            extend_texts_from_docx(
                os.path.splitext(file_path)[0]+'.docx', texts)
        else:
            raise Exception("doc file convert to docx failed")
    elif file.endswith('.rtf'):
        returncode = rtf2docx(file_path)
        if returncode == 0:
            extend_texts_from_docx(
                os.path.splitext(file_path)[0]+'.docx', texts)
        else:
            raise Exception("rtf file convert to docx failed")
    elif file.endswith('.docx'):
        extend_texts_from_docx(file_path, texts)


rootdir = '/home/xuanlong/dataclean/data/en_ms/From Agencies'


for root, dirs, files in os.walk(rootdir):
    files.sort()
    texts = []
    for i, file in enumerate(files):

        file_path = os.path.join(root, file)

        if file_path.endswith('.docx'):
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
                    fOut.write("{} ||| {}\n".format(
                        sentence_pair[0], sentence_pair[1]))

            with open(os.path.splitext(file_path)[0]+'.en-ms', 'w', encoding='utf8') as fOut:
                for sentence_pair in en_ms_sentence_pair:
                    fOut.write("{} ||| {}\n".format(
                        sentence_pair[0], sentence_pair[1]))

            with open(os.path.splitext(file_path)[0]+'.en-ta', 'w', encoding='utf8') as fOut:
                for sentence_pair in en_ta_sentence_pair:
                    fOut.write("{} ||| {}\n".format(
                        sentence_pair[0], sentence_pair[1]))

            print(file_path,flush=True)
            print('en_zh_sentence_pair number:{}'.format(
                len(en_zh_sentence_pair)),flush=True)
            print('en_ms_sentence_pair number:{}'.format(
                len(en_ms_sentence_pair)),flush=True)
            print('en_ta_sentence_pair number:{}'.format(
                len(en_ta_sentence_pair)),flush=True)

            texts.clear()


print('finished translated sentences mining',flush=True)


# combine_files_in_dir(rootdir)
