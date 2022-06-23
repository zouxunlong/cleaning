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
pattern_informal = r'[@#]|([^\w]|^)(http|https|www|com|hey|guy|kind\sof|ok|okay|oh|dude|we|you|your|my|me|haha|i)([^\w]|$)|\'(s|ve|re|t|m|ll|d|am|)\s|-\s'
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


def is_filtered(sentence_src, sentence_tgt):

    if informal_detected(sentence_src):
        return True

    if short_detected(sentence_src):
        return True

    if mis_spelling_detected(sentence_src):
        return True

    if unprintable_detected(sentence_src+' '+sentence_tgt):
        return True

    if emoji_detected(sentence_src+' '+sentence_tgt):
        return True

    return False


@plac.opt('input_1', "Src Input File", type=Path)
@plac.opt('output_1', "Src Output File", type=Path)
def main(input_1,
         output_1):

    start_time = time.time()

    with open(input_1, 'r', encoding='utf8') as f_in_1, \
            open(output_1, 'w', encoding='utf8') as f_out_1:
        for line in f_in_1:
            sentences = line.split('|')

            if is_filtered(sentences[1].strip(), sentences[2].strip(), ):
                continue
            
            f_out_1.write(line)

    print("finished: --- {} seconds".format(time.time() - start_time), flush=True)


if __name__ == '__main__':
    main('/home/xuanlong/dataclean/data.t4.en-id.seleted',
         '/home/xuanlong/dataclean/data.t7.en-id')
