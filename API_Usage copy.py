# import requests
# url = 'http://10.2.56.190:5005/translator'
# d = {'source': 'zh_SG', 'target': 'en_SG', 'query': "举报者是2014年在韩国上映的一部电影，导演是任順禮"}
# r = requests.post(url, data=d)
# print(eval(r.text)["data"]["translations"][0]['translatedText'])


import aiohttp
import asyncio
import time
import fasttext
from nltk.translate.bleu_score import sentence_bleu
from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer('all-MiniLM-L6-v2')
model_fasttext = fasttext.load_model('./lid.176.bin')

start_time=time.time()

url = 'http://10.2.56.190:5005/translator'


async def main():

    async with aiohttp.ClientSession() as session:
        with open("wikimedia.en-zh.zh", encoding='utf-8') as file_zh, open("wikimedia.en-zh.en", encoding='utf-8') as file_en:
            for (i, text_zh), (j, text_en) in zip(enumerate(file_zh), enumerate(file_en)):
                if i in range(1,100):
                    sentences_zh = []
                    sentences_en = []
                    for sentence in text_zh.strip().split('。'):
                        language_type=model_fasttext.predict(sentence)
                        if language_type[0][0] == "__label__zh" and language_type[1][0] > 0.6:
                            sentences_zh.append(sentence)

                    for sentence in text_en.strip().split('.'):
                        language_type=model_fasttext.predict(sentence)
                        if language_type[0][0] == "__label__en" and language_type[1][0] > 0.6:
                            sentences_en.append(sentence)

                    if len(sentences_zh) != 0 and len(sentences_en) != 0:
                        references=[]
                        for sentence_zh in sentences_zh:

                            d = {'source': 'zh_SG', 'target': 'en_SG', 'query': sentence_zh}

                            # async with session.post(url,data=d) as resp:
                            #     r = await resp.json()
                            #     reference=r["data"]["translations"][0]['translatedText']
                            #     reference = reference.split(" ")
                            #     scores=[]
                            #     for sentence_en in sentences_en:
                            #         score = sentence_bleu([reference], sentence_en.split(" "))
                            #         print(score)
                            #         scores.append(score)
                            #     with open('parallel-sentences-cleaned_out.txt', 'at', encoding='utf8') as fOut:
                            #         for i in range(len(scores)):
                            #             if scores[i] > 0.65:
                            #                 fOut.write("{} | {}\n".format(sentence_zh.replace(
                            #                         "|", " "), sentences_en[i].replace("|", "")))
                            
                            async with session.post(url,data=d) as resp:
                                r = await resp.json()
                                reference=r["data"]["translations"][0]['translatedText']
                                references.append(reference)


                        embeddings1 = model.encode(references, convert_to_tensor=True)
                        embeddings2 = model.encode(sentences_en, convert_to_tensor=True)

                        cosine_scores = util.cos_sim(embeddings1, embeddings2)

                        with open('parallel-sentences-cleaned_out2.txt', 'at', encoding='utf8') as fOut:
                            for i in range(len(cosine_scores)):
                                for j in range(len(cosine_scores[0])):
                                    if cosine_scores[i][j] > 0.65:
                                        fOut.write("{} | {}\n".format(sentences_zh[i].replace(
                                            "|", " "), sentences_en[j].replace("|", "")))

asyncio.run(main())
print("--- %s seconds ---" % (time.time() - start_time))


# import aiohttp
# import asyncio
# import time

# start_time = time.time()

# async def get_pokemon(session, url):
#     async with session.post(url) as resp:
#         pokemon = await resp.json()
#         return pokemon['name']

# async def main():

#     async with aiohttp.ClientSession() as session:

#         tasks = []
#         for number in range(1, 151):
#             url = f'https://pokeapi.co/api/v2/pokemon/{number}'
#             tasks.append(asyncio.ensure_future(get_pokemon(session, url)))

#         original_pokemon = await asyncio.gather(*tasks)
#         for pokemon in original_pokemon:
#             print(pokemon)

# asyncio.run(main())
# print("--- %s seconds ---" % (time.time() - start_time))


# from nltk.translate.bleu_score import sentence_bleu, corpus_bleu
# reference1 = ['The', 'cat', 'sat', 'on', 'the', 'mat']
# reference2 = ['The', 'cat', 'sat', 'on', 'the']
# reference3 = ['The', 'cat', 'sat', 'on', 'the','house']
# candidate1 = ['The', 'cat', 'sat', 'on', 'the']
# candidate2 = ['The', 'cat', 'sat', 'on', 'the', 'mat']
# candidate3 = ['The', 'cat', 'sat', 'on', 'the', 'mat', 'garden']

# score = sentence_bleu([reference1], candidate1)
# score2 = sentence_bleu([reference1,reference2], candidate1)
# score22 = corpus_bleu([[reference1,reference2],[reference3,reference2]], [candidate1,candidate2])

# print(score)
