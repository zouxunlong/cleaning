from sentence_transformers import SentenceTransformer, models
from bitext_mining_utils import *
import numpy as np
import gzip
import tqdm
import time
from sklearn.decomposition import PCA
import torch

start_time = time.time()

modelPath = '../model/labse_bert_model'

model = SentenceTransformer(modelPath)


#Input files. We interpret every line as sentence.
source_file = "sentences.en"
target_file = "sentences.ta"
output_file = "parallel-sentences.en-ta"

# Only consider sentences that are between min_sent_len and max_sent_len characters long
min_sent_len = 4

# We base the scoring on k nearest neighbors for each element
knn_neighbors = 2

# Min score for text pairs. Note, score can be larger than 1
min_threshold = 0.5

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
print("Target Sentences:", len(target_sentences))


### Encode source sentences
source_sentences = list(source_sentences)


print("Encode source sentences")
source_embeddings = model.encode(source_sentences, show_progress_bar=True, convert_to_numpy=True)


### Encode target sentences
target_sentences = list(target_sentences)

print("Encode target sentences")
target_embeddings = model.encode(target_sentences, show_progress_bar=True, convert_to_numpy=True)


# Normalize embeddings
x = source_embeddings
x = x / np.linalg.norm(x, axis=1, keepdims=True)

y = target_embeddings
y = y / np.linalg.norm(y, axis=1, keepdims=True)

# Perform kNN in both directions
x2y_sim, x2y_ind = kNN(x, y, knn_neighbors)
x2y_mean = x2y_sim.mean(axis=1)

y2x_sim, y2x_ind = kNN(y, x, knn_neighbors)
y2x_mean = y2x_sim.mean(axis=1)

# Compute forward and backward scores
margin = lambda a, b: a / b
fwd_scores = score_candidates(x, y, x2y_ind, x2y_mean, y2x_mean, margin)
bwd_scores = score_candidates(y, x, y2x_ind, y2x_mean, x2y_mean, margin)
fwd_best = x2y_ind[np.arange(x.shape[0]), fwd_scores.argmax(axis=1)]
bwd_best = y2x_ind[np.arange(y.shape[0]), bwd_scores.argmax(axis=1)]

indices = np.stack([np.concatenate([np.arange(x.shape[0]), bwd_best]), np.concatenate([fwd_best, np.arange(y.shape[0])])], axis=1)
scores = np.concatenate([fwd_scores.max(axis=1), bwd_scores.max(axis=1)])
seen_src, seen_trg = set(), set()

#Extact list of parallel sentences
print("Write sentences to disc")
sentences_written = 0
with open(output_file, 'w', encoding='utf8') as fOut:
    for i in np.argsort(-scores):
        src_ind, trg_ind = indices[i]
        src_ind = int(src_ind)
        trg_ind = int(trg_ind)

        if scores[i] < min_threshold:
            break

        if src_ind not in seen_src and trg_ind not in seen_trg:
            seen_src.add(src_ind)
            seen_trg.add(trg_ind)
            fOut.write("{:.4f} | {} | {}\n".format(scores[i], source_sentences[src_ind].replace("|", " "), target_sentences[trg_ind].replace("|", " ")))
            sentences_written += 1

print("Done. {} sentences written".format(sentences_written))
print("--- %s seconds ---" % (time.time() - start_time))
