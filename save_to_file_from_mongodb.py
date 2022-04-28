import time
from sentence_transformers import SentenceTransformer
from pymongo import MongoClient


client = MongoClient("mongodb://localhost:27017/")


start_time = time.time()

with open("../data/clean_sorted.en-zh", 'w', encoding='utf8') as fOUT:
    sentence_pairs=client["translation_data"]["sentence_pair"].find().sort('cos',-1)
    for sentence_pair in sentence_pairs:
        fOUT.write("{:.4f} | {} | {}\n".format(sentence_pair['cos'], sentence_pair['sentence_en'], sentence_pair['sentence_zh']))



print("--- %s seconds ---" % (time.time() - start_time))
