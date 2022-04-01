import fasttext
import requests
from sentence_transformers import SentenceTransformer, util

model_sentence_transformers = SentenceTransformer('all-MiniLM-L6-v2')
model_fasttext = fasttext.load_model('./lid.176.bin')

print("Write sentences to disc")
sentences_written = 0
with open('wikimedia-cleaned.txt', 'at', encoding='utf8') as fOut, open("wikimedia.en-zh.zh", encoding='utf-8') as file_zh, open("wikimedia.en-zh.en", encoding='utf-8') as file_en:
    for (i, sentence_zh), (j, sentence_en) in zip(enumerate(file_zh), enumerate(file_en)):
        if i in range(0, 1000):
            ratio = len(sentence_en)/len(sentence_zh)
            if ratio > 2.5 and ratio < 4.5:
                sentence_zh=sentence_zh.strip()
                sentence_en=sentence_en.strip()
                
                if model_fasttext.predict(sentence_zh)[0][0]=="__label__zh" and model_fasttext.predict(sentence_en)[0][0]=="__label__en":
                    url = 'http://10.2.56.190:5005/translator'
                    d = {'source': 'zh_SG', 'target': 'en_SG', 'query': sentence_zh}
                    r = requests.post(url, data=d)
                    translatedText=eval(r.text)["data"]["translations"][0]['translatedText']
                    print(translatedText)
                    embedding1 = model_sentence_transformers.encode(translatedText, convert_to_tensor=True,device = "cpu")
                    embedding2 = model_sentence_transformers.encode(sentence_en, convert_to_tensor=True,device = "cpu")

                    # Compute cosine-similarities for each sentence with each other sentence
                    cosine_score = util.cos_sim(embedding1, embedding2)

                    if cosine_score[0][0]>0.8:
                        fOut.write("{} | {}\n".format(sentence_zh.replace("|", " "), sentence_en.replace("|", "")))
                        sentences_written += 1
                        print(sentences_written)