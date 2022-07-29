import re
import sys
import pycld2 as cld2
import cld3
import fasttext


model_fasttext = fasttext.load_model('../model/lid.176.bin')


punctuation = r"""!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~，。、‘’“”：；【】·！￥★…《》？！（）—"""
pattern_punctuation = r"""[!?,.:;"#$£€%&'()+-/<≤=≠≥>@[\]^_{|}，。、—‘’“”：；【】￥…《》？！（）]"""
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
            if {'vi'} & {lang_by_cld2, lang_by_cld3, lang_by_fasttext}:
                lang_detected.add('vi')

        except Exception as err:
            exception_type, exception_object, exception_traceback = sys.exc_info()
            filename = exception_traceback.tb_frame.f_code.co_filename
            line_number = exception_traceback.tb_lineno

            print("Exception type: ", exception_type, flush=True)
            print("File name: ", filename, flush=True)
            print("Line number: ", line_number, flush=True)
            print(err)

    return lang_detected
