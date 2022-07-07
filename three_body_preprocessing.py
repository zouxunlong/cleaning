import re


def preprocess_sentence(s):
    s = s.lower().strip()

    s = re.sub(r"([?.!,？。！，])", r" \1 ", s)
    s = re.sub(r'[" "]+', r" ", s)

    s = re.sub(r"[^a-zA-Z?.!,？。！，\u4e00-\u9fff]+", r" ", s)
    s = s.strip()

    s = '<start> '+s+' <end>'

    return s


with open('/home/xuanlong/dataclean/data/cleaned/clean_sorted.en-zh', 'r', encoding='utf8') as f_in, \
        open('/home/xuanlong/dataclean/data/cleaned/clean_sorted.en-zh.en', 'w', encoding='utf8') as f_out_en, \
        open('/home/xuanlong/dataclean/data/cleaned/clean_sorted.en-zh.zh', 'w', encoding='utf8') as f_out_zh:
    for i, line in enumerate(f_in):
        score, en, zh = line.split('|')
        f_out_zh.write(preprocess_sentence(zh)+'\n')
        f_out_en.write(preprocess_sentence(en)+'\n')
