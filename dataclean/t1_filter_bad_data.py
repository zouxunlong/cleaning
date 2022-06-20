import re
import time
import plac
from pathlib import Path


punctuation = r"""!"\#$%&'()*+,-./:;<=>?@[]^_`{|}~，。、‘’“”：；【】·！￥★…《》？！（）—"""
punctuation2none_dict = str.maketrans('', '', punctuation)
pattern_punctuation = r"""[!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~，。、‘’“”：；【】·！￥★…《》？！（）—]"""
pattern_url = r"[(http(s)?):\/\/(www\.)?a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,6}\b([-a-zA-Z0-9@:%_\+.~#?&//=]*)"
pattern_email = r"[\w\-\.]+@([\w\-]+\.)+[\w\-]{2,4}"
pattern_html = r"""<("[^"]*"|'[^']*'|[^'">])*>"""
pattern_special_charactors = r"[\x00-\x08\x0a-\x1f\x7f-\x9f\xa0]|[\ufffd\ufeff\u2000-\u200f\u2028-\u202f\u205f-\u206e]|[\↑√§¶†‡‖▪●•·]"


def chaotic_detected(text_for_chaotic_detect):
    alphabetic_text = re.sub('[^a-zA-Z]', '', text_for_chaotic_detect)
    if len(alphabetic_text)/len(text_for_chaotic_detect) < 0.5:
        return True
    return False


def is_filtered(sentence_src, sentence_tgt):
    
    if len(sentence_src) < 2:
        return True
    if len(sentence_tgt) < 2:
        return True
    if len(sentence_src.split()) < 4:
        return True
    if re.search("{}|{}".format(pattern_special_charactors, pattern_html), sentence_src+sentence_tgt, re.I):
        return True
    if len(re.findall(':', sentence_src, re.I)) != len(re.findall(':', sentence_tgt, re.I)):
        return True
    if len(re.findall('\/', sentence_src, re.I)) != len(re.findall('\/', sentence_tgt, re.I)):
        return True
    if len(re.findall(r'\\', sentence_src, re.I)) != len(re.findall(r'\\', sentence_tgt, re.I)):
        return True
    if len(re.findall('@', sentence_src, re.I)) != len(re.findall('@', sentence_tgt, re.I)):
        return True
    if len(re.findall('#', sentence_src, re.I)) != len(re.findall('#', sentence_tgt, re.I)):
        return True
    if chaotic_detected(sentence_src):
        return True

    return False

@plac.opt('input_1', "Src Input File", type=Path)
@plac.opt('input_2', "Tgt Input File", type=Path)
@plac.opt('output_1', "Src Output File", type=Path)
@plac.opt('output_2', "Tgt Output File", type=Path)
def main(input_1,
         input_2,
         output_1,
         output_2):
    start_time = time.time()
    with open(input_1, 'r', encoding='utf8') as f_in_en, \
            open(input_2, 'r', encoding='utf8') as f_in_id, \
            open(output_1, 'w', encoding='utf8') as f_out_en, \
            open(output_2, 'w', encoding='utf8') as f_out_id:
        for (i, sentence_en), (j, sentence_id) in zip(enumerate(f_in_en), enumerate(f_in_id)):
            if is_filtered(sentence_en.strip(), sentence_id.strip()):
                continue
            f_out_en.write(sentence_en)
            f_out_id.write(sentence_id)
    print("finished ")
    print("--- %s seconds ---" % (time.time() - start_time), flush=True)


if __name__ == '__main__':
    main('/home/xuanlong/dataclean/data/Total/train.en',
         '/home/xuanlong/dataclean/data/Total/train.id',
         '/home/xuanlong/dataclean/data/Total/train.filtered.en',
         '/home/xuanlong/dataclean/data/Total/train.filtered.id')
