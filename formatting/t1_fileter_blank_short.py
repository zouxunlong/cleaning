import os
import re
import string
import time


def non_en_detect(text_for_lang_detect):

    other_lang_detected = False

    text_for_lang_detect = re.sub(
        "(?i)\w+@\S+\s?|http\S*\s?|www\.\S*\s?|[a-z\.]*\.sg\S*\s?|[0-9]+\s?", "", text_for_lang_detect)
    text_for_lang_detect = text_for_lang_detect.translate(
        str.maketrans('-', ' ', string.punctuation.replace('-', ''))).strip().lower()

    if re.search('[\u4e00-\u9fff\u0B80-\u0BFF\u0400-\u04FF\uac00-\ud7a3\u3040-\u30ff\u31f0-\u31ff\u0A00-\u0A7FàáãạảăắằẳẵặâấầẩẫậèéẹẻẽêềếểễệđìíĩỉịòóõọỏôốồổỗộơớờởỡợùúũụủưứừửữựỳỵỷỹýÀÁÃẠẢĂẮẰẲẴẶÂẤẦẨẪẬÈÉẸẺẼÊỀẾỂỄỆĐÌÍĨỈỊÒÓÕỌỎÔỐỒỔỖỘƠỚỜỞỠỢÙÚŨỤỦƯỨỪỬỮỰỲỴỶỸÝ]', text_for_lang_detect):
        other_lang_detected = True

    return other_lang_detected


def filter(file_path):
    with open(file_path) as fIN,open(file_path + '.filtered', 'w', encoding='utf8') as fOUT:
        for line in fIN:
            sentences = line.strip().split('|')
            if len(sentences) < 2:
                continue

            en_sent = ' '.join(re.sub("(?i)<Phone Icon>|<Stopwatch>|<br>|<Red>|<Orange>|^[a-zA-Z0-9]{1,3}\.\s|^[\*▪●•·-]{1,3}\s?|^\(?[0-9]\)\s?|_+$|\\\\n|</?b>", " ", sentences[0].strip()).strip().split())
            non_en_sent = ' '.join(re.sub("(?i)<Phone Icon>|<Stopwatch>|<br>|<Red>|<Orange>|^[a-zA-Z0-9]{1,3}\.\s|^[\*▪●•·-]{1,3}\s?|^\(?[0-9]\)\s?|_+$|\\\\n|</?b>", " ", sentences[-1].strip()).strip().split())

            if non_en_detect(en_sent):
                continue
            if len(en_sent) < 10:
                continue
            if len(non_en_sent) < 3:
                continue
            fOUT.write("{} | {}\n".format(en_sent, non_en_sent))
    print("finished " + file_path)


def main(rootdir):
    for root, dirs, files in os.walk(rootdir):
        for file in files:
            if os.path.splitext(file)[1] in {'.en-ta', '.en-zh', '.en-vi', '.en-ms', '.en-id'}:
                file_path = os.path.join(root, file)
                filter(file_path)


if __name__ == '__main__':
    start_time = time.time()
    rootdir = '/home/xuanlong/dataclean/data/MCI_combined'
    main(rootdir)
    print("--- %s seconds ---" % (time.time() - start_time))
