import re
import string
import sys
import time
import pycld2 as cld2
import cld3
import fasttext


model_fasttext = fasttext.load_model('../model/lid.176.bin')

punctuation = r"""!"\#$%&'()*+,-./:;<=>?@[]^_`{|}~，。、‘’“”：；【】·！￥★…《》？！（）—"""
punctuation2none_dict = str.maketrans('', '', punctuation)
pattern_punctuation = r"""[!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~，。、‘’“”：；【】·！￥★…《》？！（）—]"""
pattern_url = r"[(http(s)?):\/\/(www\.)?a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,6}\b([-a-zA-Z0-9@:%_\+.~#?&//=]*)"
pattern_email = r"[\w\-\.]+@([\w\-]+\.)+[\w\-]{2,4}"


def chaotic_detected(text_for_chaotic_detect):
    alphabetic_text = ''.join(
        re.sub('[^a-zA-Z]', '', text_for_chaotic_detect).split())
    if len(alphabetic_text)/len(text_for_chaotic_detect) < 0.6:
        return True
    return False


def wrong_language_detect(text_for_lang_detect, lang):

    if re.search('[^{}]'.format(string.printable), text_for_lang_detect):
        return True

    try:
        lang_by_cld2 = cld2.detect(text_for_lang_detect)[2][0][1]
        lang_by_cld3 = cld3.get_language(text_for_lang_detect)[0]
        lang_by_fasttext = model_fasttext.predict(
            text_for_lang_detect)[0][0][-2:]

        if not {lang} & {lang_by_cld2, lang_by_cld3, lang_by_fasttext}:
            return True

    except Exception as err:
        exception_type, exception_object, exception_traceback = sys.exc_info()
        filename = exception_traceback.tb_frame.f_code.co_filename
        line_number = exception_traceback.tb_lineno

        print("Exception type: ", exception_type, flush=True)
        print("File name: ", filename, flush=True)
        print("Line number: ", line_number, flush=True)
        print(err)

    return False


def is_filtered(sentence_en, non_en_sent, lang_src, lang_tgt):
    if len(sentence_en) < 2:
        return True
    if len(non_en_sent) < 2:
        return True
    if len(sentence_en.split()) < 4:
        return True
    if len(re.findall(':', sentence_en, re.I)) != len(re.findall(':', non_en_sent, re.I)):
        return True
    if len(re.findall('\/', sentence_en, re.I)) != len(re.findall('\/', non_en_sent, re.I)):
        return True
    if len(re.findall(r'\\', sentence_en, re.I)) != len(re.findall(r'\\', non_en_sent, re.I)):
        return True
    if len(re.findall('@', sentence_en, re.I)) != len(re.findall('@', non_en_sent, re.I)):
        return True
    if len(re.findall('#', sentence_en, re.I)) != len(re.findall('#', non_en_sent, re.I)):
        return True
    if chaotic_detected(sentence_en):
        return True
    if wrong_language_detect(sentence_en, lang_src):
        return True
    if wrong_language_detect(non_en_sent, lang_tgt):
        return True
    if sentence_en.translate(punctuation2none_dict).lower().split() == non_en_sent.translate(punctuation2none_dict).lower().split():
        return True
    return False


def main():
    start_time = time.time()
    with open('/home/xuanlong/dataclean/data/Total/train.en', 'r', encoding='utf8') as f_in_en, \
            open('/home/xuanlong/dataclean/data/Total/train.id', 'r', encoding='utf8') as f_in_id, \
            open('/home/xuanlong/dataclean/data/Total/train.filtered.en', 'w', encoding='utf8') as f_out_en, \
            open('/home/xuanlong/dataclean/data/Total/train.filtered.id', 'w', encoding='utf8') as f_out_id:
        for (i, sentence_en), (j, sentence_id) in zip(enumerate(f_in_en), enumerate(f_in_id)):
            if is_filtered(sentence_en.strip(), sentence_id.strip(), 'en', 'id'):
                continue
            f_out_en.write(sentence_en)
            f_out_id.write(sentence_id)
    print("--- %s seconds ---" % (time.time() - start_time), flush=True)


if __name__ == '__main__':
    main()
