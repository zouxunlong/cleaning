from sentence_transformers import SentenceTransformer, util
from milvus import Milvus, IndexType, MetricType, Status
import numpy as np
import torch
import os
from pymongo import MongoClient, TEXT

MONGODB_CONNECTION_STRING = 'mongodb://localhost:27017/'
mongo_client = MongoClient(MONGODB_CONNECTION_STRING)

db = mongo_client['mlops']
collection = db['airflow']
milvus_collection_name = 'airflow'

torch.cuda.set_device(1)
os.environ["TOKENIZERS_PARALLELISM"] = "false"

_HOST = '127.0.0.1'
_PORT = '19530'
_DIM = 768
_INDEX_FILE_SIZE = 2048

milvus = Milvus(host=_HOST, port=_PORT)

# model_sentence_transformers = SentenceTransformer('./model/labse_bert_model')
# model_sentence_transformers = SentenceTransformer('all-mpnet-base-v2')


def _create_collection(collection_name):

    status, ok = milvus.has_collection(collection_name)
    if not ok:
        param = {
            'collection_name': collection_name,
            'dimension': _DIM,
            'index_file_size': _INDEX_FILE_SIZE,  # optional
            'metric_type': MetricType.IP  # optional
        }

        milvus.create_collection(param)

    print(milvus.list_collections(), flush=True)
    print(milvus.get_collection_info(collection_name), flush=True)
    print(milvus.get_collection_stats(collection_name), flush=True)
    print(milvus.get_index_info(collection_name), flush=True)


def _insert(collection_name, vectors, milvus_ids):

    status, ids = milvus.insert(collection_name=collection_name,
                                records=vectors,
                                ids=milvus_ids)

    if not status.OK():
        print("Insert failed: {}".format(status), flush=True)

    milvus.flush([collection_name])

    status, result = milvus.count_entities(collection_name)

    print(milvus.get_collection_stats(collection_name), flush=True)
    print(milvus.get_index_info(collection_name), flush=True)


def query(collection_name, query):

    query_vector = model_sentence_transformers.encode([query],
                                                      show_progress_bar=False,
                                                      convert_to_numpy=True,
                                                      normalize_embeddings=True)

    search_param = {"nprobe": 1}

    param = {
        'collection_name': collection_name,
        'query_records': query_vector,
        'top_k': 10,
        'params': search_param,
    }

    status, results = milvus.search(**param)

    if status.OK():
        print(results, flush=True)
    else:
        print("Search failed. ", status, flush=True)

    return results


def main():

    _create_collection(milvus_collection_name)

    results = collection.find({}, {'sentence_src': 1, 'sentence_tgt': 1, '_id': 1})
    sentences_src = []
    sentences_tgt = []
    milvus_ids = []
    for item in results:
        sentences_src.append(item['sentence_src'])
        sentences_tgt.append(item['sentence_tgt'])
        milvus_ids.append(item['_id'])

        if item['_id'] % 50000 == 0:

            embeddings = model_sentence_transformers.encode(
                sentences_src, show_progress_bar=False, convert_to_numpy=True, normalize_embeddings=True)

            assert len(embeddings) == len(milvus_ids), "length of embeddings and ids don't match"

            _insert(milvus_collection_name, embeddings, milvus_ids)

            sentences_src.clear()
            sentences_tgt.clear()
            milvus_ids.clear()
            print(item['_id'], flush=True)

    embeddings = model_sentence_transformers.encode(
        sentences_src, show_progress_bar=False, convert_to_numpy=True, normalize_embeddings=True)

    assert len(embeddings) == len(milvus_ids), "length of embeddings and ids don't match"
    
    _insert(milvus_collection_name, embeddings, milvus_ids)

    sentences_src.clear()
    sentences_tgt.clear()
    milvus_ids.clear()
    print('all finished', flush=True)


if __name__ == "__main__":
    # results=query(collection_name,"I'll have to let you know later what I think.")
    # print(results.id_array)
    # print(results.distance_array)
    # for (i, milvus_id), (j, distance) in zip(enumerate(results.id_array[0]), enumerate(results.distance_array[0])):
    #     print(milvus_id)
    #     print(distance)
    #     sentence=collection.find_one({"_id":milvus_id})["sentence_src"]
    #     print(sentence)

    # main()
    index_param = {'nlist': 4096}
    status = milvus.create_index(milvus_collection_name,
                                 IndexType.IVF_FLAT,
                                 index_param)
    print('success', flush=True)
    # print(milvus.drop_index(milvus_collection_name), flush=True)
    print(milvus.list_collections(), flush=True)
    print(milvus.get_collection_info(milvus_collection_name), flush=True)
    print(milvus.get_collection_stats(milvus_collection_name), flush=True)
    print(milvus.get_index_info(milvus_collection_name), flush=True)