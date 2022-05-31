import os
import re
import time
from simhash import Simhash, SimhashIndex


def load_words():
    with open('/home/xuanlong/dataclean/cleaning/dataclean_stage2/words_alpha.txt') as word_file:
        valid_words = set(word_file.read().split())

    return valid_words


english_words = load_words()


def fix_punctuations(sent):
    matches_to_split = re.findall(
        '[\)\:,?!][a-zA-Z\u4e00-\u9fff\u0B80-\u0BFF\u0400-\u04FF\uac00-\ud7a3\u3040-\u30ff\u31f0-\u31ff\u0A00-\u0A7FàáãạảăắằẳẵặâấầẩẫậèéẹẻẽêềếểễệđìíĩỉịòóõọỏôốồổỗộơớờởỡợùúũụủưứừửữựỳỵỷỹýÀÁÃẠẢĂẮẰẲẴẶÂẤẦẨẪẬÈÉẸẺẼÊỀẾỂỄỆĐÌÍĨỈỊÒÓÕỌỎÔỐỒỔỖỘƠỚỜỞỠỢÙÚŨỤỦƯỨỪỬỮỰỲỴỶỸÝ]', sent)
    for match in matches_to_split:
        sent = sent.replace(match, match[0]+' '+match[1])

    matches_to_conjunct = re.findall('\s+[:,.?!]', sent)
    for match in matches_to_conjunct:
        sent = sent.replace(match, match[-1])

    matches_to_conjunct = re.findall('\s+[：，。“”？！]|[：，。“”？！]\s+', sent)
    for match in matches_to_conjunct:
        sent = sent.replace(match, match.strip())

    return sent


def fix_serial_number(en_sent, non_en_sent):
    if en_sent[0] == non_en_sent[0]:
        if re.match('\d\s', en_sent) and re.match('\d\S', non_en_sent):
            non_en_sent = non_en_sent[:1]+' '+non_en_sent[1:]
        if re.match('\d\s', non_en_sent) and re.match('\d\S', en_sent):
            en_sent = en_sent[:1]+' '+en_sent[1:]
    return en_sent, non_en_sent


def fix_format(line):

    sentences = line.strip().split('|')

    score = sentences[0].strip()
    en_sent = sentences[1].strip()
    non_en_sent = sentences[2].strip()

    en_sent = ' '.join(re.sub(
        "[\x00-\x1f\x7f-\x9f]|[\ufffd\ufeff\u2000-\u200f\u2028-\u202f\u205f-\u206e]|^([a-zA-Z0-9]{1,3}\.|\(?[0-9]+\)|o)\s|^[\.#]{1,3}\s?|_+$|\\\\n|</?b>|[\^\*\↑√§¶†‡+‖▪●•·-]", "", en_sent, flags=re.I).strip().split())
    non_en_sent = ' '.join(re.sub(
        "[\x00-\x1f\x7f-\x9f]|[\ufffd\ufeff\u2000-\u200f\u2028-\u202f\u205f-\u206e]|^([a-zA-Z0-9]{1,3}\.|\(?[0-9]+\)|o)\s|^[\.#]{1,3}\s?|_+$|\\\\n|</?b>|[\^\*\↑√§¶†‡+‖▪●•·-]", "", non_en_sent, flags=re.I).strip().split())

    en_sent, non_en_sent = fix_serial_number(en_sent, non_en_sent)
    en_sent = fix_punctuations(en_sent)
    non_en_sent = fix_punctuations(non_en_sent)

    return score, en_sent, non_en_sent


def mis_spelling_detected(en_sent):

    non_en_words = [word for word in en_sent.split() if (
        not re.search('[^a-z]', word)) and (word not in english_words)]
    if non_en_words:
        return True
    return False


def emoji_detected(text_for_emoji_detect):

    if re.search('[\u1408\U0001F1E0-\U0001F1FF\U0001F300-\U0001F64F\U0001F680-\U0001FAFF\U00002702-\U000027B0]', text_for_emoji_detect):
        return True
    return False


def non_en_detected(text_for_non_en_detect):

    if re.search('[\u4e00-\u9fff\u0B80-\u0BFF\u0400-\u04FF\uac00-\ud7a3\u3040-\u30ff\u31f0-\u31ff\u0A00-\u0A7FàáãạảăắằẳẵặâấầẩẫậèéẹẻẽêềếểễệđìíĩỉịòóõọỏôốồổỗộơớờởỡợùúũụủưứừửữựỳỵỷỹýÀÁÃẠẢĂẮẰẲẴẶÂẤẦẨẪẬÈÉẸẺẼÊỀẾỂỄỆĐÌÍĨỈỊÒÓÕỌỎÔỐỒỔỖỘƠỚỜỞỠỢÙÚŨỤỦƯỨỪỬỮỰỲỴỶỸÝ]', text_for_non_en_detect):
        return True
    return False


def chaotic_detected(text_for_chaotic_detect):
    alphabetic_text = ''.join(
        re.sub('[^a-zA-Z]', '', text_for_chaotic_detect).split())
    if len(alphabetic_text)/len(text_for_chaotic_detect) < 0.7:
        return True
    return False


def similar_detected(i, en_sent, index):

    s = Simhash(en_sent)
    if index.near_dups_detected(s):
        return True

    index.add(i, s)
    return False


def is_filtered(i, line, index):

    sentences = line.strip().split('|')
    if len(sentences) != 3:
        return True

    en_sent = sentences[1].strip()
    non_en_sent = sentences[2].strip()

    if len(en_sent.split()) < 10:
        return True
    if mis_spelling_detected(en_sent):
        return True
    if chaotic_detected(en_sent):
        return True
    if non_en_detected(en_sent):
        return True
    if emoji_detected(line):
        return True
    if similar_detected(i, en_sent, index):
        return True
    if len(re.findall(':', en_sent, re.I)) != len(re.findall(':', non_en_sent, re.I)):
        return True
    if len(re.findall('\)', en_sent, re.I)) != len(re.findall('\)', non_en_sent, re.I)):
        return True
    if len(re.findall('@', en_sent, re.I)) != len(re.findall('@', non_en_sent, re.I)):
        return True
    if len(re.findall('#', en_sent, re.I)) != len(re.findall('#', non_en_sent, re.I)):
        return True

    return False


def filter_and_fix(file_path):

    print("start " + file_path, flush=True)

    with open(file_path) as fIN, \
            open(file_path + '.filtered', 'a', encoding='utf8') as fOUT:
        index = SimhashIndex([], k=15)
        for (i, line) in enumerate(fIN):
            if (i+1) % 10000 == 0:
                index = SimhashIndex([], k=15)
            if is_filtered(i, line, index):
                continue
            score, en_sent, non_en_sent = fix_format(line)
            fOUT.write("{} | {} | {}\n".format(score, en_sent, non_en_sent))


    print("finished " + file_path, flush=True)


def main(rootdir):
    for root, dirs, files in os.walk(rootdir):
        for file in files:
            if os.path.splitext(file)[1] in {'.en-ta', '.en-zh', '.en-vi', '.en-ms', '.en-id'}:
                file_path = os.path.join(root, file)
                filter_and_fix(file_path)


if __name__ == '__main__':
    start_time = time.time()
    rootdir = '/home/xuanlong/dataclean/data/parallel/en-ms'
    main(rootdir)
    print("--- %s seconds ---" % (time.time() - start_time), flush=True)
