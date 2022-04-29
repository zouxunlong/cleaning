import os
import time
from sentence_transformers import SentenceTransformer


model_sentence_transformers = SentenceTransformer('../model/labse_bert_model')

start_time = time.time()


def embedding_saving(sentences_en, sentences_tgt, filepath_out):
    source_embedding = model_sentence_transformers.encode(
        sentences_en, show_progress_bar=True, convert_to_numpy=True, normalize_embeddings=True)

    target_embedding = model_sentence_transformers.encode(
        sentences_tgt, show_progress_bar=True, convert_to_numpy=True, normalize_embeddings=True)

    assert len(source_embedding) == len(
        target_embedding), "length of src and target don't match"

    with open(filepath_out, 'a', encoding='utf8') as fOUT:
        for k in range(len(source_embedding)):
            cosine = source_embedding[k].dot(target_embedding[k])
            if cosine >= 0.7:
                fOUT.write("{:.4f} | {} | {}\n".format(
                    cosine, sentences_en[k].replace("|", " "), sentences_tgt[k].replace("|", " ")))


def clean_with_score(filepath_en, filepath_ms, filepath_out):
    with open(filepath_en, encoding='utf-8') as file_en, \
            open(filepath_ms, encoding='utf-8') as file_ms:

        sentences_en = []
        sentences_tgt = []
        for (i, sentence_en), (j, sentence_ms) in zip(enumerate(file_en), enumerate(file_ms)):
            if len(sentence_en.strip()) > 10 and len(sentence_ms.strip()) > 10:
                sentences_en.append(sentence_en.strip())
                sentences_tgt.append(sentence_ms.strip())

            if (i+1) % 100000 == 0:
                embedding_saving(sentences_en, sentences_tgt, filepath_out)
                sentences_en.clear()
                sentences_tgt.clear()
                print("finished "+str(i))

        embedding_saving(sentences_en, sentences_tgt, filepath_out)
        print("finished "+str(len(sentences_en)))

clean_with_score("/home/xuanlong/dataclean/data/ccaligned/CCAligned.en-ms.en",
                 "/home/xuanlong/dataclean/data/ccaligned/CCAligned.en-ms.ms", "/home/xuanlong/dataclean/data/ccaligned/CCAligned.en-ms.en-ms")


print("--- %s seconds ---" % (time.time() - start_time))
