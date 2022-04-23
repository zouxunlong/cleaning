from sentence_transformers import SentenceTransformer, util
from bitext_mining_utils import *
import numpy as np
import gzip
import tqdm
from sklearn.decomposition import PCA
import torch

# Model we want to use for bitext mining. LaBSE achieves state-of-the-art performance
model_name = 'LaBSE'
model = SentenceTransformer(model_name)


start_time = time.time()

# Input files. We interpret every line as sentence.
source_file = "sentences.en"
target_file = "sentences.ta"
output_file = "parallel-sentences1.en-ta"


# Only consider sentences that are between min_sent_len and max_sent_len characters long
min_sent_len = 4


print("Read source file")
source_sentences = set()
with open(source_file) as fIn:
    for line in tqdm.tqdm(fIn):
        line = line.strip()
        if len(line) >= min_sent_len:
            source_sentences.add(line)

print("Read target file")
target_sentences = set()
with open(target_file) as fIn:
    for line in tqdm.tqdm(fIn):
        line = line.strip()
        if len(line) >= min_sent_len:
            target_sentences.add(line)



print("Source Sentences:", len(source_sentences))
print("Target Sentences1:", len(target_sentences))


# Encode source sentences
source_sentences = list(source_sentences)


print("Encode source sentences")
source_embeddings = model.encode(
    source_sentences, show_progress_bar=True, convert_to_numpy=True)


# Encode target sentences
target_sentences = list(target_sentences)


print("Encode target sentences")
target_embeddings = model.encode(
    target_sentences, show_progress_bar=True, convert_to_numpy=True)


# Normalize embeddings
x = source_embeddings
x = x / np.linalg.norm(x, axis=1, keepdims=True)

y = target_embeddings
y = y / np.linalg.norm(y, axis=1, keepdims=True)


cosine_scores = util.cos_sim(x, y)


sentences_ta_written = 0


with open(output_file, 'w', encoding='utf8') as fOut:
    for i in range(len(cosine_scores)):
        for j in range(len(cosine_scores[0])):
            if cosine_scores[i][j] > 0.7:
                fOut.write("{:.4f} | {} | {}\n".format(cosine_scores[i][j], source_sentences[i].replace(
                    "|", " "), target_sentences[j].replace("|", " ")))
                sentences_ta_written += 1


print("Done. {} sentences ta written".format(sentences_ta_written))
print("--- %s seconds ---" % (time.time() - start_time))
