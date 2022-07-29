from pathlib import Path
import plac
import re
from docx import Document
from docx import Document
from docx.oxml.shared import qn
from docx.text.paragraph import Paragraph
from docx.text.run import Run, _Text


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


pattern_punctuation = r"""[!?,.:;"#$£€%&'()+-_/<≤=≠≥>@[\]^{|}，。、—‘’“”：；【】￥…《》？！（）]"""
pattern_arabic = r"[\u0600-\u06FF]"
pattern_chinese = r"[\u4e00-\u9fff]"
pattern_tamil = r"[\u0B80-\u0BFF]"
pattern_russian = r"[\u0400-\u04FF]"
pattern_korean = r"[\uac00-\ud7a3]"
pattern_japanese = r"[\u3040-\u30ff\u31f0-\u31ff]"
pattern_vietnamese = r"[àáãạảăắằẳẵặâấầẩẫậèéẹẻẽêềếểễệđìíĩỉịòóõọỏôốồổỗộơớờởỡợùúũụủưứừửữựỳỵỷỹýÀÁÃẠẢĂẮẰẲẴẶÂẤẦẨẪẬÈÉẸẺẼÊỀẾỂỄỆĐÌÍĨỈỊÒÓÕỌỎÔỐỒỔỖỘƠỚỜỞỠỢÙÚŨỤỦƯỨỪỬỮỰỲỴỶỸÝ]"
pattern_emoji = r'[\U0001F1E0-\U0001F1FF\U0001F300-\U0001F64F\U0001F680-\U0001FAFF\U00002702-\U000027B0]'


def extract_texts(docx_path):

    if not str(docx_path).endswith('.docx'):
        return []

    wordDoc = Document(docx_path)
    items = get_all_paragraphs(wordDoc)
    for section in wordDoc.sections:
        header = section.header
        footer = section.footer
        items += get_all_paragraphs(header)
        items += get_all_paragraphs(footer)

    texts = [
        re.sub(
            r'[^a-zA-Z0-9\s\t{}{}{}{}{}{}{}{}{}]'.format(
                pattern_punctuation[1:-1],
                pattern_arabic[1:-1],
                pattern_chinese[1:-1],
                pattern_tamil[1:-1],
                pattern_russian[1:-1],
                pattern_korean[1:-1],
                pattern_japanese[1:-1],
                pattern_vietnamese[1:-1],
                pattern_emoji[1:-1],
            ), ' ', item.text.strip()).strip()
        for item in items if item.text.strip()]

    texts = [
        re.sub(
            r'^([0-9i]{1,3}\.)([^0-9])',
            '\\2',
            ' '.join(text.split())
        ).replace('|||', ' ').strip()
        for text in texts if text.strip()]

    additional_texts = set()

    for text in texts:
        if re.search(r'[\(\[（【】）\]\)]', text):
            # find all Brackets content and the words sequence in front of Brackets,
            # return format: ('words sequence','word infront','Brackets content')
            results = re.findall(
                r'(?=((\s[^\s】）\]\)]+){2,8})\s?[\(\[（【](.+?)[】）\]\)])', text)
            results2 = re.findall(
                r'(?=(^[^\(\[（【】）\]\)]+)\s?[\(\[（【](.+?)[】）\]\)])', text)
            for tuple in results:
                additional_texts.update(tuple)
            for tuple in results2:
                additional_texts.update(tuple)

    texts.extend([text.strip() for text in additional_texts if text.strip()])

    return texts


