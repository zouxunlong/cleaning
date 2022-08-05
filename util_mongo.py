from whoosh.analysis import StemmingAnalyzer, SimpleAnalyzer
from custom_analyzers import ThAnalyzer, ViAnalyzer, TaAnalyzer
from jieba.analyse import ChineseAnalyzer
from pymongo import MongoClient, TEXT
import json
import pandas as pd

MONGODB_CONNECTION_STRING = 'mongodb://localhost:27017/'
mongo_client = MongoClient(MONGODB_CONNECTION_STRING)

collection_wukui = mongo_client['mlops']['wukui']


def get_analyzer(lang):
    if lang == 'en':
        analyzer = StemmingAnalyzer()
    elif lang == 'zh':
        analyzer = ChineseAnalyzer()
    elif lang == 'ms':
        analyzer = SimpleAnalyzer()
    elif lang == 'id':
        analyzer = SimpleAnalyzer()
    elif lang == 'ta':
        analyzer = TaAnalyzer()
    elif lang == 'vi':
        analyzer = ViAnalyzer()
    elif lang == 'th':
        analyzer = ThAnalyzer()
    else:
        analyzer = SimpleAnalyzer()
    return analyzer


def insert_data(file_path_src, file_path_tgt, lang_src, lang_tgt):
    try:
        analyzer_src = get_analyzer(lang_src)
        analyzer_tgt = get_analyzer(lang_tgt)
        with open(file_path_src, encoding='utf8') as file_src,\
                open(file_path_tgt, encoding='utf8') as file_tgt:
            for (i, line_src), (j, line_tgt) in zip(enumerate(file_src), enumerate(file_tgt)):
                tokens_src = [
                    token.text for token in analyzer_src(line_src.strip())]
                tokens_tgt = [
                    token.text for token in analyzer_tgt(line_tgt.strip())]
                result = collection_wukui.insert_one(
                    {'sentence_src': line_src.strip(),
                     'sentence_tgt': line_tgt.strip(),
                     'lang_src': lang_src,
                     'lang_tgt': lang_tgt,
                     'tokens_src': tokens_src,
                     'tokens_tgt': tokens_tgt,
                     'domain': ['full-domain']})

            print("inserted {} documents.".format(i), flush=True)
    except Exception as err:
        print(err, flush=True)
        print(i, flush=True)


def insert_data2(jl_path, lang_src, lang_tgt):
    try:
        analyzer_src = get_analyzer(lang_src)
        analyzer_tgt = get_analyzer(lang_tgt)
        with open(jl_path, 'r', encoding='utf-8') as f_in:
            for line in f_in:
                item = json.loads(line)

                tokens_src = [
                    token.text for token in analyzer_src(item["sentence_src"].strip())]
                tokens_tgt = [
                    token.text for token in analyzer_tgt(item["sentence_tgt"].strip())]

                result = collection_wukui.insert_one(
                    {'sentence_src': item["sentence_src"].strip(),
                     'sentence_tgt': item["sentence_tgt"].strip(),
                     'source_lang': item["source_lang"],
                     'target_lang': item["target_lang"],
                     'tokens_src': tokens_src,
                     'tokens_tgt': tokens_tgt,
                     'data_source': 'airflow',
                     'domain': ['full-domain', 'news']})

        print("finished insert documents.", flush=True)
    except Exception as err:
        print(err, flush=True)


def insert_data3(jl_path):
    try:
        with open(jl_path, 'r', encoding='utf-8') as f_in:
            i = 1000000000000000001
            for j, line in enumerate(f_in):
                item = json.loads(line)

                result = collection_wukui.insert_one(
                    {'_id': i+j,
                     'sentence_src': item["sentence_src"].strip(),
                     'sentence_tgt': item["sentence_tgt"].strip(),
                     'lang_src': item["source_lang"],
                     'lang_tgt': item["target_lang"],
                     'data_source': 'airflow',
                     'domain': ['full-domain', 'news']})

        print("finished insert documents.", flush=True)
    except Exception as err:
        print(err, flush=True)


def build_index_text():


    collection_wukui.create_index(
        [
            ('tokens_tgt', 1),
        ]
    )
    collection_wukui.create_index(
        [
            ('tokens_src', 1),
        ]
    )


def build_array():

    for document in collection_wukui.find():

        collection_wukui.update_one(
            {'_id': document['_id']},
            {
                '$set': {
                    'array_en': document['tokens_en'].split(),
                    'array_zh': document['tokens_zh'].split()
                }
            }
        )


def build_int_index():
    i = 1000000000000000001
    try:
        result = collection_wukui.find({}, {"_id": 1})
        for item in result:
            collection_wukui.update_one({'_id': item['_id']}, {
                                  '$set': {'milvus_id': i}})
            i += 1
            if i % 100000 == 0:
                print(i, flush=True)
    except Exception as err:
        print(err, flush=True)
        print(i, flush=True)


def search_query(query, lang):

    analyzer = get_analyzer(lang)

    tokens_query = [token.text for token in analyzer(query)]

    print(tokens_query, flush=True)

    pipeline = []
    pipeline.append({"$match": {"$or": [{"$and": [{"lang_src": lang}, {"tokens_src": {"$all": tokens_query}}]},
                                        {"$and": [{"lang_tgt": lang}, {"tokens_tgt": {"$all": tokens_query}}]}]}})

    pipeline.append({"$limit": 20000})

    results = collection_wukui.aggregate(pipeline)

    retrieved_items = [result for result in results]
    items_df = pd.DataFrame.from_records(data=retrieved_items, columns=['sentence_src',
                                                                        'sentence_tgt',
                                                                        'lang_src',
                                                                        'lang_tgt',
                                                                        'data_source',
                                                                        'domain',
                                                                        'source_media',
                                                                        '_id'])
    if not items_df.empty:
        items_df['_id'] = items_df['_id'].apply(lambda s: str(s))
        items_df = items_df.reset_index()
    return items_df, tokens_query


if __name__ == "__main__":
    insert_data3('./data/translated_sentence.en')
    # build_index_text()
    # build_array()
    # print(collection_wukui.index_information())
    # search_query("this is singapore's best food", "en")
    # build_int_index()
    print("finished", flush=True)
