import os
import re
import string
import time


def lang_detect(text_for_lang_detect):

    lang_detected = set()

    text_for_lang_detect = re.sub(
        "(?i)\w+@\S+\s?|http\S*\s?|www\.\S*\s?|[a-z\.]*\.sg\S*\s?|[0-9]+\s?", "", text_for_lang_detect)
    text_for_lang_detect = text_for_lang_detect.translate(
        str.maketrans('-', ' ', string.punctuation.replace('-', ''))).strip().lower()

    if text_for_lang_detect:
        if re.search('[\u4e00-\u9fff]', text_for_lang_detect):
            lang_detected.add('zh')
        if re.search('[\u0B80-\u0BFF]', text_for_lang_detect):
            lang_detected.add('ta')
        if re.search('[\u0400-\u04FF]', text_for_lang_detect):
            lang_detected.add('ru')
        if re.search('[\uac00-\ud7a3]', text_for_lang_detect):
            lang_detected.add('ko')
        if re.search('[\u3040-\u30ff\u31f0-\u31ff]', text_for_lang_detect):
            lang_detected.add('ja')
        if re.search('[\u0A00-\u0A7F]', text_for_lang_detect):
            lang_detected.add('pa')
        if re.search('[àáãạảăắằẳẵặâấầẩẫậèéẹẻẽêềếểễệđìíĩỉịòóõọỏôốồổỗộơớờởỡợùúũụủưứừửữựỳỵỷỹýÀÁÃẠẢĂẮẰẲẴẶÂẤẦẨẪẬÈÉẸẺẼÊỀẾỂỄỆĐÌÍĨỈỊÒÓÕỌỎÔỐỒỔỖỘƠỚỜỞỠỢÙÚŨỤỦƯỨỪỬỮỰỲỴỶỸÝ]', text_for_lang_detect):
            lang_detected.add('vi')

    return lang_detected


def other_lang_detect(text_for_lang_detect):

    other_lang_detected = False

    text_for_lang_detect = re.sub(
        "(?i)\w+@\S+\s?|http\S*\s?|www\.\S*\s?|[a-z\.]*\.sg\S*\s?|[0-9]+\s?", "", text_for_lang_detect)
    text_for_lang_detect = text_for_lang_detect.translate(
        str.maketrans('-', ' ', string.punctuation.replace('-', ''))).strip().lower()

    if re.search('[\u4e00-\u9fff\u0B80-\u0BFF\u0400-\u04FF\uac00-\ud7a3\u3040-\u30ff\u31f0-\u31ff\u0A00-\u0A7FàáãạảăắằẳẵặâấầẩẫậèéẹẻẽêềếểễệđìíĩỉịòóõọỏôốồổỗộơớờởỡợùúũụủưứừửữựỳỵỷỹýÀÁÃẠẢĂẮẰẲẴẶÂẤẦẨẪẬÈÉẸẺẼÊỀẾỂỄỆĐÌÍĨỈỊÒÓÕỌỎÔỐỒỔỖỘƠỚỜỞỠỢÙÚŨỤỦƯỨỪỬỮỰỲỴỶỸÝ]', text_for_lang_detect):
        other_lang_detected = True

    return other_lang_detected


def filter(file_path):
    start_time = time.time()
    with open(file_path) as fIN:
        list = []
        for line in fIN:
            en_sent = line.split('|')[1].strip()
            if not other_lang_detect(en_sent):
                list.append(line)
    with open(file_path, 'w', encoding='utf8') as fOUT:
        for sentence in list:
            fOUT.write(sentence)
    list.clear()
    print("finished " + file_path)
    print("--- %s seconds ---" % (time.time() - start_time))


if __name__ == '__main__':

    rootdir = '/home/xuanlong/dataclean/data'

    for root, dirs, files in os.walk(rootdir):
        for file in files:
            if os.path.splitext(file)[1] in {'.en-ta', '.en-zh', '.en-vi', '.en-ms', '.en-id'}:
                file_path = os.path.join(root, file)
                filter(file_path)
