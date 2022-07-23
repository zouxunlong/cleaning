import os
import json
import plac
from pathlib import Path
from sentsplit.segment import SentSplit
import html
import pandas as pd

def output_metadata(metadata_file_path, metadata):

    with open(metadata_file_path, "w") as metafile:
        metafile.write(json.dumps(metadata))


def extract_sentences(input_path, output_file1, output_file2, lang):

    output_path_dir = os.path.dirname(output_file1)
    if not os.path.exists(output_path_dir):
        os.makedirs(output_path_dir)

    sent_splitter = SentSplit(lang, strip_spaces=True)

    df = pd.read_csv(input_path, header=None)

    with open(output_file1, "w", encoding="utf8") as fOut1, open(output_file2, "w", encoding="utf8") as fOut2:
        for i, [sentence0, sentence1, sentence2, sentence3] in enumerate(df.loc[0:].values):
            if i>0:
                if sentence2:
                    fOut1.write((html.unescape(sentence2)+"\n"))
                sentences = sent_splitter.segment(sentence3)
                if sentences:
                    fOut2.write(("\n".join([html.unescape(sentence) for sentence in sentences])+"\n"))


@plac.pos('input_path', "Src File/dir", type=Path)
@plac.pos('output_path', "Tgt File/dir", type=Path)
@plac.pos('lang', "language type", type=str)

def main(input_path="/home/xuanlong/dataclean/data/MediaCorp", output_path="/home/xuanlong/dataclean/data/MediaCorp", lang='en'):

    os.chdir(os.path.dirname(__file__))

    if os.path.isfile(input_path):
        if lang in {'ms','en','id','vi','ta','th'}:
            lang = 'en'
        elif lang in {'zh'}:
            lang = 'zh'
        extract_sentences(str(input_path), str(output_path), lang)

    elif os.path.isdir(input_path):
        for rootdir, dirs, files in os.walk(input_path):
            for file in files:
                if file.endswith('.csv'):
                    input_file = os.path.join(rootdir, file)
                    output_file1 = os.path.join(rootdir, file.replace('.csv', '_headlines.sent'))
                    output_file2 = os.path.join(rootdir, file.replace('.csv', '.sent'))
                    extract_sentences(input_file, output_file1, output_file2, lang)
    else:
        print("invalid input_file")


if __name__ == "__main__":
    plac.call(main)
