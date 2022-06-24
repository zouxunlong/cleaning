import os
import re
import string
import time
import plac
from pathlib import Path


def load_words():
    with open('/home/xuanlong/dataclean/cleaning/dataclean/words_alpha.txt') as word_file:
        valid_words = set(word_file.read().split())
    return valid_words


english_words = load_words()

punctuation = r"""!"\#$%&'()*+,-./:;<=>?@[]^_`{|}~，。、‘’“”：；【】·！￥★…《》？！（）—"""
punctuation2none_dict = str.maketrans('', '', punctuation)
pattern_punctuation = """[!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~，。、‘’“”：；【】·！￥★…《》？！（）—]"""
pattern_url = r"[(http(s)?):\/\/(www\.)?a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,6}\b([-a-zA-Z0-9@:%_\+.~#?&//=]*)"
pattern_email = r"[\w\-\.]+@([\w\-]+\.)+[\w\-]{2,4}"
pattern_html = r"""<("[^"]*"|'[^']*'|[^'">])*>"""
pattern_special_charactors = r"[\x00-\x08\x0a-\x1f\x7f-\x9f\xa0]|[\ufffd\ufeff\u2000-\u200f\u2028-\u202f\u205f-\u206e]|[\↑√§¶†‡‖▪●•·]"
pattern_emoji = r'[\U0001F1E0-\U0001F1FF\U0001F300-\U0001F64F\U0001F680-\U0001FAFF\U00002702-\U000027B0]'
pattern_informal = r'[@#\\]|([^\w]|^)(http|https|www|com|hey|guy|kind\sof|ok|okay|oh|dude|we|you|your|my|me|ha|haha|i)([^\w]|$)|\'(s|ve|re|t|m|ll|d|am|)\s|-\s'
pattern_I = r'I\s|([^\w]|$)us([^\w]|$)'


def mis_spelling_detected(en_sent):
    non_en_words = [word for word in en_sent.split() if (
        not re.search('[^a-z]', word)) and (word not in english_words)]
    if non_en_words:
        return True
    return False


def emoji_detected(text_for_detect):
    if re.search(pattern_emoji, text_for_detect):
        return True
    return False


def informal_detected(text_for_detect):
    if re.search(pattern_informal, text_for_detect, re.I):
        return True
    if re.search(pattern_I, text_for_detect):
        return True
    return False


def unprintable_detected(text_for_detect):
    if re.search('[^{}]'.format(string.printable), text_for_detect, re.I):
        return True
    return False


def short_detected(text_for_detect):
    sub_strings = re.split(pattern_punctuation, text_for_detect)
    if max([len(substring.split()) for substring in sub_strings]) < 7:
        return True
    return False


def chaotic_detected(text_for_chaotic_detect):
    alphabetic_text = re.sub('[^a-zA-Z]', '', text_for_chaotic_detect)
    if len(alphabetic_text)/len(text_for_chaotic_detect) < 0.5:
        return True
    return False


def is_filtered(sentence_src, sentence_tgt):

    if short_detected(sentence_src):
        return True

    if informal_detected(sentence_src):
        return True

    if mis_spelling_detected(sentence_src):
        return True

    if unprintable_detected(sentence_src):
        return True

    if emoji_detected(sentence_src+' '+sentence_tgt):
        return True

    if re.search(pattern_special_charactors, sentence_src+' '+sentence_tgt, re.I):
        return True

    if len(re.findall('\/', sentence_src, re.I)) != len(re.findall('\/', sentence_tgt, re.I)):
        return True

    if chaotic_detected(sentence_src):
        return True

    return False


@plac.opt('file_in', "Input File", type=Path)
@plac.opt('file_out', "Output File", type=Path)
def filter_file(file_in,
                file_out):

    start_time = time.time()

    with open(file_in, 'r', encoding='utf8') as f_in, \
            open(file_out, 'w', encoding='utf8') as f_out:
        for line in f_in:
            sentences=line.split('|')
            if len(sentences)!=3:
                continue
            if is_filtered(sentences[1].strip(), sentences[2].strip()):
                continue
            f_out.write(line)

    print("finished " + file_in, flush=True)
    print("--- %s seconds ---" % (time.time() - start_time), flush=True)


def main():

    root_dir = '/home/xuanlong/dataclean/data/VMT'
    for folder, dirs, files in os.walk(root_dir):
        files.sort()
        for file in files:
            filter_file(os.path.join(folder, file),
                   os.path.join(folder, file+'.select'))


if __name__ == '__main__':
    main()
