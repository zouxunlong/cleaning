
import os
import pandas as pd
import requests


class Translator:

    def __init__(
        self,
        itranslate_api='https://dev-api.itranslate.com/translation/v2/',
        sgtt_api='http://10.2.56.190:5008/translator',
    ):
        self.APIs = {
            'itranslate': itranslate_api,
            'sgtt': sgtt_api
        }
        self.api_headers = {
            'itranslate_head': {
                "Authorization": "Bearer 24784523-65ac-4c08-abcf-1ad90d398fe1",
                "Content-Type": "application/json"
            },
        }

    def itranslate(self, sentence_src, src, tgt):
        response = requests.post(url=self.APIs['itranslate'],
                                 headers=self.api_headers['itranslate_head'],
                                 json={
                                     "source": {"dialect": src, "text": sentence_src},
                                     "target": {"dialect": tgt}
        }
        )
        sentence_tgt = response.json()["target"]["text"]
        return sentence_tgt

    def google(self, sentence_src, src, tgt):
        response = requests.post(url=self.APIs['itranslate'],
                                 headers=self.api_headers['itranslate_head'],
                                 json={
                                     "source": {"dialect": src, "text": sentence_src},
                                     "target": {"dialect": tgt}
        }
        )
        sentence_tgt = response.json()["target"]["text"]
        return sentence_tgt

    def translate_sgtt(self, sentences_src, src, tgt):
        url = self.urls[src+'2'+tgt]
        sentences_tgt = []
        source = src+"_SG"
        target = tgt+"_SG"

        for i in range(0, len(sentences_src), self.batch_size):
            batch_sentences_src = sentences_src[i:i+self.batch_size]
            response = requests.post(
                url, json={"source": source, "target": target, "query": '\n'.join(batch_sentences_src)})
            batch_sentences_tgt = [item["translatedText"]
                                   for item in response.json()["data"]["translations"]]
            sentences_tgt.extend(batch_sentences_tgt)

        assert len(sentences_src) == len(
            sentences_tgt), 'length of source and target do not match'

        return sentences_tgt

    def translate(self, sentences_src, src, tgt):
        if (src, tgt) in [('en', 'th'), ('th', 'en')]:
            return self.translate_th(sentences_src, src, tgt)

        if (src, tgt) in [('en', 'zh'), ('zh', 'en'), ('en', 'ms'), ('ms', 'en'), ('en', 'ta'), ('ta', 'en')]:
            return self.translate_sgtt(sentences_src, src, tgt)


if __name__ == "__main__":
    translator = Translator()
    for rootdir, dirs, files in os.walk("/home/xunlong/dataclean/cleaning/wukui/files2"):
        for file in files:
            src = file[:2]
            tgt = file[3:5]
            src = 'zh-CN' if src == 'zh' else src
            tgt = 'zh-CN' if tgt == 'zh' else tgt

            df = pd.read_excel(os.path.join(rootdir, file))
            for i, sentence_src in enumerate(df.iloc[:, 0].values):
                sentence_itranslate = translator.itranslate(
                    sentence_src, src, tgt)
                df.loc[i,"iTranslate"] = sentence_itranslate
            df.to_excel(os.path.join(rootdir, file), index=False, header=True)

    print("finished all", flush=True)
