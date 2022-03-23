import fasttext
from sentence_transformers import SentenceTransformer, util

model_sentence_transformers = SentenceTransformer("LaBSE")

model_fasttext = fasttext.load_model('./lid.176.bin')



print("Write sentences to disc")
sentences_written = 0
with open('parallel-sentences-cleaned_out.txt', 'wt', encoding='utf8') as fOut, open("wikimedia.en-zh.zh", encoding='utf-8') as file_zh, open("wikimedia.en-zh.en", encoding='utf-8') as file_en:
    for sentence_zh, sentence_en in zip(file_zh, file_en):
        sentence_zh=sentence_zh.strip()
        sentence_en=sentence_en.strip()
        
        if model_fasttext.predict(sentence_zh)[0][0]=="__label__zh" and model_fasttext.predict(sentence_en)[0][0]=="__label__en":
            embedding1 = model_sentence_transformers.encode(sentence_zh, convert_to_tensor=True)
            embedding2 = model_sentence_transformers.encode(sentence_en, convert_to_tensor=True)

            # Compute cosine-similarities for each sentence with each other sentence
            cosine_score = util.cos_sim(embedding1, embedding2)

            if cosine_score[0][0]>0.8:
                fOut.write("{} | {} | Score: {:.4f}\n".format(sentence_zh.replace("|", " "), sentence_en.replace("|", ""), cosine_score[0][0]))
                sentences_written += 1
                print(sentences_written)

print("Done. {} sentences written".format(sentences_written))