import time
from sentence_transformers import SentenceTransformer
from pymongo import MongoClient


client = MongoClient("mongodb://localhost:27018/")

model_sentence_transformers = SentenceTransformer('../model/labse_bert_model')

start_time = time.time()

with open("../data/noisy_1.en-zh", encoding='utf-8') as fIN:
    sentences_en = []
    sentences_zh = []
    for i, sentence in enumerate(fIN):
        sentences = sentence.split('|')
        sentences_en.append(sentences[0].strip())
        sentences_zh.append(sentences[1].strip())

        if i > 0 and i % 100000 == 0:
            source_embedding = model_sentence_transformers.encode(
                sentences_en, show_progress_bar=True, convert_to_numpy=True, normalize_embeddings=True)
            target_embedding = model_sentence_transformers.encode(
                sentences_zh, show_progress_bar=True, convert_to_numpy=True, normalize_embeddings=True)

            for j in range(len(source_embedding)):
                cosine = source_embedding[j].dot(target_embedding[j])
                if cosine > 0.7:
                    client["translation_data"]["sentence_pair"].insert_one(
                        {'cos': float(cosine), 'sentence_en': sentences_en[j], 'sentence_zh': sentences_zh[j]})
            sentences_en.clear()
            sentences_zh.clear()
print("--- %s seconds ---" % (time.time() - start_time))
