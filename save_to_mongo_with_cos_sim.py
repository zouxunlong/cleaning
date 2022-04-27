import time
from sentence_transformers import SentenceTransformer
from pymongo import MongoClient


client = MongoClient("mongodb://localhost:27018/")

model_sentence_transformers = SentenceTransformer('../model/labse_bert_model')

start_time = time.time()
for file in ["../data/noisy_3.en-zh","../data/noisy_4.en-zh","../data/noisy_5.en-zh"]:
    with open(file, encoding='utf-8') as fIN:
        sentences_en = []
        sentences_zh = []
        for i, sentence in enumerate(fIN):
            sentences = sentence.split('|')
            sentences_en.append(sentences[0].strip())
            sentences_zh.append(sentences[1].strip())

            if (i+1) % 100000 == 0:
                source_embedding = model_sentence_transformers.encode(
                    sentences_en, convert_to_numpy=True, normalize_embeddings=True)
                target_embedding = model_sentence_transformers.encode(
                    sentences_zh, convert_to_numpy=True, normalize_embeddings=True)
                assert len(source_embedding)==len(target_embedding)
                for j in range(len(source_embedding)):
                    cosine = source_embedding[j].dot(target_embedding[j])
                    if cosine > 0.7:
                        client["translation_data"]["sentence_pair"].insert_one(
                            {'cos': float(cosine), 'sentence_en': sentences_en[j], 'sentence_zh': sentences_zh[j]})
                sentences_en.clear()
                sentences_zh.clear()
                print("finished "+str(i))
print("--- %s seconds ---" % (time.time() - start_time))
